import base64
import hashlib
import hmac
import httpx
import logging
import re

from typing import Optional
from datetime import datetime, timezone

from app.config import settings

from fastapi.routing import APIRoute


logger = logging.getLogger(__name__)


def simple_generate_unique_route_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


def generate_signature(api_key: str, query_string: str = ""):
    message = query_string.encode("utf-8")
    secret = api_key.encode("utf-8")
    signature = hmac.new(secret, message, hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def get_headers(query_string: str = ""):
    return {
        "api-auth-id": settings.API_ID,
        "api-auth-signature": generate_signature(settings.API_KEY, query_string),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


async def fetch_all_unleashed_products() -> list[dict]:
    """Paginate through all products from the Products API."""
    products = []
    page = 1
    page_size = 1000

    async with httpx.AsyncClient() as client:
        while True:
            query_string = f"PageSize={page_size}"
            response = await client.get(
                f"{settings.BASE_URL}/Products/{page}",
                params={"PageSize": page_size},
                headers=get_headers(query_string=query_string),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            items = data.get("Items", [])
            products.extend(items)

            pagination = data.get("Pagination", {})
            if page >= pagination.get("NumberOfPages", 1):
                break
            page += 1

    logger.info(f"Fetched {len(products)} products from Unleashed")

    return products


def map_item(product: dict, stock: Optional[dict] = None) -> dict:
    """
    Merge a Products API record with its StockOnHand record into a
    tItems column dict.  Stock data fills the inventory quantity/value
    fields that the Products API does not provide.
    """
    stock = stock or {}

    # Sell prices — safely cast from string
    def tier(key: str) -> Optional[float]:
        return safe_float((product.get(key) or {}).get("Value"))

    base_sell = tier("SellPriceTier1") or 0.0

    # Cost — StockOnHand AvgCost is more reliable than AverageLandPrice
    avg_cost = safe_float(stock.get("AvgCost")) or safe_float(product.get("AverageLandPrice")) or 0.0

    return {
        # --- Identity ---
        "UnleashedGUID":                    product.get("Guid"),
        "ItemNumber":                       product.get("ProductCode"),
        "ItemName":                         (product.get("ProductDescription") or ""),
        "ItemDescription":                  (product.get("ProductDescription") or ""),

        # --- Status flags ---
        "IsInactive":                       bool_to_yn(product.get("Obsolete", False)),
        "ItemIsSold":                       bool_to_yn(product.get("IsSellable", False)),
        "ItemIsBought":                     bool_to_yn(product.get("IsPurchasable", False)),
        "ItemIsInventoried":                'Y', # (DECIDE)

        # --- Quantities (from StockOnHand) ---
        "QuantityOnHand":                   safe_float(stock.get("QtyOnHand")) or 0.0,
        "ValueOnHand":                      safe_float(stock.get("TotalCost")) or 0.0,
        "SellOnOrder":                      safe_float(stock.get("AllocatedQty")) or 0.0,
        "PurchaseOnOrder":                  safe_float(stock.get("OnPurchase")) or 0.0,

        # --- Cost (StockOnHand preferred, Products API fallback) ---
        "TaxExclusiveStandardCost":         avg_cost,
        "TaxExclusiveLastPurchasePrice":    avg_cost,
        "TaxInclusiveLastPurchasePrice":    avg_cost,   # Unleashed doesn't split this out

        # --- Units of measure ---
        "SellUnitMeasure":                  (product.get("UnitOfMeasure") or {}).get("Name") or "",
        "SellUnitQuantity":                 1,
        "BuyUnitMeasure":                   (product.get("DefaultPurchasesUnitOfMeasure") or {}).get("Name") or "",
        "BuyUnitQuantity":                  1,

        # --- Sell prices ---
        "BaseSellingPrice":                 base_sell,
        "SellPrice1":                       tier("SellPriceTier1"),
        "SellPrice2":                       tier("SellPriceTier2"),
        "SellPrice3":                       tier("SellPriceTier3"),
        "SellPrice4":                       tier("SellPriceTier4"),
        "SellPrice5":                       tier("SellPriceTier5"),
        "SellPrice6":                       tier("SellPriceTier6"),
        "SellPrice7":                       tier("SellPriceTier7"),
        "SellPrice8":                       tier("SellPriceTier8"),
        "SellPrice9":                       tier("SellPriceTier9"),
        "SellPrice10":                      tier("SellPriceTier10"),

        # --- Reorder / stock levels ---
        "MinLevelBeforeReorder":            safe_float(product.get("MinStockAlertLevel")) or 0.0,
        "DefaultReorderQuantity":           safe_float(product.get("ReOrderPoint")),
        "DefaultReoderQuantity":            safe_float(product.get("ReOrderPoint")),  # legacy typo column

        # --- Tracking ---
        "BatchTracked":                     bool_to_yn(product.get("IsBatchTracked", False)),
        "SerialTracked":                    bool_to_yn(product.get("IsSerialized", False)),

        # --- Supplier ---
        "SupplierName":                     (product.get("Supplier") or {}).get("SupplierName"),

        # --- Categories (StockOnHand ProductGroupName confirms Products API) ---
        "CatSearch_1":                      stock.get("ProductGroupName") or (product.get("ProductGroup") or {}).get("GroupName"),
        "CatSearch_2":                      (product.get("ProductSubGroup") or {}).get("GroupName"),

        # --- Custom fields ---
        "CustomField1":                     product.get("Barcode") or "",   # no native barcode column
        "Picture":                          product.get("ImageUrl") or "",

        # --- Timestamps ---
        "DateLastModified":                 parse_unleashed_date(product.get("LastModifiedOn")),

        # --- Required non-null columns (set sensible defaults) ---
        # ⚠️  Replace 0 account IDs with your real chart-of-accounts IDs
        "IncomeAccountID":                  0,
        "UseDescription":                   'N',
        "PriceIsInclusive":                 'N',
        "SellTaxCodeID":                    0,
        "SalesTaxCalcBasisID":              'ITE',
        "ChangeControl":                    '0000000000',
    }


# IncomeAccountID, ExpenseAccountID, InventoryAccountID
# CustomList1ID, CustomList2ID, CustomList3ID
# CustomField1, CustomField2, CustomField3
# SellTaxCodeID, BuyTaxCodeID (unleashed is not providing any tax field with values to map to these)
# PrimarySupplierID, SupplierItemNumber (imp) (unleashed is giving Supplier: null)
# ChangeControl

def parse_unleashed_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse Unleashed's /Date(milliseconds)/ format."""
    if not date_str:
        return None
    match = re.search(r'/Date\((\d+)\)/', date_str)
    if match:
        ms = int(match.group(1))
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).replace(tzinfo=None)
    return None


def bool_to_yn(value: Optional[bool]) -> str:
    return 'Y' if value else 'N'


def safe_float(val) -> Optional[float]:
    try:
        return float(val) if val is not None else None
    except (ValueError, TypeError):
        return None


async def fetch_all_stock_on_hand() -> dict[str, dict]:
    """
    Paginate through StockOnHand API.
    Returns a dict keyed by ProductCode for easy lookup.
    Note: When WarehouseCode/WarehouseId are empty the row represents
    the aggregate across all warehouses — which is what we want for tItems.
    """
    stock_map: dict[str, dict] = {}
    page = 1
    page_size = 1000

    async with httpx.AsyncClient() as client:
        while True:
            query_string = f"PageSize={page_size}"
            response = await client.get(
                f"{settings.BASE_URL}/StockOnHand/{page}",
                params={"PageSize": page_size},
                headers=get_headers(query_string=query_string),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            for item in data.get("Items", []):
                product_code = item.get("ProductCode")
                warehouse_code = item.get("WarehouseCode", "")

                if not product_code:
                    continue

                # Prefer the aggregate row (empty WarehouseCode = all warehouses).
                # Only store a warehouse-specific row if no aggregate exists yet.
                if warehouse_code == "" or product_code not in stock_map:
                    stock_map[product_code] = item

            pagination = data.get("Pagination", {})
            if page >= pagination.get("NumberOfPages", 1):
                break
            page += 1

    logger.info(f"Fetched {len(stock_map)} stock records from Unleashed")

    return stock_map
