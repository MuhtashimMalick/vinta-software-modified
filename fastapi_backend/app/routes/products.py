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
    4. Upsert into tItems (keyed on UnleashedGUID).
       - INSERT if not seen before.
       - UPDATE only if Unleashed LastModifiedOn is newer than DB.
       - SKIP if DB is already current.
    """

    # -- Step 1 & 2: fetch both APIs concurrently --
    try:
        products, stock_map = await asyncio.gather(
            fetch_all_unleashed_products(),
            fetch_all_stock_on_hand(),
        )
    except httpx.HTTPError as e:
        jsonl_logger.info(build_jsonl_entry(
            action_type="Import from Unleashed to SQL",
            action_variant="import-from-unleashed-to-sql",
            status="Error",
            message=f"Unleashed API error: {e}",
        ))
        raise HTTPException(status_code=502, detail=f"Unleashed API error: {e}")

    # -- Step 3: load existing GUIDs from DB in one query --
    existing_rows = (await db.execute(
        select(TItems.UnleashedGUID, TItems.ItemID, TItems.DateLastModified)
        .where(TItems.UnleashedGUID.isnot(None))
    )).all()
    existing_map = {row.UnleashedGUID: row for row in existing_rows}

    inserted = updated = skipped = 0

    max_id_result = await db.execute(select(func.max(TItems.ItemID)))
    current_max_id = max_id_result.scalar() or 0
    next_id = current_max_id + 1

    for product in products:
        guid = product.get("Guid")
        if not guid:
            skipped += 1
            continue
 
        product_code = product.get("ProductCode")
        stock = stock_map.get(product_code)
        mapped = map_item(product, stock)
 
        if guid not in existing_map:
            mapped["ItemID"] = next_id
            logger.info(f"Inserting ItemID={next_id} for {product.get('ProductCode')}")
            db.add(TItems(**mapped))
            await db.flush()  
            next_id += 1
            inserted += 1
        # else:
        #     existing_row = existing_map[guid]
        #     db_modified = existing_row.DateLastModified
        #     unleashed_modified = mapped["DateLastModified"]
 
        #     if (
        #         unleashed_modified
        #         and db_modified
        #         and unleashed_modified == db_modified
        #     ):
        #         skipped += 1
        #         continue
 
        #     await db.execute(
        #         TItems.__table__.update()
        #         .where(TItems.ItemID == existing_row.ItemID)
        #         .values(**{k: v for k, v in mapped.items() if k != "UnleashedGUID"})
        #     )
        #     updated += 1
 
    await db.commit()
    jsonl_logger.info(build_jsonl_entry(
        action_type="Import from Unleashed to SQL",
        action_variant="import-from-unleashed-to-sql",
        status="Success",
        message=f"Successfully inserted {inserted} products.",
    ))
    return {
        "status": "success",
        "total_from_api": len(products),
        "stock_records_fetched": len(stock_map),
        "inserted": inserted,
        # "updated": updated,
        # "skipped": skipped,
    }
