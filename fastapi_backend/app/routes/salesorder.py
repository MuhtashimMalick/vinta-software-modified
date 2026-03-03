# app/routers/unleashed.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import requests
import base64
import hashlib
import hmac
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import  get_async_session
from app.models import TRICGPDAMobileSalesHeader, TRICGPDAMobileSalesOrdersLine,TREMOTETransCustomer,TREMOTETransSaleLines
import datetime
router = APIRouter()

API_ID = "e1242a87-6f65-4d90-b931-0437f793f7c1"
API_KEY = "3W1MHYwXaDR2iYOQ853Mbs9Ccf5N8khCOIkTWLMEmSIN7k5Z4oowvZMpz4onZQS3nDrJhYTdher8sPB3K4yw=="
BASE_URL = "https://api.unleashedsoftware.com/SalesOrders"


# ==============================
# AUTH
# ==============================

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


# ==============================
# ENDPOINT
# ==============================
from sqlalchemy import select

# @router.post("/export-sales-orders")
# async def export_sales_orders(db: AsyncSession = Depends(get_async_session)):

#     result = await db.execute(
#         select(TRICGPDAMobileSalesHeader)
#         .filter(TRICGPDAMobileSalesHeader.exported == 0)
#         .limit(1)
#     )
#     headers = result.scalars().all()

#     if not headers:
#         return {"message": "No unexported sales orders found"}

#     results = []

#     for header in headers:
#         lines_result = await db.execute(
#             select(TRICGPDAMobileSalesOrdersLine)
#             .filter(TRICGPDAMobileSalesOrdersLine.salesorder_id == header.salesorder_id)
#         )
#         lines = lines_result.scalars().all()

#         sales_order_lines = []
#         sub_total = 0
#         tax_total = 0
#         line_number = 1

#         for line in lines:
#             quantity = float(line.quantity)
#             unit_price = float(line.sell_ex)
#             tax_rate = 0.1

#             line_total = quantity * unit_price
#             line_tax = line_total * tax_rate
#             sub_total += line_total
#             tax_total += line_tax

#             sales_order_lines.append({
#                 "LineNumber": line_number,
#                 "Product": {"ProductCode": 101},#line.stock_id
#                 "OrderQuantity": quantity,
#                 "UnitPrice": unit_price,
#                 "LineTotal": round(line_total, 8),
#                 "TaxRate": round(tax_rate, 6),
#                 "LineTax": round(line_tax, 3)
#             })
#             line_number += 1

#         total = sub_total + tax_total

#         payload = {
#             "OrderNumber": header.salesorder_id,
#             "OrderDate": header.salesorder_date.strftime("%Y-%m-%d"),
#             "RequiredDate": header.expiry_date.strftime("%Y-%m-%d") if header.expiry_date else header.salesorder_date.strftime("%Y-%m-%d"),
#             "OrderStatus": "Completed" if header.status == 1 else "Parked",
#             "Customer": {"CustomerCode": "1ALEX"},  #header.customer_id
#             "Warehouse": {"WarehouseCode": "BR"},   #cant find in sql,in unleashed it is amde form setitngs
#             "Currency": {"CurrencyCode": "AUD"},    #currency only capital A written (Remotetranssalelines)
#             "ExchangeRate": 1,
#             "Tax": {
#                 "TaxCode": "G.S.T.", #tax present in sql but cant understand the maoping
#                 "TaxRate": 0.1
#             },
#             "TaxRate": 0.1,
#             "SubTotal": round(sub_total, 3),
#             "TaxTotal": round(tax_total, 3),
#             "Total": round(total, 3),
#             "SalesOrderLines": sales_order_lines,
#             "Comments": header.comments
#         }

#         response = requests.post(BASE_URL, headers=get_headers(), json=payload, timeout=30)

#         if response.status_code == 201:
#             header.exported = 1
#             await db.commit()
#             results.append({"order_id": header.salesorder_id, "status": "exported"})
#         else:
#             results.append({
#                 "order_id": header.salesorder_id,
#                 "status": "failed",
#                 "error": response.text
#             })

#     return {"processed": len(results), "results": results}





@router.post("/export-sales-orders")
async def export_sales_orders(db: AsyncSession = Depends(get_async_session)):

    # Get 1 unsent transaction header
    result = await db.execute(
        select(TREMOTETransCustomer)
        # .where(
        #     (TREMOTETransCustomer.Sent2Host == None) |
        #     (TREMOTETransCustomer.Sent2Host != 'Y')
        # )
        .limit(1)
    )

    headers = result.scalars().all()

    if not headers:
        return {"message": "No unexported sales orders found"}

    results = []

    for header in headers:

        # Fetch matching sale lines
        lines_result = await db.execute(
            select(TREMOTETransSaleLines).where(
                TREMOTETransSaleLines.Company_ID == header.Company_ID,
                TREMOTETransSaleLines.StoreCode == header.StoreCode,
                TREMOTETransSaleLines.PostingDate == header.PostingDate,
                TREMOTETransSaleLines.TransID == header.TransID,
            )
        )

        lines = lines_result.scalars().all()

        if not lines:
            continue

        sales_order_lines = []
        sub_total = 0
        tax_total = 0

        for idx, line in enumerate(lines, start=1):

            quantity = float(line.SaleQty)
            unit_price_inc = float(line.SaleUnitAmountIncTax)
            tax_rate = float(line.SaleTaxRate) / 100  # if stored as 10.00

            # Convert inclusive price → exclusive
            unit_price_ex = unit_price_inc / (1 + tax_rate)
            line_total = quantity * unit_price_ex
            line_tax = (quantity * unit_price_inc) - line_total

            sub_total += line_total
            tax_total += line_tax

            sales_order_lines.append({
                "LineNumber": idx,
                "Product": {
                    "ProductCode": 101 #line.SKU.strip()
                },
                "OrderQuantity": quantity,
                "UnitPrice": round(unit_price_ex, 6),
                "LineTotal": round(line_total, 6),
                "TaxRate": round(tax_rate, 6),
                "LineTax": round(line_tax, 6)
            })

        total = sub_total + tax_total

        payload = {
            "OrderNumber": header.TransID.strip(),
            "OrderDate": header.PostingDate.strftime("%Y-%m-%d"),
            "RequiredDate": header.PostingDate.strftime("%Y-%m-%d"),
            "OrderStatus": "Completed",
            "Customer": {"CustomerCode": "1ALEX"},  #header.customer_id
            "Warehouse": {"WarehouseCode": "GOS"},   #cant find in sql,in unleashed it is amde form setitngs
            "Currency": {"CurrencyCode": "AUD"},    #currency only capital A written (Remotetranssalelines)
            # "Customer": {
            #     "CustomerCode": header.AccountCode.strip() if header.AccountCode else "CASH"
            # },
            # "Warehouse": {
            #     "WarehouseCode": header.StoreCode.strip()
            # },
            # "Currency": {
            #     "CurrencyCode": lines[0].CurrencyCode.strip() if lines[0].CurrencyCode else "AUD"
            # },
            "ExchangeRate": 1,
            "Tax": {
                "TaxCode": "G.S.T.",
                "TaxRate": round(float(lines[0].SaleTaxRate) / 100, 6)
            },
            "TaxRate": round(float(lines[0].SaleTaxRate) / 100, 6),
            "SubTotal": round(sub_total, 3),
            "TaxTotal": round(tax_total, 3),
            "Total": round(total, 3),
            "SalesOrderLines": sales_order_lines,
            "Comments": header.Name.strip() if header.Name else None
        }

        try:
            response = requests.post(
                BASE_URL,
                headers=get_headers(),
                json=payload,
                timeout=30
            )

            if response.status_code == 201:

                # Mark header as sent
                header.Sent2Host = 'Y'
                header.Sent2HostDateTime = datetime.datetime.utcnow()

                # Mark all lines as sent
                for line in lines:
                    line.Sent2Host = 'Y'
                    line.Sent2HostDateTime = datetime.datetime.utcnow()

                await db.commit()

                results.append({
                    "order_id": header.TransID.strip(),
                    "status": "exported"
                })

            else:
                results.append({
                    "order_id": header.TransID.strip(),
                    "status": "failed",
                    "error": response.text
                })

        except Exception as e:
            results.append({
                "order_id": header.TransID.strip(),
                "status": "error",
                "error": str(e)
            })

    return {
        "processed": len(results),
        "results": results
    }