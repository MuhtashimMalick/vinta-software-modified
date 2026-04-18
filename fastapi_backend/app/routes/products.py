# app/routers/unleashed.py
import asyncio
import logging
import httpx


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import  get_async_session
from app.models import TItems
from app.utils import fetch_all_unleashed_products, map_item, fetch_all_stock_on_hand
from app.logging_config import get_jsonl_logger, build_jsonl_entry


jsonl_logger = get_jsonl_logger()
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/import-products")
async def sync_unleashed_products(db: AsyncSession = Depends(get_async_session)):
    """
    1. Fetch all Products from Unleashed.
    2. Fetch all StockOnHand from Unleashed.
    3. Merge on ProductCode.
    4. Sync into tItems (keyed on UnleashedGUID):
       - INSERT if not seen before.
       - UPDATE if Unleashed LastModifiedOn is newer than DB.
       - SKIP if DB is already current.
       - DELETE if product no longer exists in Unleashed.
    """

    # -- Step 1 & 2: fetch both APIs concurrently --
    try:
        products, stock_map = await asyncio.gather(
            fetch_all_unleashed_products(),
            fetch_all_stock_on_hand(),
        )
    except httpx.HTTPError as e:
        jsonl_logger.info(build_jsonl_entry(
            action_type="Sync Products from Unleashed to SQL",
            action_variant="sync-products-from-unleashed",
            status="Error",
            message=f"Unleashed API error: {e}",
        ))
        raise HTTPException(status_code=502, detail=f"Unleashed API error: {e}")

    # -- Step 3: load existing products from DB in one query --
    existing_rows = (await db.execute(
        select(TItems.ItemNumber, TItems.ItemID, TItems.DateLastModified)
    )).all()
    existing_map = {row.ItemNumber: row for row in existing_rows}

    # Create set of current Unleashed ProductCodes for deletion check
    unleashed_product_codes = {p.get("ProductCode") for p in products if p.get("ProductCode")}

    inserted = updated = skipped = deleted = 0
    errors = []

    max_id_result = await db.execute(select(func.max(TItems.ItemID)))
    current_max_id = max_id_result.scalar() or 0
    next_id = current_max_id + 1

    # Process each product from Unleashed
    for product in products:
        try:
            product_code = product.get("ProductCode")
            if not product_code:
                skipped += 1
                continue
     
            stock = stock_map.get(product_code)
            mapped = map_item(product, stock)
     
            if product_code not in existing_map:
                # INSERT new product
                mapped["ItemID"] = next_id
                logger.info(f"Inserting ItemID={next_id} for {product_code}")
                db.add(TItems(**mapped))
                await db.flush()  
                next_id += 1
                inserted += 1
            else:
                # UPDATE if changed
                existing_row = existing_map[product_code]
                db_modified = existing_row.DateLastModified
                unleashed_modified = mapped.get("DateLastModified")
                unleashed_modified = unleashed_modified.replace(microsecond=0)
                db_modified = db_modified.replace(microsecond=0)

                print(unleashed_modified, db_modified)

                if (
                    unleashed_modified
                    and db_modified
                    and unleashed_modified > db_modified
                ):
                    # Product has been modified in Unleashed
                    logger.info(f"Updating ItemID={existing_row.ItemID} for {product_code}")
                    await db.execute(
                        TItems.__table__.update()
                        .where(TItems.ItemID == existing_row.ItemID)
                        .values(**{k: v for k, v in mapped.items() if k != "UnleashedGUID"})
                    )
                    updated += 1
                else:
                    # Product is current, no update needed
                    skipped += 1

        except Exception as e:
            error_msg = f"Error processing product {product.get('ProductCode', 'Unknown')}: {str(e)}"
            logger.error(error_msg)
            jsonl_logger.info(build_jsonl_entry(
                action_type="Sync Products from Unleashed to SQL",
                action_variant="sync-products-from-unleashed",
                status="Error",
                message=error_msg,
            ))
            errors.append(error_msg)
    
    # DELETE products that are in DB but not in Unleashed
    logger.info("Checking for deleted products...")
    for item_number, existing_row in existing_map.items():
        if item_number not in unleashed_product_codes:
            try:
                await db.execute(
                    TItems.__table__.delete()
                    .where(TItems.ItemID == existing_row.ItemID)
                )
                deleted += 1
                logger.info(f"Deleted ItemID={existing_row.ItemID} with ItemNumber={item_number} (no longer in Unleashed)")
            except Exception as e:
                error_msg = f"Error deleting product ItemID={existing_row.ItemID}: {str(e)}"
                logger.error(error_msg)
                jsonl_logger.info(build_jsonl_entry(
                    action_type="Sync Products from Unleashed to SQL",
                    action_variant="sync-products-from-unleashed",
                    status="Error",
                    message=error_msg,
                ))
                errors.append(error_msg)
 
    await db.commit()
    
    logger.info(f"Product sync complete - Inserted: {inserted}, Updated: {updated}, Skipped: {skipped}, Deleted: {deleted}, Failed: {len(errors)}")
    jsonl_logger.info(build_jsonl_entry(
        action_type="Sync Products from Unleashed to SQL",
        action_variant="sync-products-from-unleashed",
        status="Success",
        message=f"Sync complete: {inserted} inserted, {updated} updated, {deleted} deleted, {skipped} skipped",
    ))
    
    return {
        "status": "success",
        "total_from_api": len(products),
        "stock_records_fetched": len(stock_map),
        "inserted": inserted,
        "updated": updated,
        "deleted": deleted,
        "skipped": skipped,
        "errors": errors if errors else []
    }
