# app/routers/unleashed.py
import datetime
import logging
import requests

from defusedxml import ElementTree as ET
from dateutil import parser as dateutil_parser
from decimal import Decimal

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import  get_async_session
from app.config import settings
from app.models import (
    TREMOTETransCustomer,
    TREMOTETransSaleLines,
    TREMOTETransHeader,
    TREMOTETransSaleTenders,
    TREMOTETransSaleLineSerials,
    TCustomers,
    TTaxCodes,
    TShippingMethods
)
from app.utils import get_headers


# Get logger
logger = logging.getLogger(__name__)
router = APIRouter()

####################RIGCG PDA SALES ORDER VERSION
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



#REMOTE TRANSHEADER,CUSTOMER,SALESLINE VERSION
# WAREHOUSE_MAP = {
#     60: "W1",
#     2: "BR",
#     3: "GOS",
#     4: "NQ",
#     5: "TH",
#     6: "VIC",
#     7: "SOU",
#     8: "IL",
# }
@router.post("/export-sales-orders")
async def export_sales_orders(db: AsyncSession = Depends(get_async_session)):
    try:
        # Find one unsent header (Sent2Host is NULL or != 'Y')
        result = await db.execute(
            select(TREMOTETransHeader).where(
                (TREMOTETransHeader.Sent2Host == None) 
                | (TREMOTETransHeader.Sent2Host == 'Y')
            ).limit(1)
        )

        headers = result.scalars().all()
        logger.debug(f"Found {len(headers)} unsent headers")
        if not headers:
            logger.info("No unexported sales orders found")
            return {"message": "No unexported sales orders found"}

        results = []

        for header in headers:

            # fetch customer record for this transaction
            cust_result = await db.execute(
                select(TREMOTETransCustomer).where(
                    TREMOTETransCustomer.Company_ID == header.Company_ID,
                    TREMOTETransCustomer.StoreCode == header.StoreCode,
                    # TREMOTETransCustomer.PostingDate == header.PostingDate,
                    TREMOTETransCustomer.TransID == header.TransID,
                ).limit(1)
            )
            cust = cust_result.scalars().first()

            # fetch sale lines
            lines_result = await db.execute(
                select(TREMOTETransSaleLines).where(
                    TREMOTETransSaleLines.Company_ID == header.Company_ID,
                    TREMOTETransSaleLines.StoreCode == header.StoreCode,
                    # TREMOTETransSaleLines.PostingDate == header.PostingDate,
                    TREMOTETransSaleLines.TransID == header.TransID,
                )
            )
            lines = lines_result.scalars().all()

            if not lines:
                continue

            # Attempt to find canonical customer record in tCustomers using AccountCode
            tax_code = None
            tax_rate = None
            customer_code = None
            customer_name = None
            shipping_method=None

            if cust:
                customer_name = cust.Name.strip() if cust.Name else None
                # Do NOT map AccountCode to CustomerID. Use CustomerID from the header
                cust_val = header.CustomerID if getattr(header, 'CustomerID', None) else None
                customer_id = cust_val
                # try lookup in tCustomers by CustomerID (acct_val typically numeric)
                try:
                    cust_id = int(cust_val) if cust_val else None
                except Exception:
                    cust_id = None

                if cust_id is not None: #what if cust is not present in the tcustomer table should we return cust not present in our system 
                    tcust_res = await db.execute(select(TCustomers).where(TCustomers.CustomerID == '145').limit(1))
                    tcust = tcust_res.scalars().first()
                    logger.debug(f"Retrieved TCustomer record: {tcust}")
                    if tcust and getattr(tcust, 'TaxCodeID', None) is not None:
                        tax_rec = await db.execute(select(TTaxCodes).where(TTaxCodes.TaxCodeID == tcust.TaxCodeID).limit(1))
                        taxobj = tax_rec.scalars().first()
                        if taxobj:
                            tax_code = taxobj.TaxCode
                            tax_rate = float(taxobj.TaxPercentageRate) if taxobj.TaxPercentageRate is not None else None
                        tcust_delivery_res = await db.execute(select(TShippingMethods).where(TShippingMethods.ShippingMethodID == tcust.ShippingMethodID).limit(1))
                        tcust_delivery = tcust_delivery_res.scalars().first()
                        if tcust_delivery and getattr(tcust_delivery, 'ShippingMethod', None) is not None:
                            shipping_method=tcust_delivery.ShippingMethod
            # Build SalesOrderLines payload
            sales_lines_payload = []
            sub_total = 0.0
            tax_total = 0.0
            for idx, line in enumerate(lines, start=1):
                try:
                    quantity = float(line.SaleQty)
                except Exception:
                    quantity = 0.0

                try:
                    unit_inc = float(line.SaleUnitAmountIncTax) if line.SaleUnitAmountIncTax is not None else 0.0
                except Exception:
                    unit_inc = 0.0

                # determine tax rate for the line: prefer line.SaleTaxRate, fallback to customer tax
                line_tax_rate = None
                try:
                    if line.SaleTaxRate is not None:
                        line_tax_rate = float(line.SaleTaxRate) / 100.0
                    elif tax_rate is not None:
                        line_tax_rate = float(tax_rate)
                    else:
                        line_tax_rate = 0.0
                except Exception:
                    line_tax_rate = 0.0

                unit_ex = unit_inc / (1.0 + line_tax_rate) if (1.0 + line_tax_rate) != 0 else unit_inc
                line_total = quantity * unit_ex #this is the total with tax exclude
                line_tax = (quantity * unit_inc) - line_total  #tax of the line total

                sub_total += line_total
                tax_total += line_tax

                sales_lines_payload.append({
                    "LineNumber": idx,
                    "Product": {
                        "ProductCode": line.SKU.strip() if getattr(line, 'SKU', None) else None
                    },
                    "OrderQuantity": round(quantity, 4),
                    "UnitPrice": round(unit_ex, 4),
                    "LineTotal": round(line_total, 8),
                    "TaxRate": round(line_tax_rate, 6),
                    "LineTax": round(line_tax, 3)
                    # "Guid": None
                })

            total = sub_total + tax_total

            payload = {
                "SalesOrderLines": sales_lines_payload,
                "OrderNumber": header.TransID.strip() if header.TransID else None,
                "OrderDate": header.PostingDate.strftime("%Y-%m-%d") if header.PostingDate else None,
                "RequiredDate": header.PostingDate.strftime("%Y-%m-%d") if header.PostingDate else None,
                "OrderStatus": "Completed" if header.ClosedYN == 'Y' else "Parked", #need to understand this status
                "Customer": {
                    "CustomerCode": '1ETC',
                    # "CustomerName": customer_name
                },
                "Warehouse": {
                    "WarehouseCode": "GOS" #header.TILL.strip() if header.TILL else None          ask them to make correct warehouse codes in unleashed 
                },
                "Currency": {
                    "CurrencyCode": "AUD" #lines[0].CurrencyCode.strip() if getattr(lines[0], 'CurrencyCode', None) else None
                },
                "ExchangeRate": 1,
                #for tax they need to make sure that the sql fields map to the fields present in unleashed
                "Tax": {
                    "TaxCode": "G.S.T.", #tax_code,
                    "TaxRate": 0.1 # round(tax_rate, 6) if tax_rate is not None else (round(float(lines[0].SaleTaxRate) / 100.0, 6) if getattr(lines[0], 'SaleTaxRate', None) is not None else 0.0)
                },
                # "DeliveryContact": cust.PhoneNo1,
                "DeliveryName": cust.ShipToName,
                "DeliveryStreetAddress":cust.Address1,                                    #cust.ShipToAddress1,
                "DeliveryStreetAddress2":cust.Address2,                                   #cust.ShipToAddress2,
                "DeliverySuburb": cust.Suburb,
                "DeliveryPostCode": str(cust.PostCode).strip(),
                "DeliveryMethod":shipping_method,
                # "TaxRate": 0.1,#round(tax_rate, 6) if tax_rate is not None else (round(float(lines[0].SaleTaxRate) / 100.0, 6) if getattr(lines[0], 'SaleTaxRate', None) is not None else 0.0),
                "SubTotal": round(sub_total, 3),
                "TaxTotal": round(tax_total, 3),
                "Total": round(total, 3)
            }
            logger.info(f"Processing sales order | TaxCode: {tax_code} | PostCode: {cust.PostCode}")
            try:
                response = requests.post(
                    f"{settings.BASE_URL}/SalesOrders",
                    headers=get_headers(),
                    json=payload,
                    timeout=30
                )
                logger.debug(f"Unleashed response status: {response.status_code}")
                if response.status_code == 201:
                    # mark header, customer and lines as sent
                    header.Sent2Host = 'Y'
                    header.Sent2HostDateTime = datetime.datetime.utcnow()

                    if cust:
                        cust.Sent2Host = 'Y'
                        cust.Sent2HostDateTime = datetime.datetime.utcnow()

                    for line in lines:
                        line.Sent2Host = 'Y'
                        line.Sent2HostDateTime = datetime.datetime.utcnow()

                    await db.commit()

                    results.append({"order_id": header.TransID.strip(), "status": "exported"})
                else:
                    logger.error(f"Failed to export order: {response.text}")
                    results.append({"order_id": header.TransID.strip(), "status": "failed", "error": response.text})
                logger.debug("Order processing completed")
            except Exception as e:
                logger.exception(f"Exception processing order: {e}")
                results.append({"order_id": header.TransID.strip(), "status": "error", "error": str(e)})
        logger.info(f"Sales order export completed: {len(results)} processed")
        return {"processed": len(results), "results": results}
    except Exception as e:
        logger.exception(f"Critical error in export_sales_orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import-remote-xml", status_code=201)
async def import_remote_xml(xml: str = Body(..., media_type="application/xml"), db: AsyncSession = Depends(get_async_session)):
    try:
        root = ET.fromstring(xml)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid XML: {e}")

    # find header, customer and lines
    header_elem = root.find('.//tREMOTETransHeader')
    if header_elem is None:
        raise HTTPException(status_code=400, detail="Missing tREMOTETransHeader element")

    def text(e, tag):
        c = e.find(tag)
        return c.text.strip() if (c is not None and c.text is not None) else None

    def parse_dt(val):
        if not val:
            return None
        try:
            return dateutil_parser.parse(val)
        except Exception:
            return None

    # map header fields
    company_id = text(header_elem, 'Company_ID')
    store_code = text(header_elem, 'StoreCode')
    posting_date = parse_dt(text(header_elem, 'PostingDate'))
    trans_id = text(header_elem, 'TransID')

    if not (company_id and store_code and posting_date and trans_id):
        raise HTTPException(status_code=400, detail="Header missing required key fields")

    # delete any existing rows for this key
    await db.execute(delete(TREMOTETransSaleLines).where(
        TREMOTETransSaleLines.Company_ID == company_id,
        TREMOTETransSaleLines.StoreCode == store_code,
        TREMOTETransSaleLines.PostingDate == posting_date,
        TREMOTETransSaleLines.TransID == trans_id,
    ))

    await db.execute(delete(TREMOTETransSaleTenders).where(
        TREMOTETransSaleTenders.Company_ID == company_id,
        TREMOTETransSaleTenders.StoreCode == store_code,
        TREMOTETransSaleTenders.PostingDate == posting_date,
        TREMOTETransSaleTenders.TransID == trans_id,
    ))

    await db.execute(delete(TREMOTETransSaleLineSerials).where(
        TREMOTETransSaleLineSerials.Company_ID == company_id,
        TREMOTETransSaleLineSerials.StoreCode == store_code,
        TREMOTETransSaleLineSerials.PostingDate == posting_date,
        TREMOTETransSaleLineSerials.TransID == trans_id,
    ))

    await db.execute(delete(TREMOTETransCustomer).where(
        TREMOTETransCustomer.Company_ID == company_id,
        TREMOTETransCustomer.StoreCode == store_code,
        TREMOTETransCustomer.PostingDate == posting_date,
        TREMOTETransCustomer.TransID == trans_id,
    ))

    await db.execute(delete(TREMOTETransHeader).where(
        TREMOTETransHeader.Company_ID == company_id,
        TREMOTETransHeader.StoreCode == store_code,
        TREMOTETransHeader.PostingDate == posting_date,
        TREMOTETransHeader.TransID == trans_id,
    ))

    # build header model
    header_kwargs = {
        'Company_ID': company_id,
        'StoreCode': store_code,
        'PostingDate': posting_date,
        'TransID': trans_id,
        'TransDate': parse_dt(text(header_elem, 'TransDate')) or posting_date,
        'ClosedYN': text(header_elem, 'ClosedYN'),
        'ClosedBy': text(header_elem, 'ClosedBy'),
        'SaleType': text(header_elem, 'SaleType'),
        'Status': text(header_elem, 'Status'),
        'Cashier': text(header_elem, 'Cashier'),
        'Salesperson': text(header_elem, 'Salesperson'),
        'CustomerID': text(header_elem, 'CustomerID'),
        'Till': text(header_elem, 'Till'),
        'OriginalSaleType': text(header_elem, 'OriginalSaleType'),
        'TransactionTime': parse_dt(text(header_elem, 'TransactionTime')),
        'VoidYN': text(header_elem, 'VoidYN'),
        'VoidedTransID': text(header_elem, 'VoidedTransID'),
        'DeletedTransaction': text(header_elem, 'DeletedTransaction'),
        'Period': int(text(header_elem, 'Period')) if text(header_elem, 'Period') else None,
        'WeekNo': int(text(header_elem, 'WeekNo')) if text(header_elem, 'WeekNo') else None,
        'WeekStartDate': parse_dt(text(header_elem, 'WeekStartDate')),
        'OriginalTransID': text(header_elem, 'OriginalTransID'),
        'Notes': text(header_elem, 'Notes'),
        'Change': Decimal(text(header_elem, 'Change')) if text(header_elem, 'Change') else None,
        'Sent2Host': text(header_elem, 'Sent2Host'),
        'Sent2HostDateTime': parse_dt(text(header_elem, 'Sent2HostDateTime')),
        'DueDate': parse_dt(text(header_elem, 'DueDate')),
        'Special1': text(header_elem, 'Special1'),
        'Special2': text(header_elem, 'Special2'),
        'Special3': text(header_elem, 'Special3'),
    }

    header_obj = TREMOTETransHeader(**header_kwargs)
    db.add(header_obj)

    # customer
    customer_elem = root.find('.//tREMOTETransCustomer')
    if customer_elem is not None:
        cust_kwargs = {
            'Company_ID': company_id,
            'StoreCode': store_code,
            'PostingDate': parse_dt(text(customer_elem, 'PostingDate')) or posting_date,
            'TransID': text(customer_elem, 'TransID') or trans_id,
            'Name': text(customer_elem, 'Name'),
            'Address1': text(customer_elem, 'Address1'),
            'Address2': text(customer_elem, 'Address2'),
            'Suburb': text(customer_elem, 'Suburb'),
            'PostCode': text(customer_elem, 'PostCode'),
            'FaxNo': text(customer_elem, 'FaxNo'),
            'PhoneNo1': text(customer_elem, 'PhoneNo1'),
            'PhoneNo2': text(customer_elem, 'PhoneNo2'),
            'EmailAddress': text(customer_elem, 'EmailAddress'),
            'SalesPerson': text(customer_elem, 'SalesPerson'),
            'ContactName1': text(customer_elem, 'ContactName1'),
            'DateTimeLastChanged': parse_dt(text(customer_elem, 'DateTimeLastChanged')),
            'AccountCode': text(customer_elem, 'AccountCode'),
            'ShipToName': text(customer_elem, 'ShipToName'),
            'ShipToAddress1': text(customer_elem, 'ShipToAddress1'),
            'ShipToAddress2': text(customer_elem, 'ShipToAddress2'),
            'ShipToSuburb': text(customer_elem, 'ShipToSuburb'),
            'ShipToPostCode': text(customer_elem, 'ShipToPostCode'),
            'Sent2Host': text(customer_elem, 'Sent2Host'),
            'Sent2HostDateTime': parse_dt(text(customer_elem, 'Sent2HostDateTime')),
        }

        cust_obj = TREMOTETransCustomer(**cust_kwargs)
        db.add(cust_obj)

    # sale lines (may be many)
    for line_elem in root.findall('.//tREMOTETransSaleLines'):
        try:
            sale_line_kwargs = {
                'Company_ID': company_id,
                'StoreCode': store_code,
                'PostingDate': parse_dt(text(line_elem, 'PostingDate')) or posting_date,
                'TransID': text(line_elem, 'TransID') or trans_id,
                'SaleLineNo': int(text(line_elem, 'SaleLineNo')) if text(line_elem, 'SaleLineNo') else None,
                'SKU': text(line_elem, 'SKU'),
                'SaleQty': Decimal(text(line_elem, 'SaleQty')) if text(line_elem, 'SaleQty') else None,
                'SaleUnitAmountIncTax': Decimal(text(line_elem, 'SaleUnitAmountIncTax')) if text(line_elem, 'SaleUnitAmountIncTax') else None,
                'SaleTaxRate': Decimal(text(line_elem, 'SaleTaxRate')) if text(line_elem, 'SaleTaxRate') else None,
                'SaleUnitDiscount': Decimal(text(line_elem, 'SaleUnitDiscount')) if text(line_elem, 'SaleUnitDiscount') else None,
                'ItemID': text(line_elem, 'ItemID'),
                'SalesPerson': text(line_elem, 'SalesPerson'),
                'SaleRRP': Decimal(text(line_elem, 'SaleRRP')) if text(line_elem, 'SaleRRP') else None,
                'SaleTaxUnitAmount': Decimal(text(line_elem, 'SaleTaxUnitAmount')) if text(line_elem, 'SaleTaxUnitAmount') else None,
                'SKUDescription': text(line_elem, 'SKUDescription'),
                'CurrencyCode': text(line_elem, 'CurrencyCode'),
                'HOSKU': text(line_elem, 'HOSKU'),
                'Cost': Decimal(text(line_elem, 'Cost')) if text(line_elem, 'Cost') else None,
                'Sent2Host': text(line_elem, 'Sent2Host'),
                'Sent2HostDateTime': parse_dt(text(line_elem, 'Sent2HostDateTime')),
            }

            sale_obj = TREMOTETransSaleLines(**sale_line_kwargs)
            db.add(sale_obj)
        except Exception:
            # skip malformed lines but continue processing
            continue

    await db.commit()

    # sale tenders
    for tender_elem in root.findall('.//tREMOTETransSaleTenders'):
        try:
            tender_kwargs = {
                'Company_ID': company_id,
                'StoreCode': store_code,
                'PostingDate': parse_dt(text(tender_elem, 'PostingDate')) or posting_date,
                'TransID': text(tender_elem, 'TransID') or trans_id,
                'TenderLine': int(text(tender_elem, 'TenderLine')) if text(tender_elem, 'TenderLine') else None,
                'TenderType': text(tender_elem, 'TenderType'),
                'TenderAmount': Decimal(text(tender_elem, 'TenderAmount')) if text(tender_elem, 'TenderAmount') else None,
                'TDets1': text(tender_elem, 'TDets1'),
                'TDets2': text(tender_elem, 'TDets2'),
                'CurrencyCode': text(tender_elem, 'CurrencyCode'),
                'ForeignTenderAmount': Decimal(text(tender_elem, 'ForeignTenderAmount')) if text(tender_elem, 'ForeignTenderAmount') else None,
                'Search': text(tender_elem, 'Search'),
                'Sent2Host': text(tender_elem, 'Sent2Host'),
                'Sent2HostDateTime': parse_dt(text(tender_elem, 'Sent2HostDateTime')),
            }

            tender_obj = TREMOTETransSaleTenders(**tender_kwargs)
            db.add(tender_obj)
        except Exception:
            # skip malformed tenders but continue
            continue

    await db.commit()

    return {"message": "Imported", "TransID": trans_id}