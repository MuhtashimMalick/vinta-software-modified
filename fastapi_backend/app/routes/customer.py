# app/routers/unleashed.py

import datetime
import logging
import requests

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import  get_async_session
from app.models import TCustomers
from app.utils import get_headers
from app.config import settings
from app.logging_config import get_jsonl_logger, build_jsonl_entry


jsonl_logger = get_jsonl_logger()
logger = logging.getLogger(__name__)
router = APIRouter()


def safe(value):
    """Convert None to empty string, otherwise return string representation"""
    if value is None:
        return ""
    return str(value).strip() if isinstance(value, str) else str(value)


# Helper: Parse Unleashed date format
def parse_date_unleashed(date_str):
    """
    Unleashed dates look like: "/Date(1685328000000)/"
    """
    if not date_str:
        return None
    try:
        if isinstance(date_str, str) and date_str.startswith("/Date("):
            ts = int(date_str[6:-2]) / 1000
            return datetime.datetime.fromtimestamp(ts)
    except (ValueError, IndexError):
        pass
    return None


# Helper: Compute invoice metrics for a customer
def compute_invoice_metrics(invoices):
    """Calculate invoice metrics (balance, highest amounts, payment counts, dates)"""
    current_balance = Decimal("0.00")
    highest_invoice = Decimal("0.00")
    highest_outstanding = Decimal("0.00")
    total_paid = 0
    last_sale_date = None
    last_payment_date = None

    for inv in invoices:
        try:
            total = Decimal(str(inv.get("Total", 0)))
            paid = Decimal(str(inv.get("AmountPaid", 0)))
            outstanding = total - paid

            current_balance += outstanding

            if total > highest_invoice:
                highest_invoice = total

            if outstanding > highest_outstanding:
                highest_outstanding = outstanding

            if paid >= total:
                total_paid += 1

            dt_inv = parse_date_unleashed(inv.get("InvoiceDate"))
            if dt_inv and (not last_sale_date or dt_inv > last_sale_date):
                last_sale_date = dt_inv

            dt_pay = parse_date_unleashed(inv.get("LastPaymentDate"))
            if dt_pay and (not last_payment_date or dt_pay > last_payment_date):
                last_payment_date = dt_pay
        except Exception as e:
            logger.warning(f"Error processing invoice metrics: {str(e)}")
            continue

    return {
        "CurrentBalance": float(current_balance),
        "HighestInvoiceAmount": float(highest_invoice),
        "HighestReceivableAmount": float(highest_outstanding),
        "TotalPaidInvoices": total_paid,
        "LastSaleDate": last_sale_date,
        "LastPaymentDate": last_payment_date
    }



def fetch_customers_from_unleashed():
    all_customers = []
    page_number = 1  # Unleashed pages start at 1
    page_size = 1000

    try:
        while True:
            logger.info(f"Current PageNumber: {page_number}")
            query_string = f"PageSize={page_size}"
            url_with_page = f"{settings.BASE_URL}/Customers/{page_number}"

            response = requests.get(
                url_with_page,
                headers=get_headers(query_string=query_string),
                params={
                    # "pageNumber": page_number,
                    "PageSize": page_size,
                }
            )

            if response.status_code != 200:
                logger.error(f"Error fetching customers: {response.text}")
                break

            data = response.json()

            if "Items" not in data or not data["Items"]:
                break

            logger.info(f"Starting 5 customers on page_number: {page_number}: {[item['CustomerCode'] for item in data['Items'][:5]]}")

            all_customers.extend(data["Items"])

            pagination = data.get("Pagination", {})
            total_pages = pagination.get("NumberOfPages", 1)

            logger.info(f"Fetched page {page_number}/{total_pages} — {len(data['Items'])} customers")

            if page_number >= total_pages:
                break

            page_number += 1

        logger.info(f"Total customers fetched: {len(all_customers)}")
        return all_customers

    except Exception as e:
        logger.error(f"Exception fetching customers from Unleashed: {str(e)}")
        raise

def fetch_invoices_from_unleashed():
    """Fetch all invoices from Unleashed API with pagination"""
    all_invoices = []
    page_number = 1
    page_size = 1000

    try:
        while True:
            query_string = f"pageSize={page_size}"
            invoices_url = f"{settings.BASE_URL}/Invoices/{page_number}"

            response = requests.get(
                invoices_url,
                headers=get_headers(query_string=query_string),
                params={
                    "pageSize": page_size,
                }
            )

            if response.status_code != 200:
                logger.error(f"Error fetching invoices: {response.text}")
                break

            data = response.json()

            if "Items" not in data or not data["Items"]:
                break

            all_invoices.extend(data["Items"])

            pagination = data.get("Pagination", {})
            total_pages = pagination.get("NumberOfPages", 1)

            logger.info(f"Fetched page {page_number}/{total_pages} — {len(data['Items'])} invoices")

            if page_number >= total_pages:
                break

            page_number += 1

        logger.info(f"Total invoices fetched: {len(all_invoices)}")
        return all_invoices

    except Exception as e:
        logger.error(f"Exception fetching invoices from Unleashed: {str(e)}")
        return []

def get_shipping_address(unleashed_customer):
    addresses = unleashed_customer.get("Addresses", [])
    
    for addr in addresses:
        if addr.get("IsDefault"):
            return addr

    return addresses[0] if addresses else {}

def map_unleashed_to_tcustomer(unleashed_customer, metrics=None):
    """
    Map Unleashed customer data to TCustomers model
    Includes invoice metrics (balance, payment info, etc.)
    """
    if metrics is None:
        metrics = {
            "CurrentBalance": 0.0,
            "HighestInvoiceAmount": 0.0,
            "HighestReceivableAmount": 0.0,
            "TotalPaidInvoices": 0,
            "LastSaleDate": None,
            "LastPaymentDate": None
        }

    shipping = get_shipping_address(unleashed_customer)

    name = safe(unleashed_customer.get("CustomerName", ""))

    first_name = name.split()[0] if name else ""
    last_name = name.split()[-1] if name else ""

    return TCustomers(

        CustomerCode=safe(unleashed_customer.get("CustomerCode", "")),
        CardRecordID=0,
        CardIdentification=safe(unleashed_customer.get("CustomerCode", "")),
        Name=safe(unleashed_customer.get("CustomerName", "")),
        LastName=safe(unleashed_customer.get("CustomerName", "").split()[-1] if unleashed_customer.get("CustomerName") else ""),
        FirstName=safe(unleashed_customer.get("CustomerName", "").split()[0] if unleashed_customer.get("CustomerName") else ""),
        IsIndividual="N",  # Default to non-individual
        IsInactive="N",
        Notes=safe(unleashed_customer.get("Comments", "").strip()),
        IdentifierID=safe(unleashed_customer.get("Guid", "")),
        CustomField1=safe(unleashed_customer.get("CustomerName", "")),

        CustomField2=safe(unleashed_customer.get("DeliveryMethod","")),

        CustomField3=safe(unleashed_customer.get("SalesOrderGroup","")),

        TermsID=0,
        ABN=safe(unleashed_customer.get("ABN", "").strip()),
        ABNBranch="",

        PriceLevelID="",

        TaxIDNumber=safe(unleashed_customer.get("GSTVATNumber"))[:19],

        TaxCodeID=0,

        FreightTaxCodeID=0,

        UseCustomerTaxCode="N",

        CreditLimit=float(unleashed_customer.get("CreditLimit") or 0),

        VolumeDiscount=float(unleashed_customer.get("DiscountRate") or 0),

        # Invoice Metrics
        CurrentBalance=metrics.get("CurrentBalance", 0.0),

        TotalDeposits=0.0,

        TotalReceivableDays=0,

        TotalPaidInvoices=metrics.get("TotalPaidInvoices", 0),

        HighestInvoiceAmount=metrics.get("HighestInvoiceAmount", 0.0),

        HighestReceivableAmount=metrics.get("HighestReceivableAmount", 0.0),

        PaymentCardNumber="",

        PaymentNameOnCard="",

        PaymentBankAccountName=safe(unleashed_customer.get("BankName"))[:32],

        PaymentNotes="",

        HourlyBillingRate=0.0,

        SaleLayoutID="",

        PrintedForm="",

        ChangeControl=str(unleashed_customer.get("LastModifiedOn"))[:20],

        CurrencyID=None,

        Picture=None,

        Identifiers=safe(unleashed_customer.get("CustomerCode"))[:26],

        CustomList1ID=None,

        CustomList2ID=None,

        CustomList3ID=None,

        CustomerSince=None,

        LastSaleDate=metrics.get("LastSaleDate"),

        LastPaymentDate=metrics.get("LastPaymentDate"),

        MethodOfPaymentID=None,

        PaymentExpirationDate=None,

        PaymentBSB=safe(unleashed_customer.get("BankBranch"))[:11],

        PaymentBankAccountNumber=safe(unleashed_customer.get("BankAccount"))[:20],

        IncomeAccountID=None,

        SalespersonID=None,

        SaleCommentID=None,

        ShippingMethodID=None,

        GSTIDNumber=safe(unleashed_customer.get("GSTVATNumber"))[:20],

        ReceiptMemo=safe(unleashed_customer.get("Notes"))[:255],

        PaymentBankBranch=safe(unleashed_customer.get("BankBranch"))[:10],

        PaymentAddress=safe(shipping.get("StreetAddress"))[:30],

        PaymentZIP=safe(shipping.get("PostalCode"))[:10],

        PaymentCardVerification="",

        ACCNO=None,

        ONHOLD="Y" if unleashed_customer.get("StopCredit") else "N",
    )



# FastAPI Endpoint: Sync customers from Unleashed to SQL database
@router.post("/import-customers-from-unleashed")
async def import_customers_from_unleashed(session: AsyncSession = Depends(get_async_session)):
    """
    Sync all customers from Unleashed API with database:
    - Import new customers
    - Update existing customers if changed
    - Delete customers no longer present in Unleashed
    Includes invoice metrics (balance, payment info, etc.)
    Returns summary of imported, updated, and deleted customers.
    """
    try:
        logger.info("Starting sync of customers from Unleashed...")
        
        # Fetch all customers from Unleashed
        unleashed_customers = fetch_customers_from_unleashed()
        
        if not unleashed_customers:
            logger.warning("No customers found in Unleashed API")
            return {
                "status": "success",
                "message": "No customers found in Unleashed API",
                "imported_count": 0,
                "updated_count": 0,
                "deleted_count": 0
            }
        
        logger.info(f"Found {len(unleashed_customers)} customers in Unleashed")
        
        # Fetch all invoices for metrics
        logger.info("Fetching invoices for metrics calculation...")
        unleashed_invoices = fetch_invoices_from_unleashed()
        
        # Group invoices by customer code
        invoice_map = {}
        for inv in unleashed_invoices:
            try:
                customer_info = inv.get("Customer", {})
                customer_code = customer_info.get("CustomerCode")
                if customer_code:
                    invoice_map.setdefault(customer_code, []).append(inv)
            except Exception as e:
                logger.warning(f"Error processing invoice: {str(e)}")
                continue
        
        logger.info(f"Grouped {len(unleashed_invoices)} invoices across {len(invoice_map)} customers")
        
        # Fetch all existing customers from database
        logger.info("Fetching existing customers from database...")
        existing_customers_result = await session.execute(select(TCustomers))
        existing_customers = existing_customers_result.scalars().all()
        logger.info(f"Found {len(existing_customers)} existing customers in database")
        
        # Create maps for quick lookup using CardIdentification
        existing_by_identification = {cust.CardIdentification: cust for cust in existing_customers}
        unleashed_codes = {cust.get("CustomerCode") for cust in unleashed_customers}
        
        imported_count = 0
        updated_count = 0
        failed_count = 0
        deleted_count = 0
        errors = []
        
        # Process each Unleashed customer
        for unleashed_customer in unleashed_customers:
            try:
                customer_code = unleashed_customer.get("CustomerCode")
                
                # Get invoices for this customer
                customer_invoices = invoice_map.get(customer_code, [])
                
                # Compute metrics from invoices
                metrics = compute_invoice_metrics(customer_invoices)
                logger.info(f"Computed metrics for customer {customer_code}: {len(customer_invoices)} invoices, balance: {metrics['CurrentBalance']}")
                
                # Map Unleashed customer to TCustomers model with metrics
                new_customer = map_unleashed_to_tcustomer(unleashed_customer, metrics)
                
                if customer_code in existing_by_identification:
                    # Customer exists - check if update is needed
                    existing_customer = existing_by_identification[customer_code]
                    
                    # Compare all relevant fields from mapping
                    fields_to_compare = [
                        'CustomerCode', 'CardIdentification', 'Name', 'LastName', 'FirstName',
                        'IsIndividual', 'IsInactive', 'Notes', 'IdentifierID', 'CustomField1',
                        'CustomField2', 'CustomField3', 'ABN', 'ABNBranch', 'PriceLevelID',
                        'TaxIDNumber', 'UseCustomerTaxCode', 'CreditLimit', 'VolumeDiscount',
                        'CurrentBalance', 'TotalDeposits', 'TotalReceivableDays', 'TotalPaidInvoices',
                        'HighestInvoiceAmount', 'HighestReceivableAmount', 'PaymentCardNumber',
                        'PaymentNameOnCard', 'PaymentBankAccountName', 'PaymentNotes', 'HourlyBillingRate',
                        'SaleLayoutID', 'PrintedForm', 'Identifiers', 'CustomerSince', 'LastSaleDate',
                        'LastPaymentDate', 'MethodOfPaymentID', 'PaymentExpirationDate', 'PaymentBSB',
                        'PaymentBankAccountNumber', 'IncomeAccountID', 'SalespersonID', 'SaleCommentID',
                        'ShippingMethodID', 'GSTIDNumber', 'ReceiptMemo', 'PaymentBankBranch',
                        'PaymentAddress', 'PaymentZIP', 'PaymentCardVerification', 'ACCNO', 'ONHOLD'
                    ]
                    
                    changed = False
                    for attr in fields_to_compare:
                        if getattr(existing_customer, attr, None) != getattr(new_customer, attr, None):
                            changed = True
                            logger.debug(f"Customer {customer_code} field {attr} changed: {getattr(existing_customer, attr, None)} -> {getattr(new_customer, attr, None)}")
                            break
                    
                    if changed:
                        # Update existing customer with new data
                        for attr in fields_to_compare + ['ChangeControl']:
                            setattr(existing_customer, attr, getattr(new_customer, attr, None))
                        
                        updated_count += 1
                        logger.info(f"Updated customer {customer_code}")
                    else:
                        logger.info(f"Customer {customer_code} unchanged, no update needed")
                else:
                    # Customer doesn't exist - insert new
                    session.add(new_customer)
                    imported_count += 1
                    logger.info(f"Prepared new customer {customer_code} for import")
                
            except Exception as e:
                failed_count += 1
                error_msg = f"Error processing customer {unleashed_customer.get('CustomerCode', 'Unknown')}: {str(e)}"
                jsonl_logger.info(build_jsonl_entry(
                    action_type="Sync Customers from Unleashed to SQL",
                    action_variant="sync-customers-from-unleashed",
                    status="Error",
                    message=error_msg,
                ))
                logger.error(error_msg)
                errors.append(error_msg)
        
        # Delete customers that are in database but not in Unleashed
        logger.info("Checking for deleted customers...")
        for existing_customer in existing_customers:
            if existing_customer.CardIdentification not in unleashed_codes:
                try:
                    await session.delete(existing_customer)
                    deleted_count += 1
                    logger.info(f"Marked for deletion: customer {existing_customer.CardIdentification} (no longer in Unleashed)")
                except Exception as e:
                    error_msg = f"Error deleting customer {existing_customer.CardIdentification}: {str(e)}"
                    jsonl_logger.info(build_jsonl_entry(
                        action_type="Sync Customers from Unleashed to SQL",
                        action_variant="sync-customers-from-unleashed",
                        status="Error",
                        message=error_msg,
                    ))
                    logger.error(error_msg)
                    errors.append(error_msg)
        
        # Commit all changes to database
        await session.commit()
        
        logger.info(f"Sync complete - Imported: {imported_count}, Updated: {updated_count}, Deleted: {deleted_count}, Failed: {failed_count}")
        jsonl_logger.info(build_jsonl_entry(
            action_type="Sync Customers from Unleashed to SQL",
            action_variant="sync-customers-from-unleashed",
            status="Success",
            message=f"Sync completed: {imported_count} imported, {updated_count} updated, {deleted_count} deleted, {failed_count} failed.",
        ))
        
        return {
            "status": "success",
            "message": f"Sync completed: {imported_count} new, {updated_count} updated, {deleted_count} deleted",
            "imported_count": imported_count,
            "updated_count": updated_count,
            "deleted_count": deleted_count,
            "failed_count": failed_count,
            "invoices_processed": len(unleashed_invoices),
            "errors": errors if errors else []
        }
        
    except Exception as e:
        jsonl_logger.info(build_jsonl_entry(
            action_type="Sync Customers from Unleashed to SQL",
            action_variant="sync-customers-from-unleashed",
            status="Error",
            message=f"Error syncing customers: {str(e)}",
        ))
        logger.error(f"Error syncing customers: {str(e)}")
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error syncing customers: {str(e)}"
        )

