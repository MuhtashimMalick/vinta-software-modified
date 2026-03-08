# app/routers/unleashed.py

import logging
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
import requests
import base64
import hashlib
import hmac
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import  get_async_session
from app.models import (
    TRICGPDAMobileSalesHeader,
    TRICGPDAMobileSalesOrdersLine,
    TREMOTETransCustomer,
    TREMOTETransSaleLines,
    TREMOTETransHeader,
    TREMOTETransSaleTenders,
    TREMOTETransSaleLineSerials,
    TCustomers,
    TTaxCodes,
    TShippingMethods
)
import datetime
from decimal import Decimal

# Get logger
logger = logging.getLogger(__name__)
router = APIRouter()

API_ID = "e1242a87-6f65-4d90-b931-0437f793f7c1"
API_KEY = "3W1MHYwXaDR2iYOQ853Mbs9Ccf5N8khCOIkTWLMEmSIN7k5Z4oowvZMpz4onZQS3nDrJhYTdher8sPB3K4yw=="
BASE_URL = "https://api.unleashedsoftware.com/Customers"


def generate_signature(api_key, query_string=""):
    message = query_string.encode("utf-8")
    secret = api_key.encode("utf-8")
    signature = hmac.new(secret, message, hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

def get_headers(query_string=""):
    return {
        "api-auth-id": API_ID,
        "api-auth-signature": generate_signature(API_KEY, query_string),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


# Helper: convert None → ""
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



# Call Unleashed API
def send_to_unleashed(payload):
    """Send POST request to Unleashed API"""
    signature = generate_signature(BASE_URL)

    headers = {
        "api-auth-id": API_ID,
        "api-auth-signature": signature,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    print("====== PAYLOAD SENT ======")
    print(json.dumps(payload, indent=2))

    response = requests.post(
        BASE_URL,
        headers=headers,
        json=payload
    )

    print("====== RESPONSE ======")
    print(response.text)

    return response


# Fetch customers from Unleashed API
def fetch_customers_from_unleashed():
    """Fetch all customers from Unleashed API with pagination"""
    signature = generate_signature(BASE_URL)

    headers = {
        "api-auth-id": API_ID,
        "api-auth-signature": signature,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    all_customers = []
    page_number = 0
    
    try:
        while True:
            # Unleashed uses pagination with pageNumber parameter
            url_with_page = f"{BASE_URL}"
            # signature = base64.b64encode(
            #     hmac.new(
            #         API_KEY.encode("utf-8"),
            #         url_with_page.encode("utf-8"),
            #         hashlib.sha256
            #     ).digest()
            # ).decode()
            
            # headers["api-auth-signature"] = signature

            response = requests.get(url_with_page, headers=get_headers())

            if response.status_code != 200:
                logger.error(f"Error fetching customers: {response.text}")
                break

            data = response.json()
            
            # Check if we have customers in this page
            if "Items" not in data or not data["Items"]:
                break

            all_customers.extend(data["Items"])
            
            # Check if there are more pages
            if not data.get("HasMorePages", False):
                break
                
            page_number += 1

        return all_customers

    except Exception as e:
        logger.error(f"Exception fetching customers from Unleashed: {str(e)}")
        raise


# Fetch invoices from Unleashed API
def fetch_invoices_from_unleashed():
    """Fetch all invoices from Unleashed API with pagination"""
    invoices_url = "https://api.unleashedsoftware.com/Invoices"
    all_invoices = []
    page_number = 0
    
    try:
        while True:
            headers = get_headers()

            response = requests.get(invoices_url, headers=headers)

            if response.status_code != 200:
                logger.error(f"Error fetching invoices: {response.text}")
                break

            data = response.json()
            
            # Check if we have invoices in this page
            if "Items" not in data or not data["Items"]:
                break

            all_invoices.extend(data["Items"])
            
            # Check if there are more pages
            if not data.get("HasMorePages", False):
                break
                
            page_number += 1

        logger.info(f"Fetched {len(all_invoices)} invoices from Unleashed")
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
        # Required fields - using safe() to handle None
        # CustomerID=00,
        CustomerCode=safe(unleashed_customer.get("CustomerCode", "")),
        CardRecordID=0,
        CardIdentification=safe(unleashed_customer.get("CustomerCode", "")),
        Name=safe(unleashed_customer.get("CustomerName", "")),
        LastName=safe(unleashed_customer.get("CustomerName", "").split()[-1] if unleashed_customer.get("CustomerName") else ""),
        FirstName=safe(unleashed_customer.get("CustomerName", "").split()[0] if unleashed_customer.get("CustomerName") else ""),
        IsIndividual="N",  # Default to non-individual
        IsInactive="N",
        Notes=safe(unleashed_customer.get("Comments", "")),
        IdentifierID=safe(unleashed_customer.get("Guid", "")),
        CustomField1="",

        CustomField2="",

        CustomField3="",

        TermsID=0,
        ABN=safe(unleashed_customer.get("ABN", "")),
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

# def map_unleashed_to_tcustomer(unleashed_customer: dict) -> TCustomers:
#     """
#     Map Unleashed customer data to TCustomers model
#     All missing fields default to empty string or 0
#     """
#     return TCustomers(
#         # Required fields - using safe() to handle None
#         # CustomerID=00,
#         CustomerCode=safe(unleashed_customer.get("CustomerCode", "")),
#         CardRecordID=0,
#         CardIdentification=safe(unleashed_customer.get("CustomerCode", "")),
#         Name=safe(unleashed_customer.get("CustomerName", "")),
#         LastName=safe(unleashed_customer.get("CustomerName", "").split()[-1] if unleashed_customer.get("CustomerName") else ""),
#         FirstName=safe(unleashed_customer.get("CustomerName", "").split()[0] if unleashed_customer.get("CustomerName") else ""),
#         IsIndividual="N",  # Default to non-individual
#         IsInactive="N",
#         Notes=safe(unleashed_customer.get("Comments", "")),
#         IdentifierID=safe(unleashed_customer.get("CustomerCode", "")),
#         CustomField1="",
#         CustomField2="",
#         CustomField3="",
#         TermsID=0,
#         ABN=safe(unleashed_customer.get("ABN", "")),
#         ABNBranch="",
#         PriceLevelID="",
#         TaxIDNumber=safe(unleashed_customer.get("TaxNumber", "")),
#         TaxCodeID=0,
#         FreightTaxCodeID=0,
#         UseCustomerTaxCode="N",
#         CreditLimit=0.0,
#         VolumeDiscount=0.0,
#         CurrentBalance=0.0,
#         TotalDeposits=0.0,
#         TotalReceivableDays=0,
#         TotalPaidInvoices=0,
#         HighestInvoiceAmount=0.0,
#         HighestReceivableAmount=0.0,
#         PaymentCardNumber="",
#         PaymentNameOnCard="",
#         PaymentBankAccountName="",
#         PaymentNotes="",
#         HourlyBillingRate=0.0,
#         SaleLayoutID="",
#         PrintedForm="",
#         ChangeControl="",
#         # Optional fields
#         CurrencyID=None,
#         Picture=None,
#         Identifiers=safe(unleashed_customer.get("CustomerCode", "")),
#         CustomList1ID=None,
#         CustomList2ID=None,
#         CustomList3ID=None,
#         CustomerSince=None,
#         LastSaleDate=None,
#         LastPaymentDate=None,
#         MethodOfPaymentID=None,
#         PaymentExpirationDate=None,
#         PaymentBSB=safe(unleashed_customer.get("BankBSB", "")),
#         PaymentBankAccountNumber=safe(unleashed_customer.get("BankAccountNumber", "")),
#         IncomeAccountID=None,
#         SalespersonID=None,
#         SaleCommentID=None,
#         ShippingMethodID=None,
#         GSTIDNumber=safe(unleashed_customer.get("TaxNumber", "")),
#         ReceiptMemo=safe(unleashed_customer.get("Comments", "")),
#         PaymentBankBranch=safe(unleashed_customer.get("BankBranch", "")),
#         PaymentAddress=safe(unleashed_customer.get("DeliveryStreetAddress", "")),
#         PaymentZIP=safe(unleashed_customer.get("DeliveryPostalCode", "")),
#         PaymentCardVerification="",
#         ACCNO=None,
#         ONHOLD="N"
#     )
# FastAPI Endpoint: Export customer to Unleashed



# FastAPI Endpoint: Import all customers from Unleashed to SQL database
@router.post("/import-customers-from-unleashed")
async def import_customers_from_unleashed(session: AsyncSession = Depends(get_async_session)):
    """
    Fetch all customers from Unleashed API and store them in TCustomers table.
    Includes invoice metrics (balance, payment info, etc.)
    Returns summary of imported customers.
    """
    try:
        logger.info("Starting import of customers from Unleashed...")
        
        # Fetch all customers from Unleashed
        unleashed_customers = fetch_customers_from_unleashed()
        
        if not unleashed_customers:
            logger.warning("No customers found in Unleashed API")
            return {
                "status": "success",
                "message": "No customers found in Unleashed API",
                "imported_count": 0
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
        
        imported_count = 0
        failed_count = 0
        errors = []
        
        for unleashed_customer in unleashed_customers:
            try:
                customer_code = unleashed_customer.get("CustomerCode")
                
                # Get invoices for this customer
                customer_invoices = invoice_map.get(customer_code, [])
                
                # Compute metrics from invoices
                metrics = compute_invoice_metrics(customer_invoices)
                logger.info(f"Computed metrics for customer {customer_code}: {len(customer_invoices)} invoices, balance: {metrics['CurrentBalance']}")
                
                # Map Unleashed customer to TCustomers model with metrics
                customer = map_unleashed_to_tcustomer(unleashed_customer, metrics)
                
                # Add to session
                session.add(customer)
                imported_count += 1
                
                logger.info(f"Prepared customer {customer.CardIdentification} for import")
                
            except Exception as e:
                failed_count += 1
                error_msg = f"Error importing customer {unleashed_customer.get('CustomerCode', 'Unknown')}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        # Commit all changes to database
        await session.commit()
        
        logger.info(f"Successfully imported {imported_count} customers to SQL database")
        
        return {
            "status": "success",
            "message": f"Successfully imported {imported_count} out of {len(unleashed_customers)} customers with metrics",
            "imported_count": imported_count,
            "failed_count": failed_count,
            "invoices_processed": len(unleashed_invoices),
            "errors": errors if errors else []
        }
        
    except Exception as e:
        logger.error(f"Error importing customers: {str(e)}")
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error importing customers: {str(e)}"
        )


# FastAPI Endpoint: Get customer data from Unleashed (returns raw data)
@router.get("/get-customers-from-unleashed")
async def get_customers_from_unleashed():
    """
    Fetch all customers from Unleashed API and return raw data.
    Useful for debugging and seeing what fields are available.
    """
    try:
        logger.info("Fetching customers from Unleashed API...")
        
        customers = fetch_customers_from_unleashed()
        
        return {
            "status": "success",
            "count": len(customers),
            "customers": customers[0]
        }
        
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching customers from Unleashed: {str(e)}"
        )