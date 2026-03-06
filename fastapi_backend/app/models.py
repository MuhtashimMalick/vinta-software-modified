from typing import Any, Optional
import datetime
import decimal
from decimal import Decimal
import uuid
from sqlmodel import SQLModel
from sqlalchemy import BigInteger, Boolean, CHAR, Column, Computed, DECIMAL, DateTime, Float, Identity, Index, Integer, NCHAR, Numeric, PrimaryKeyConstraint, REAL, SmallInteger, String, TEXT, Table, Unicode, Uuid, text
from sqlalchemy.dialects.mssql import MONEY, SMALLDATETIME, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import MetaData

# metadata = MetaData(schema="dbo")
# Base = DeclarativeBase(metadata=metadata)
# class Base(DeclarativeBase):
#     pass
class Base(DeclarativeBase):
    metadata = MetaData(schema="dbo")
import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(
        default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

class EParcelHeader(Base):
    __tablename__ = 'eParcel_Header'
    __table_args__ = (
        PrimaryKeyConstraint('SendPCMSManifest_Id', 'TransactionId', name='PK_eParcel_Header'),
    )

    TransactionId: Mapped[str] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'), primary_key=True)
    SendPCMSManifest_Id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    TransactionDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ParentId: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    TransactionSequence: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    ApplicationId: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
# class EParcelHeader(Base):
#     __tablename__ = "eParcel_Header"

#     __table_args__ = (
#         PrimaryKeyConstraint(
#             "SendPCMSManifest_Id",
#             "TransactionId",
#             name="PK_eParcel_Header",
#         ),
#         {"schema": "dbo"},
#     )

#     TransactionId: Mapped[str] = mapped_column(
#         Unicode(40, collation="Latin1_General_CI_AS"),
#         primary_key=True,
#     )

#     SendPCMSManifest_Id: Mapped[uuid.UUID] = mapped_column(
#         Uuid,
#         primary_key=True,
#     )

#     TransactionDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(
#         DateTime
#     )

#     ParentId: Mapped[Optional[str]] = mapped_column(
#         Unicode(40, collation="Latin1_General_CI_AS")
#     )

#     TransactionSequence: Mapped[Optional[str]] = mapped_column(
#         Unicode(40, collation="Latin1_General_CI_AS")
#     )

#     ApplicationId: Mapped[Optional[str]] = mapped_column(
#         Unicode(20, collation="Latin1_General_CI_AS")
#     )

class EParcelPCMSConsignment(Base):
    __tablename__ = 'eParcel_PCMSConsignment'
    __table_args__ = (
        PrimaryKeyConstraint('SendPCMSManifest_Id', 'merchantlocationid', 'manifestnumber', 'ConsignmentNumber', name='PK_eParcel_PCMSConsignment'),
    )

    ConsignmentNumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), primary_key=True)
    SendPCMSManifest_Id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    merchantlocationid: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), primary_key=True)
    manifestnumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), primary_key=True)
    ChargeCode: Mapped[Optional[str]] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'))
    InternalChargebackAccount: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    ReferenceNo1: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    ReferenceNo2: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    DeliveryName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    DeliveryCompanyName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    EmailNotification: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    DeliveryAddressLine1: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    DeliveryAddressLine2: Mapped[Optional[str]] = mapped_column(Unicode(60, 'Latin1_General_CI_AS'))
    DeliveryAddressLine3: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    DeliveryAddressLine4: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    DeliveryPhoneNumber: Mapped[Optional[str]] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'))
    DeliveryEmailAddress: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    DeliverySuburb: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    DeliveryStateCode: Mapped[Optional[str]] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'))
    DeliveryPostcode: Mapped[Optional[str]] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'))
    DeliveryCountryCode: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    DeliveryInstructions: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    IsInternationalDelivery: Mapped[Optional[bool]] = mapped_column(Boolean)
    ReturnName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    ReturnAddressLine1: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    ReturnAddressLine2: Mapped[Optional[str]] = mapped_column(Unicode(60, 'Latin1_General_CI_AS'))
    ReturnAddressLine3: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    ReturnAddressLine4: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    ReturnSuburb: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    ReturnStateCode: Mapped[Optional[str]] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'))
    ReturnPostcode: Mapped[Optional[str]] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'))
    ReturnCountryCode: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ReturnDeliveryInstructions: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    CreatedDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PostChargeToAccount: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    IsSignatureRequired: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    CTCAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(28, 10))
    DeliverPartConsignment: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    ContainsDangerousGoods: Mapped[Optional[bool]] = mapped_column(Boolean)
    ProfileId: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    PCMSManifest_Id: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 0))


class EParcelPCMSDomesticArticle(Base):
    __tablename__ = 'eParcel_PCMSDomesticArticle'
    __table_args__ = (
        PrimaryKeyConstraint('SendPCMSManifest_Id', 'merchantlocationid', 'manifestnumber', 'consignmentnumber', 'ArticleNumber', name='PK_eParcel_PCMSDomesticArticle'),
    )

    ArticleNumber: Mapped[str] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'), primary_key=True)
    SendPCMSManifest_Id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    merchantlocationid: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), primary_key=True)
    manifestnumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), primary_key=True)
    consignmentnumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), primary_key=True)
    BarcodeArticleNumber: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    Length: Mapped[Optional[int]] = mapped_column(BigInteger)
    Width: Mapped[Optional[int]] = mapped_column(BigInteger)
    Height: Mapped[Optional[int]] = mapped_column(BigInteger)
    ActualWeight: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(28, 10))
    CubicWeight: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(28, 10))
    ArticleDescription: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    IsTransitCoverRequired: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    TransitCoverAmount: Mapped[Optional[str]] = mapped_column(Unicode(40, 'Latin1_General_CI_AS'))
    PCMSConsignment_Id: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 0))


class EParcelPCMSManifest(Base):
    __tablename__ = 'eParcel_PCMSManifest'
    __table_args__ = (
        PrimaryKeyConstraint('SendPCMSManifest_Id', 'MerchantLocationId', 'ManifestNumber', name='PK_eParcel_PCMSManifest'),
    )

    MerchantLocationId: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), primary_key=True)
    ManifestNumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), primary_key=True)
    SendPCMSManifest_Id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    DateSubmitted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DateLodged: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    body_Id: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 0))


class TAccounts(Base):
    __tablename__ = 'tAccounts'
    __table_args__ = (
        PrimaryKeyConstraint('AccountID', name='PK_tAccounts'),
    )

    AccountID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ParentAccountID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsInactive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    AccountName: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    AccountNumber: Mapped[str] = mapped_column(Unicode(6, 'Latin1_General_CI_AS'), nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    CurrencyExchangeAccountID: Mapped[int] = mapped_column(Integer, nullable=False)
    AccountClassificationID: Mapped[str] = mapped_column(Unicode(4, 'Latin1_General_CI_AS'), nullable=False)
    AccountLevel: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    AccountTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    LastChequeNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    IsReconciled: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    StatementBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    IsCreditBalance: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    OpeningAccountBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    CurrentAccountBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    PreLastYearActivity: Mapped[float] = mapped_column(Float(53), nullable=False)
    LastYearOpeningBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    ThisYearOpeningBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    PostThisYearActivity: Mapped[float] = mapped_column(Float(53), nullable=False)
    LastReconciledDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)


class TAcquitalCharges(Base):
    __tablename__ = 'tAcquitalCharges'
    __table_args__ = (
        PrimaryKeyConstraint('ReceiptID', 'ChargeID', name='PK_tAcquitalCharges'),
    )

    ReceiptID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ChargeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ChargeAmount: Mapped[float] = mapped_column(Float(53), nullable=False)


class TAcquitalHeader(Base):
    __tablename__ = 'tAcquitalHeader'
    __table_args__ = (
        PrimaryKeyConstraint('AcquitalID', 'PurchaseID', name='PK_tAcquitalHeader'),
    )

    AcquitalID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PurchaseID: Mapped[int] = mapped_column(Integer, primary_key=True)
    MYOBOrderTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    CalculatedInvoiceCost: Mapped[float] = mapped_column(Float(53), nullable=False)
    DateCommitted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ActualExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    SuppInvAmt: Mapped[float] = mapped_column(Float(53), nullable=False)
    InternalCosting: Mapped[float] = mapped_column(Float(53), nullable=False)
    SuppGSTAmt: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalChargesGSTAmt: Mapped[float] = mapped_column(Float(53), nullable=False)
    CalculatedExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    LandedUnitCostFactor: Mapped[float] = mapped_column(Float(53), nullable=False)
    DateReceived: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    SupplierInvoiceNumber: Mapped[str] = mapped_column(CHAR(30, 'Latin1_General_CI_AS'), nullable=False)
    Consolidation: Mapped[str] = mapped_column(CHAR(30, 'Latin1_General_CI_AS'), nullable=False)
    OverseasSupplier: Mapped[str] = mapped_column(CHAR(50, 'Latin1_General_CI_AS'), nullable=False)
    MYOBPurchaseNumber: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Latin1_General_CI_AS'))
    LandedCost: Mapped[Optional[float]] = mapped_column(Float(53))
    InvoiceExchangeRate: Mapped[Optional[float]] = mapped_column(Float(53))
    MultipleAcquitalID: Mapped[Optional[int]] = mapped_column(Integer)
    AUDInternalCosts: Mapped[Optional[float]] = mapped_column(Float(53))


t_tAcquitalLines = Table(
    'tAcquitalLines', Base.metadata,
    Column('PurchaseID', Integer, nullable=False),
    Column('PurchaseLineNumber', Integer, nullable=False),
    Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('ItemQty', Float(53), nullable=False),
    Column('ItemCostUS', Float(53), nullable=False),
    Column('ItemCostAUD', Float(53), nullable=False),
    Column('ExtendedCostAUD', Float(53), nullable=False),
    Column('AcqLinePercentage', Float(53), nullable=False),
    Column('AcqUnitCostFactor', Float(53), nullable=False)
)


class TAddress(Base):
    __tablename__ = 'tAddress'
    __table_args__ = (
        PrimaryKeyConstraint('AddressID', name='PK_tAddress'),
    )

    AddressID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    Location: Mapped[int] = mapped_column(Integer, nullable=False)
    Street: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    City: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    State: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Country: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Phone1: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    Phone2: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    Phone3: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    Fax: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    Email: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    WWW: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Salutation: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    ContactName: Mapped[str] = mapped_column(CHAR(50, 'Latin1_General_CI_AS'), nullable=False)
    StreetLine1: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    StreetLine2: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    StreetLine3: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    StreetLine4: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ChangeControl: Mapped[str] = mapped_column(CHAR(5, 'Latin1_General_CI_AS'), nullable=False)
    PostCode: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


t_tAddressLabelConfig = Table(
    'tAddressLabelConfig', Base.metadata,
    Column('SaleID', Integer, nullable=False),
    Column('LabelField', CHAR(25, 'Latin1_General_CI_AS'))
)


class TAttacheInvoiceHdextn(Base):
    __tablename__ = 'tAttache_Invoice_Hdextn'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tAttache_Invoice_Hdextn'),
        Index('IX_tAttache_Invoice_Hdextn_InvoiceNumber', 'InvoiceNumber', mssql_clustered=False, mssql_include=[]),
        Index('IX_tAttache_Invoice_Hdextn_SaleID', 'SaleID', mssql_clustered=False, mssql_include=[]),
        Index('IX_tAttache_Invoice_Hdextn_SubReferenceNumber', 'SubReferenceNumber', mssql_clustered=False, mssql_include=[])
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    InvoiceNumber: Mapped[str] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'), nullable=False)
    SubReferenceNumber: Mapped[int] = mapped_column(Integer, nullable=False)


class TAttacheInvoiceHeader(Base):
    __tablename__ = 'tAttache_Invoice_Header'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tAttache_Invoice_Header'),
        Index('IX_tAttache_Invoice_Header_InvoiceNumber', 'InvoiceNumber', mssql_clustered=False, mssql_include=[]),
        Index('IX_tAttache_Invoice_Header_SaleID', 'SaleID', mssql_clustered=False, mssql_include=[])
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    InvoiceNumber: Mapped[str] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'), nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    LocNo: Mapped[int] = mapped_column(Integer, nullable=False)
    CardRecordID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomerPONumber: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    IsHistorical: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsThirteenthPeriod: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    ShipToAddress: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine3: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine4: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    InvoiceTypeID: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    InvoiceStatusID: Mapped[Optional[str]] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'))
    Memo: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Comment: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsTaxInclusive: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    IsPrinted: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    CostCentreID: Mapped[Optional[int]] = mapped_column(Integer)
    LinesPurged: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    PreAuditTrail: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    InvoiceDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickingStatus: Mapped[Optional[int]] = mapped_column(SmallInteger)
    PrintCount: Mapped[Optional[int]] = mapped_column(Integer)
    OverrideCustomerName: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine2: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine3: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverridePostCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TimeSalePicked: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickedBYID: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    BOLoaded: Mapped[Optional[bool]] = mapped_column(Boolean)
    OrderStatus: Mapped[Optional[int]] = mapped_column(Integer)
    ProfileID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))


class TB4PStocktakeCounts(Base):
    __tablename__ = 'tB4PStocktakeCounts'
    __table_args__ = (
        PrimaryKeyConstraint('serial', name='PK_tB4PStocktakeCounts'),
    )

    serial: Mapped[int] = mapped_column(Integer, primary_key=True)
    stocktake_name: Mapped[str] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'), nullable=False)
    stocktake_loc: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    stocktake_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    stock_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    date_modified: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    barcode: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    barcode1: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    barcode2: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    barcode3: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


t_tBolwellBuildsNotInMYOB = Table(
    'tBolwellBuildsNotInMYOB', Base.metadata,
    Column('ItemID', Integer, nullable=False),
    Column('ItemNumber', Unicode(32, 'Latin1_General_CI_AS'), nullable=False)
)


class TBuildComponents(Base):
    __tablename__ = 'tBuildComponents'
    __table_args__ = (
        PrimaryKeyConstraint('BuiltItemID', 'SequenceNumber', 'ComponentID', name='PK_tBuildComponents'),
    )

    BuildComponentID: Mapped[int] = mapped_column(Integer, nullable=False)
    BuiltItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SequenceNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    ComponentID: Mapped[int] = mapped_column(Integer, primary_key=True)
    QuantityNeeded: Mapped[float] = mapped_column(Float(53), nullable=False)


class TCards(Base):
    __tablename__ = 'tCards'
    __table_args__ = (
        PrimaryKeyConstraint('CardRecordID', name='PK_tCards'),
    )

    CardRecordID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardIdentification: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'))
    CardTypeID: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    Name: Mapped[Optional[str]] = mapped_column(String(60, 'Latin1_General_CI_AS'))
    LastName: Mapped[Optional[str]] = mapped_column(String(60, 'Latin1_General_CI_AS'))
    FirstName: Mapped[Optional[str]] = mapped_column(String(60, 'Latin1_General_CI_AS'))
    IsIndividual: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    IsInactive: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    CurrencyID: Mapped[Optional[int]] = mapped_column(Integer)
    Notes: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Identifiers: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Latin1_General_CI_AS'))
    IdentifierID: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Latin1_General_CI_AS'))
    Customlist1ID: Mapped[Optional[int]] = mapped_column(Integer)
    Customlist2ID: Mapped[Optional[int]] = mapped_column(Integer)
    Customlist3ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomField1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    CustomField2: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    CustomField3: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    ChangeControl: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))


t_tCategoryDSN = Table(
    'tCategoryDSN', Base.metadata,
    Column('CustomListID', Integer),
    Column('CustomListText', Unicode(30, 'Latin1_General_CI_AS')),
    Column('DSNName', Unicode(50, 'Latin1_General_CI_AS'))
)


class TCoilRegister(Base):
    __tablename__ = 'tCoilRegister'
    __table_args__ = (
        PrimaryKeyConstraint('CoilID', name='PK_tCoilRegister'),
    )

    CoilID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    StockCode: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    SupplierID: Mapped[int] = mapped_column(Integer, nullable=False)
    CoilNo: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    PackNo: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    DateInsert: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    Consumed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    LocationNo: Mapped[str] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'), nullable=False)
    Printed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    Mass: Mapped[Optional[float]] = mapped_column(Float(53))
    DateConsumed: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FromPONo: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))


class TComments(Base):
    __tablename__ = 'tComments'
    __table_args__ = (
        PrimaryKeyConstraint('CommentID', name='PK_tComments'),
    )

    CommentID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=Decimal('1'), increment=Decimal('1')), primary_key=True)
    Comment: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)


class TConfig(Base):
    __tablename__ = 'tConfig'
    __table_args__ = (
        PrimaryKeyConstraint('ConfigID', name='PK_tConfig'),
    )

    ConfigID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    SMTPServer: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    SMTPUser: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    SMTPPass: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    FROMEmail: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Emails_Auto_on_Schedule: Mapped[Optional[bool]] = mapped_column(Boolean)
    Email_via_Queue: Mapped[Optional[bool]] = mapped_column(Boolean)


class TConfiguration(Base):
    __tablename__ = 'tConfiguration'
    __table_args__ = (
        PrimaryKeyConstraint('ConfigID', name='PK_tConfiguration'),
    )

    ConfigID: Mapped[int] = mapped_column(Integer, primary_key=True)
    KANBANPicDirectory: Mapped[str] = mapped_column(CHAR(25, 'Latin1_General_CI_AS'), nullable=False)


class TCostCentres(Base):
    __tablename__ = 'tCostCentres'
    __table_args__ = (
        PrimaryKeyConstraint('CostCentreID', name='PK_tCostCentres'),
    )

    CostCentreID: Mapped[int] = mapped_column(Integer, primary_key=True)
    IsInactive: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    CostCentreName: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    CostCentreIdentification: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    CostCentreDescription: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TCurrency(Base):
    __tablename__ = 'tCurrency'
    __table_args__ = (
        PrimaryKeyConstraint('CurrencyID', name='PK_tCurrency'),
    )

    CurrencyID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    CurrencyCode: Mapped[str] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'), nullable=False)
    CurrencyName: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    ExchangeRate: Mapped[Optional[float]] = mapped_column(Float(53))
    CurrencySymbol: Mapped[Optional[str]] = mapped_column(Unicode(4, 'Latin1_General_CI_AS'))
    DigitGroupingSymbol: Mapped[Optional[str]] = mapped_column(String(1, 'Latin1_General_CI_AS'))
    SymbolPosition: Mapped[Optional[str]] = mapped_column(CHAR(13, 'Latin1_General_CI_AS'))
    DecimalPlaces: Mapped[Optional[int]] = mapped_column(Integer)
    NumberDigitsInGroup: Mapped[Optional[int]] = mapped_column(Integer)
    DecimalPlacesSymbol: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    NegativeFormat: Mapped[Optional[str]] = mapped_column(CHAR(25, 'Latin1_General_CI_AS'))
    UseLeadingZero: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))


class TCustomLists(Base):
    __tablename__ = 'tCustomLists'
    __table_args__ = (
        PrimaryKeyConstraint('CustomListID', name='PK_tCustomLists'),
    )

    CustomListID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CustomListType: Mapped[str] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'), nullable=False)
    CustomListText: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    CustomListNumber: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CustomListName: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ChangeControl: Mapped[str] = mapped_column(Unicode(5, 'Latin1_General_CI_AS'), nullable=False)


class TCustomerPaymentLines(Base):
    __tablename__ = 'tCustomerPaymentLines'
    __table_args__ = (
        PrimaryKeyConstraint('CustomerPaymentLineID', name='PK_tCustomerPaymentLines'),
    )

    CustomerPaymentLineID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    CustomerPaymentID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    AmountApplied: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    IsDepositPayment: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    SaleIDfromMYOB: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))


class TCustomerPayments(Base):
    __tablename__ = 'tCustomerPayments'
    __table_args__ = (
        PrimaryKeyConstraint('CustomerPaymentID', name='PK_tCustomerPayments'),
    )

    CustomerPaymentID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TransactionDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    IsTaxInclusive: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    CurrencyID: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    TotalCustomerPayment: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    MethodofPaymentID: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CustomerPaymentNumber: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Memo: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    PaymentCardNumber: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    PaymentNameonCard: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    PaymentExpirationDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PaymentAuthorisationNumber: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))
    PaymentChequeNumber: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'))
    PaymentBankAccountNumber: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'))
    PaymentBankAccountName: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    PaymentBSB: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))
    PaymentBankBranch: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    PaymentNotes: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    CardRecordID: Mapped[Optional[int]] = mapped_column(Integer)


class TCustomerProductProfileDetails(Base):
    __tablename__ = 'tCustomerProductProfileDetails'
    __table_args__ = (
        PrimaryKeyConstraint('Customer_ID', 'Product_Name', 'Product_Module', name='PK_tCustomerProductProfileDetails'),
    )

    Customer_ID: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    Product_Name: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    Product_Module: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    AccountCode: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)


class TCustomers(Base):
    __tablename__ = 'tCustomers'
    __table_args__ = (
        PrimaryKeyConstraint('CustomerID', name='PK_tCustomers'),
        Index('IX_tCustomers_Change_Control', 'ChangeControl', mssql_clustered=False, mssql_include=[]),
        Index('IX_tCustomers_Name', 'Name', mssql_clustered=False, mssql_include=[])
    )

    CustomerID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    CardIdentification: Mapped[str] = mapped_column(Unicode(16, 'Latin1_General_CI_AS'), nullable=False)
    Name: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    LastName: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    FirstName: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    IsIndividual: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    IsInactive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Notes: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    IdentifierID: Mapped[str] = mapped_column(Unicode(26, 'Latin1_General_CI_AS'), nullable=False)
    CustomField1: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    CustomField2: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    CustomField3: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    ABN: Mapped[str] = mapped_column(Unicode(14, 'Latin1_General_CI_AS'), nullable=False)
    ABNBranch: Mapped[str] = mapped_column(Unicode(11, 'Latin1_General_CI_AS'), nullable=False)
    PriceLevelID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    TaxIDNumber: Mapped[str] = mapped_column(Unicode(19, 'Latin1_General_CI_AS'), nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    UseCustomerTaxCode: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    CreditLimit: Mapped[float] = mapped_column(Float(53), nullable=False)
    VolumeDiscount: Mapped[float] = mapped_column(Float(53), nullable=False)
    CurrentBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalReceivableDays: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalPaidInvoices: Mapped[int] = mapped_column(Integer, nullable=False)
    HighestInvoiceAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    HighestReceivableAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    PaymentCardNumber: Mapped[str] = mapped_column(Unicode(25, 'Latin1_General_CI_AS'), nullable=False)
    PaymentNameOnCard: Mapped[str] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'), nullable=False)
    PaymentBankAccountName: Mapped[str] = mapped_column(Unicode(32, 'Latin1_General_CI_AS'), nullable=False)
    PaymentNotes: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    HourlyBillingRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    SaleLayoutID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    PrintedForm: Mapped[str] = mapped_column(Unicode(34, 'Latin1_General_CI_AS'), nullable=False)
    ChangeControl: Mapped[str] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'), nullable=False)
    CurrencyID: Mapped[Optional[int]] = mapped_column(Integer)
    Picture: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Identifiers: Mapped[Optional[str]] = mapped_column(Unicode(26, 'Latin1_General_CI_AS'))
    CustomList1ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomList2ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomList3ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomerSince: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    LastSaleDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    LastPaymentDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    MethodOfPaymentID: Mapped[Optional[int]] = mapped_column(Integer)
    PaymentExpirationDate: Mapped[Optional[str]] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'))
    PaymentBSB: Mapped[Optional[str]] = mapped_column(String(11, 'Latin1_General_CI_AS'))
    PaymentBankAccountNumber: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    IncomeAccountID: Mapped[Optional[int]] = mapped_column(Integer)
    SalespersonID: Mapped[Optional[int]] = mapped_column(Integer)
    SaleCommentID: Mapped[Optional[int]] = mapped_column(Integer)
    ShippingMethodID: Mapped[Optional[int]] = mapped_column(Integer)
    GSTIDNumber: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    ReceiptMemo: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    PaymentBankBranch: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    PaymentAddress: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    PaymentZIP: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    PaymentCardVerification: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    ACCNO: Mapped[Optional[int]] = mapped_column(Integer)
    ONHOLD: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))


class TDRACCS(Base):
    __tablename__ = 'tDR_ACCS'
    __table_args__ = (
        PrimaryKeyConstraint('ACCNO', name='PK_DR_ACCS'),
    )

    ACCNO: Mapped[int] = mapped_column(Integer, primary_key=True)
    FREIGHT_FREE: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('N')"))
    KEEPTRANSACTIONS: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('Y')"))
    NEED_ORDERNO: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('N')"))
    ALLOW_RESTRICTED_STOCK: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('Y')"))
    PRIVATE_ACC: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('N')"))
    ISTEMPLATE: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('N')"))
    NAME: Mapped[Optional[str]] = mapped_column(String(40, 'Latin1_General_CI_AS'), server_default=text("('')"))
    ADDRESS1: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDRESS2: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDRESS3: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR1: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR2: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR3: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR4: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    PHONE: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    FAX: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    EMAIL: Mapped[Optional[str]] = mapped_column(String(60, 'Latin1_General_CI_AS'))
    CREDLIMIT: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ACCGROUP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    SALESNO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    LASTMONTH: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    LASTYEAR: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    AGEDBAL0: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    AGEDBAL1: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    AGEDBAL2: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    AGEDBAL3: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    CREDITSTATUS: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    DISCOUNTLEVEL: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    OPENITEM: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('Y')"))
    INVOICETYPE: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    NOTES: Mapped[Optional[str]] = mapped_column(String(4096, 'Latin1_General_CI_AS'))
    MONTHVAL: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    YEARVAL: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    STARTDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))
    SORTCODE: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    BANK: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    BANK_ACCOUNT: Mapped[Optional[str]] = mapped_column(String(40, 'Latin1_General_CI_AS'))
    BANK_ACC_NAME: Mapped[Optional[str]] = mapped_column(String(40, 'Latin1_General_CI_AS'))
    BSBNO: Mapped[Optional[str]] = mapped_column(String(40, 'Latin1_General_CI_AS'))
    D_DEBIT_FAX: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('N')"))
    D_DEBIT_PRINT: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('N')"))
    D_DEBIT_EMAIL: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('N')"))
    PAY_TYPE: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    BRANCH: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DRAWER: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    TAXSTATUS: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    PRICENO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((1))'))
    AUTOBILLCODE: Mapped[Optional[str]] = mapped_column(String(23, 'Latin1_General_CI_AS'))
    ALPHACODE: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    HEAD_ACCNO: Mapped[Optional[int]] = mapped_column(Integer)
    PASS_WORD: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    CURRENCYNO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    ALERT: Mapped[Optional[str]] = mapped_column(String(60, 'Latin1_General_CI_AS'))
    STATEMENT: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('Y')"))
    INVFILENO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    PROMPTPAY_PC: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    PROMPTPAY_AMT: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ISACTIVE: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('Y')"))
    BAD_CHEQUE: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('N')"))
    BRANCHNO: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    LAST_UPDATED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TAXREG: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    STOPCREDIT: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('N')"))
    DELADDR5: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR6: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    POST_CODE: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    GLCONTROLACC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    GLCONTROLSUBACC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    PRIOR_AGEDBAL0: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    PRIOR_AGEDBAL1: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    PRIOR_AGEDBAL2: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    PRIOR_AGEDBAL3: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    BALANCE: Mapped[Optional[float]] = mapped_column(Float(53), Computed('((([AGEDBAL0]+[AGEDBAL1])+[AGEDBAL2])+[AGEDBAL3])', persisted=False))
    PRIOR_BALANCE: Mapped[Optional[float]] = mapped_column(Float(53), Computed('((([PRIOR_AGEDBAL0]+[PRIOR_AGEDBAL1])+[PRIOR_AGEDBAL2])+[PRIOR_AGEDBAL3])', persisted=False))
    ADDRESS4: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ACCGROUP2: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("('0')"))
    COURIER_DEPOT_SEQNO: Mapped[Optional[int]] = mapped_column(Integer)
    PRICEGROUP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    LastOrderDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LastOrderValue: Mapped[Optional[float]] = mapped_column(Float(53))
    X_DAY1: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_DAY2: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_DAY3: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_DAY4: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_DAY5: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_DAY6: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_DAY7: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    RICG_CreditTerms: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


t_tDataFileInformation = Table(
    'tDataFileInformation', Base.metadata,
    Column('CompanyName', String(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('Address', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('Phone', String(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('FaxNumber', String(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('Email', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('ABN', String(14, 'Latin1_General_CI_AS'), nullable=False),
    Column('ABNBranch', String(11, 'Latin1_General_CI_AS'), nullable=False),
    Column('ACN', String(19, 'Latin1_General_CI_AS'), nullable=False),
    Column('GSTRegistrationNumber', CHAR(19, 'Latin1_General_CI_AS'), nullable=False),
    Column('SalesTaxNumber', CHAR(19, 'Latin1_General_CI_AS'), nullable=False),
    Column('CompanyRegistrationNumber', CHAR(19, 'Latin1_General_CI_AS'), nullable=False),
    Column('UseMultipleCurrencies', CHAR(1, 'Latin1_General_CI_AS'))
)


class TEDITransRecords(Base):
    __tablename__ = 'tEDI_Trans_Records'
    __table_args__ = (
        PrimaryKeyConstraint('RecordID', name='PK_tEDI_Trans_Records'),
        Index('IX_tEDI_Trans_Records', 'SaleID', mssql_clustered=False, mssql_include=[])
    )

    RecordID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    TransType: Mapped[str] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'), nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    FileName: Mapped[str] = mapped_column(Unicode(35, 'Latin1_General_CI_AS'), nullable=False)
    Date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('(getdate())'))
    Status: Mapped[int] = mapped_column(SmallInteger, nullable=False)


t_tEftPOSParms = Table(
    'tEftPOSParms', Base.metadata,
    Column('MerchID', String(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('TermID', String(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('HostAddress', String(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('HostPort', String(30, 'Latin1_General_CI_AS'), nullable=False)
)


class TEmailQueue(Base):
    __tablename__ = 'tEmailQueue'
    __table_args__ = (
        PrimaryKeyConstraint('EMailQid', name='PK_tEmailQueue'),
    )

    EMailQid: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    FromEmail: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ToEmail: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Status: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    DateTimeInserted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    EmailSubject: Mapped[Optional[str]] = mapped_column(String(4096, 'Latin1_General_CI_AS'))
    EmailBody: Mapped[Optional[str]] = mapped_column(Unicode(collation='Latin1_General_CI_AS'))
    AttachmentPath: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    DateTimePrinted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EmailCC: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TEmployees(Base):
    __tablename__ = 'tEmployees'
    __table_args__ = (
        PrimaryKeyConstraint('EmployeeID', name='PK_tEmployees'),
    )

    EmployeeID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    BankAccountName: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    IsPaidElectronically: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    CardRecordID: Mapped[Optional[int]] = mapped_column(BigInteger)
    CardIdentification: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'))
    Name: Mapped[Optional[str]] = mapped_column(CHAR(60, 'Latin1_General_CI_AS'))
    LastName: Mapped[Optional[str]] = mapped_column(CHAR(60, 'Latin1_General_CI_AS'))
    FirstName: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Latin1_General_CI_AS'))
    IsIndividual: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    IsInactive: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    CurrencyID: Mapped[Optional[int]] = mapped_column(BigInteger)
    Picture: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Latin1_General_CI_AS'))
    Notes: Mapped[Optional[str]] = mapped_column(CHAR(255, 'Latin1_General_CI_AS'))
    Identifiers: Mapped[Optional[str]] = mapped_column(CHAR(26, 'Latin1_General_CI_AS'))
    IdentifierID: Mapped[Optional[str]] = mapped_column(CHAR(26, 'Latin1_General_CI_AS'))
    CustomList1ID: Mapped[Optional[int]] = mapped_column(BigInteger)
    CustomList2ID: Mapped[Optional[int]] = mapped_column(BigInteger)
    CustomList3ID: Mapped[Optional[int]] = mapped_column(BigInteger)
    CustomField1: Mapped[Optional[str]] = mapped_column(String(155, 'Latin1_General_CI_AS'))
    CustomField2: Mapped[Optional[str]] = mapped_column(String(155, 'Latin1_General_CI_AS'))
    CustomField3: Mapped[Optional[str]] = mapped_column(String(155, 'Latin1_General_CI_AS'))
    BSBCode: Mapped[Optional[str]] = mapped_column(CHAR(7, 'Latin1_General_CI_AS'))
    BankAccountNumber: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    HourlyBillingRate: Mapped[Optional[Any]] = mapped_column(MONEY)
    EstimatedCostPerHour: Mapped[Optional[Any]] = mapped_column(MONEY)
    EmploymentBasisID: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Latin1_General_CI_AS'))
    StartDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TaxScaleID: Mapped[Optional[int]] = mapped_column(BigInteger)
    TaxFileNumber: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'))
    DateOfBirth: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TotalRebates: Mapped[Optional[Any]] = mapped_column(MONEY)
    ExtraTax: Mapped[Optional[Any]] = mapped_column(MONEY)
    TerminationDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    WagesExpenseAccountID: Mapped[Optional[int]] = mapped_column(BigInteger)
    PayBasisID: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    BasePay: Mapped[Optional[Any]] = mapped_column(MONEY)
    PayFrequencyID: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    ChangeControl: Mapped[Optional[str]] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'))


t_tFieldMapping = Table(
    'tFieldMapping', Base.metadata,
    Column('MYOBField', Unicode(50, 'Latin1_General_CI_AS')),
    Column('MappedField', Unicode(50, 'Latin1_General_CI_AS'))
)


class TFreightCompany(Base):
    __tablename__ = 'tFreightCompany'
    __table_args__ = (
        PrimaryKeyConstraint('FreightCompanyID', name='PK_tFreightCompany'),
    )

    FreightCompanyID: Mapped[int] = mapped_column(Integer, primary_key=True)
    FreightCompany: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)


class TFreightConNoteNumbers(Base):
    __tablename__ = 'tFreightConNoteNumbers'
    __table_args__ = (
        PrimaryKeyConstraint('ConNoteID', 'SaleID', name='PK_tFreightConNoteNumbers'),
    )

    ConNoteID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)


class TFreightInformation(Base):
    __tablename__ = 'tFreightInformation'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tFreightInformation'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    DateShipped: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FreightCompany: Mapped[Optional[str]] = mapped_column(Unicode(52, 'Latin1_General_CI_AS'))
    TrackingNumber: Mapped[Optional[str]] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'))
    PackageType: Mapped[Optional[str]] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'))
    NoOfCartons: Mapped[Optional[int]] = mapped_column(Integer)
    Comments: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Latin1_General_CI_AS'))


class TGoodsReceiptHeader(Base):
    __tablename__ = 'tGoodsReceiptHeader'
    __table_args__ = (
        PrimaryKeyConstraint('GReceiptID', name='PK_tGoodsReceipts'),
    )

    GReceiptID: Mapped[int] = mapped_column(Integer, primary_key=True)
    GRDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    SupplierID: Mapped[int] = mapped_column(Integer, nullable=False)
    InMYOB: Mapped[bool] = mapped_column(Boolean, nullable=False)
    SupplierInvNo: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Latin1_General_CI_AS'))
    OrderType: Mapped[Optional[str]] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'))
    POID: Mapped[Optional[int]] = mapped_column(Integer)
    PONumber: Mapped[Optional[str]] = mapped_column(String(8, 'Latin1_General_CI_AS'))
    Status: Mapped[Optional[int]] = mapped_column(Integer)
    LOGINID: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    LOCNO: Mapped[Optional[int]] = mapped_column(Integer)
    new_order_id: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


class TGoodsReceiptHeaderNew(Base):
    __tablename__ = 'tGoodsReceiptHeaderNew'
    __table_args__ = (
        PrimaryKeyConstraint('GReceiptID', name='PK_tGoodsReceiptHeaderNew'),
        Index('IX_tGoodsReceiptHeaderNew_GRSHeaderGUID', 'GRSHeaderGUID', mssql_clustered=False, mssql_include=[])
    )

    GReceiptID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    GRDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    SupplierID: Mapped[int] = mapped_column(Integer, nullable=False)
    InMYOB: Mapped[bool] = mapped_column(Boolean, nullable=False)
    GRSHeaderGUID: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    SupplierInvNo: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Latin1_General_CI_AS'))
    OrderType: Mapped[Optional[str]] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'))
    POID: Mapped[Optional[int]] = mapped_column(Integer)
    PONumber: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    Status: Mapped[Optional[int]] = mapped_column(Integer)
    LOGINID: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    LOCNO: Mapped[Optional[int]] = mapped_column(Integer)
    new_order_id: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    PickedBYID: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))


class TGoodsReceiptLines(Base):
    __tablename__ = 'tGoodsReceiptLines'
    __table_args__ = (
        PrimaryKeyConstraint('GReceiptID', 'GReceiptLineNo', name='PK_tGoodsReceiptLines'),
    )

    GReceiptID: Mapped[int] = mapped_column(Integer, primary_key=True)
    GReceiptLineNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    Barcode: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    ItemNumber: Mapped[str] = mapped_column(String(32, 'Latin1_General_CI_AS'), nullable=False)
    InMYOB: Mapped[bool] = mapped_column(Boolean, nullable=False)
    Quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    ItemName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TaxCodeID: Mapped[Optional[int]] = mapped_column(Integer)
    TaxExclusiveAmount: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyOrd: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    POLineNo: Mapped[Optional[int]] = mapped_column(Integer)
    Barcode2: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Barcode3: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


class TGoodsReceiptLinesAllocationsNew(Base):
    __tablename__ = 'tGoodsReceiptLinesAllocationsNew'
    __table_args__ = (
        PrimaryKeyConstraint('GReceiptID', 'GReceiptLineNo', 'GReceiptLineNoAlloc', name='PK_tGoodsReceiptLinesAllocationsNew'),
    )

    GReceiptID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    GReceiptLineNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    GReceiptLineNoAlloc: Mapped[int] = mapped_column(Integer, primary_key=True)
    LocationID: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    LocationBinID: Mapped[int] = mapped_column(Integer, nullable=False)
    Quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    Batch_Serial_No: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Expiry_Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Matched: Mapped[Optional[bool]] = mapped_column(Boolean)
    Received: Mapped[Optional[bool]] = mapped_column(Boolean)


class TGoodsReceiptLinesNew(Base):
    __tablename__ = 'tGoodsReceiptLinesNew'
    __table_args__ = (
        PrimaryKeyConstraint('GReceiptID', 'GReceiptLineNo', name='PK_tGoodsReceiptLinesNew'),
    )

    GReceiptID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    GReceiptLineNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    Barcode: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    ItemNumber: Mapped[str] = mapped_column(String(32, 'Latin1_General_CI_AS'), nullable=False)
    InMYOB: Mapped[bool] = mapped_column(Boolean, nullable=False)
    Quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    ItemName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TaxCodeID: Mapped[Optional[int]] = mapped_column(Integer)
    TaxExclusiveAmount: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyOrd: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    POLineNo: Mapped[Optional[int]] = mapped_column(Integer)
    Barcode2: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Barcode3: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    SerialTracked: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    BatchTracked: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    ItemTAG: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    LineID: Mapped[Optional[int]] = mapped_column(Integer)
    ILineNo: Mapped[Optional[int]] = mapped_column(Integer)


t_tIFOTReportTable = Table(
    'tIFOTReportTable', Base.metadata,
    Column('IFOTReportDate', DateTime, nullable=False),
    Column('ScheduleOrigDueDate', DateTime, nullable=False),
    Column('ScheduleDateUpdated', DateTime, nullable=False),
    Column('ScheduleDate', DateTime, nullable=False),
    Column('ScheduleOrderDate', DateTime, nullable=False),
    Column('ScheduleDueDate', DateTime, nullable=False),
    Column('DespatchItemNumber', String(32, 'Latin1_General_CI_AS'), nullable=False),
    Column('DespatchBarcode', CHAR(25, 'Latin1_General_CI_AS'), nullable=False),
    Column('DespatchOrderNo', CHAR(15, 'Latin1_General_CI_AS'), nullable=False),
    Column('ScheduleQty', Integer, nullable=False),
    Column('DespatchQty', Integer, nullable=False)
)


class TIdentifierLatestNumbers(Base):
    __tablename__ = 'tIdentifierLatestNumbers'
    __table_args__ = (
        PrimaryKeyConstraint('IdentifierTableName', 'IdentifierID', 'IdentifierGUID', name='PK_tIdentifierLatestNumbers'),
        Index('IX_tIdentifierLatestNumbers_IdentifierGUID', 'IdentifierGUID', mssql_clustered=False, mssql_include=[])
    )

    IdentifierTableName: Mapped[str] = mapped_column(CHAR(80, 'Latin1_General_CI_AS'), primary_key=True)
    IdentifierID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    IdentifierGUID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))


class TIdentifierLatestNumberstPurchases(Base):
    __tablename__ = 'tIdentifierLatestNumberstPurchases'
    __table_args__ = (
        PrimaryKeyConstraint('IdentifierID', name='PK_tIdentifierLatestNumberstPurchases'),
        Index('IX_tIdentifierLatestNumberstPurchases_IdentifierGUID', 'IdentifierGUID', mssql_clustered=False, mssql_include=[])
    )

    IdentifierID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    IdentifierGUID: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('(newid())'))


class TIdentifierLatestNumberstRICGPDAPalletBuildDetails(Base):
    __tablename__ = 'tIdentifierLatestNumberstRICG_PDA_Pallet_Build_Details'
    __table_args__ = (
        PrimaryKeyConstraint('IdentifierID', name='PK_tIdentifierLatestNumberstRICG_PDA_Pallet_Build_Details'),
        Index('IX_tIdentifierLatestNumberstRICG_PDA_Pallet_Build_Details_IdentifierGUID', 'IdentifierGUID', mssql_clustered=False, mssql_include=[])
    )

    IdentifierID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    IdentifierGUID: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('(newid())'))


class TIdentifierLatestNumberstRecycling4ScrapRef(Base):
    __tablename__ = 'tIdentifierLatestNumberstRecycling4_ScrapRef'
    __table_args__ = (
        PrimaryKeyConstraint('IdentifierID', name='PK_tIdentifierLatestNumberstRecycling4_ScrapRef'),
        Index('IX_tIdentifierLatestNumberstRecycling4_ScrapRef_IdentifierGUID', 'IdentifierGUID', mssql_clustered=False, mssql_include=[])
    )

    IdentifierID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    IdentifierGUID: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('(newid())'))


class TIdentifierLatestNumberstSales(Base):
    __tablename__ = 'tIdentifierLatestNumberstSales'
    __table_args__ = (
        PrimaryKeyConstraint('IdentifierID', name='PK_tIdentifierLatestNumberstSales'),
        Index('IX_tIdentifierLatestNumberstSales_IdentifierGUID', 'IdentifierGUID', mssql_clustered=False, mssql_include=[])
    )

    IdentifierID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    IdentifierGUID: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('(newid())'))


class TIdentifierLatestNumberstTransfers(Base):
    __tablename__ = 'tIdentifierLatestNumberstTransfers'
    __table_args__ = (
        PrimaryKeyConstraint('IdentifierID', name='PK_tIdentifierLatestNumberstTransfers'),
        Index('IX_tIdentifierLatestNumberstTransfers_IdentifierGUID', 'IdentifierGUID', mssql_clustered=False, mssql_include=[])
    )

    IdentifierID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    IdentifierGUID: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('(newid())'))


class TInventoryLocations(Base):
    __tablename__ = 'tInventoryLocations'
    __table_args__ = (
        PrimaryKeyConstraint('LocID', name='PK_tInventoryLocations'),
    )

    LocID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    LevelID1: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    LevelID2: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    LevelID3: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    LevelID4: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    LevelID5: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    LevelID6: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    LevelID7: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    Description: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    Multiplier: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False, server_default=text('((1))'))
    Order: Mapped[int] = mapped_column(SmallInteger, nullable=False)


class TItemCustExtraData(Base):
    __tablename__ = 'tItemCustExtraData'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', 'CardRecordID', name='PK_tItemCustExtraData'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ExtraICD1: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    ExtraICD2: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    ExtraICD3: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    ExtraICD4: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


t_tItemExtraDataNames = Table(
    'tItemExtraDataNames', Base.metadata,
    Column('ExtraD1Name', CHAR(20, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('Extra Data 1')")),
    Column('ExtraD2Name', CHAR(20, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('Extra Data 2')")),
    Column('ExtraD3Name', CHAR(20, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('Extra Data 3')")),
    Column('ExtraD4Name', CHAR(20, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('Extra Data 4')"))
)


class TItemLocations(Base):
    __tablename__ = 'tItemLocations'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', 'LocID', name='PK_tItemLocations'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LocID: Mapped[int] = mapped_column(Integer, primary_key=True)


t_tItemPriceMatrix = Table(
    'tItemPriceMatrix', Base.metadata,
    Column('PriceID', Integer, Identity(start=1, increment=1), nullable=False),
    Column('SupplierID', Integer),
    Column('ItemID', Unicode(23, 'Latin1_General_CI_AS'), nullable=False),
    Column('StartDate', DateTime, nullable=False),
    Column('EndDate', DateTime, nullable=False),
    Column('ItemPriceEx', Float(53)),
    Column('ItemPriceInc', Float(53)),
    Index('IX_tItemPriceMatrix_ItemID', 'ItemID', mssql_clustered=False, mssql_include=[]),
    Index('IX_tItemPriceMatrix_SupplierID', 'SupplierID', mssql_clustered=False, mssql_include=[])
)


class TItemPrices(Base):
    __tablename__ = 'tItemPrices'
    __table_args__ = (
        PrimaryKeyConstraint('ItemPriceID', name='PK_tItemPrices'),
        Index('IX_tItemPrices_ChangeControl_RICG', 'ChangeControl_RICG', mssql_clustered=False, mssql_include=[]),
        Index('IX_tItemPrices_ItemID', 'ItemID', mssql_clustered=False, mssql_include=[])
    )

    ItemPriceID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ItemID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    QuantityBreak: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    QuantityBreakAmount: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    PriceLevel: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    PriceLevelNameID: Mapped[str] = mapped_column(CHAR(3, 'Latin1_General_CI_AS'), nullable=False)
    SellingPrice: Mapped[Any] = mapped_column(MONEY, nullable=False)
    PriceIsInclusive: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    ChangeControl: Mapped[str] = mapped_column(String(10, 'Latin1_General_CI_AS'), nullable=False)
    ChangeControl_RICG: Mapped[Optional[int]] = mapped_column(BigInteger)


class TItemPurchaseLines(Base):
    __tablename__ = 'tItemPurchaseLines'
    __table_args__ = (
        PrimaryKeyConstraint('ItemPurchaseLineID', name='PK_tItemPurchaseLines'),
        Index('IX_tItemPurchaseLines_X_POLINEID', 'X_POLINEID', mssql_clustered=False, mssql_include=[])
    )

    ItemPurchaseLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PurchaseLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    PurchaseID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    Min: Mapped[Optional[float]] = mapped_column(Float(53))
    Max: Mapped[Optional[float]] = mapped_column(Float(53))
    QOH: Mapped[Optional[float]] = mapped_column(Float(53))
    QOO: Mapped[Optional[float]] = mapped_column(Float(53))
    QOSO: Mapped[Optional[float]] = mapped_column(Float(53))
    StockCode: Mapped[Optional[str]] = mapped_column(Unicode(23, 'Latin1_General_CI_AS'))
    Sales1: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales2: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales3: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales4: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales5: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales6: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales7: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales8: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales9: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales10: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales11: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales12: Mapped[Optional[float]] = mapped_column(Float(53))
    OriginalQOH: Mapped[Optional[float]] = mapped_column(Float(53))
    X_POLINEID: Mapped[Optional[int]] = mapped_column(Integer)


class TItemSaleLineBarcodes(Base):
    __tablename__ = 'tItemSaleLineBarcodes'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'SaleLineBarcodeID', name='PK_tItemSaleLineBarcodes'),
        Index('IX_tItemSaleLineBarcodes_Barcode', 'Barcode', mssql_clustered=False, mssql_include=[])
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineBarcodeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Barcode: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Latin1_General_CI_AS'))
    Tag1: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    Tag2: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    Tag3: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    ExpiryDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))


class TItemSaleLines(Base):
    __tablename__ = 'tItemSaleLines'
    __table_args__ = (
        PrimaryKeyConstraint('ItemSaleLineID', name='PK_tItemSaleLines'),
        Index('IX_tItemSaleLines_SaleID', 'SaleID', mssql_clustered=False, mssql_include=[]),
        Index('IX_tItemSaleLines_X_SOLINEID', 'X_SOLINEID', mssql_clustered=False, mssql_include=[])
    )

    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesTaxCalBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemPriceContainedTax: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    LocationID: Mapped[Optional[int]] = mapped_column(Integer)
    OriginalQtyOrdered: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyPicked: Mapped[Optional[float]] = mapped_column(Float(53))
    BOQty: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyintoMYOB: Mapped[Optional[float]] = mapped_column(Float(53))
    ExtraBinCode: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_SOLINEID: Mapped[Optional[int]] = mapped_column(Integer)
    PickingStatus: Mapped[Optional[int]] = mapped_column(Integer)
    DivNo: Mapped[Optional[int]] = mapped_column(Integer)
    CartonsUsed: Mapped[Optional[int]] = mapped_column(Integer)
    OverRide4PickingItemNumber: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    OverRide4PickingBarCode1: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    OverRide4PickingQty2BPicked: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    OverRide4PickingPackAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    BoxNo: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    PickedBYID: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    TimeSalePicked: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    OST_SYSUNIQUEID_DELLINE: Mapped[Optional[int]] = mapped_column(Integer)
    OST_GUID_RECEIPT: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    Min: Mapped[Optional[float]] = mapped_column(Float(53))
    Max: Mapped[Optional[float]] = mapped_column(Float(53))
    QOH: Mapped[Optional[float]] = mapped_column(Float(53))
    QOO: Mapped[Optional[float]] = mapped_column(Float(53))
    QOSO: Mapped[Optional[float]] = mapped_column(Float(53))
    StockCode: Mapped[Optional[str]] = mapped_column(Unicode(23, 'Latin1_General_CI_AS'))
    Sales1: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales2: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales3: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales4: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales5: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales6: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales7: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales8: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales9: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales10: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales11: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales12: Mapped[Optional[float]] = mapped_column(Float(53))
    OriginalQOH: Mapped[Optional[float]] = mapped_column(Float(53))
    X_OST_SALESYSUNIQUEID: Mapped[Optional[int]] = mapped_column(BigInteger)
    CartonCount: Mapped[Optional[int]] = mapped_column(SmallInteger)
    PickingDespatchArea: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    BatchCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    REVISIONNO: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    BOMTYPE: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    KITSEQNO: Mapped[Optional[int]] = mapped_column(Integer)
    KITHeaderYN: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    KITHeaderCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    SIZECODE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    COLOURCODE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))


class TItemSaleLines03(Base):
    __tablename__ = 'tItemSaleLines03'
    __table_args__ = (
        PrimaryKeyConstraint('ItemSaleLineID', name='PK_tItemSaleLines03'),
    )

    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesTaxCalBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemPriceContainedTax: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    LocationID: Mapped[Optional[int]] = mapped_column(Integer)
    OriginalQtyOrdered: Mapped[Optional[float]] = mapped_column(Float(53))
    BOQty: Mapped[Optional[float]] = mapped_column(Float(53))
    OverRide4PickingItemNumber: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    OverRide4PickingBarCode1: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    OverRide4PickingQty2BPicked: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    OverRide4PickingPackAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))


class TItemSaleLinesAllocationsNew(Base):
    __tablename__ = 'tItemSaleLinesAllocationsNew'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'GReceiptID', 'GReceiptLineNo', 'GReceiptLineNoAlloc', name='PK_tItemSaleLinesAllocationsNew'),
        Index('IX_tItemSaleLinesAllocationsNew_GReceiptID', 'GReceiptID', mssql_clustered=False, mssql_include=[])
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    GReceiptID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    GReceiptLineNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    GReceiptLineNoAlloc: Mapped[int] = mapped_column(Integer, primary_key=True)
    LocationID: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    LocationBinID: Mapped[int] = mapped_column(Integer, nullable=False)
    Quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    Batch_Serial_No: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Expiry_Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TItemSaleLinesHold(Base):
    __tablename__ = 'tItemSaleLinesHold'
    __table_args__ = (
        PrimaryKeyConstraint('ItemSaleLineID', name='PK_tItemSaleLinesHold'),
    )

    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesTaxCalBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)


class TItemSaleLinesPallets(Base):
    __tablename__ = 'tItemSaleLinesPallets'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'SSCCBarcode', name='PK_tItemSaleLinesPallets'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ItemNumber: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)
    SSCCBarcode: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    GTINBarcode: Mapped[Optional[str]] = mapped_column(String(100, 'Latin1_General_CI_AS'))
    BatchCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    ExpiryDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CartonsUsed: Mapped[Optional[int]] = mapped_column(Integer)


class TItemSaleLinesTemp(Base):
    __tablename__ = 'tItemSaleLinesTemp'
    __table_args__ = (
        PrimaryKeyConstraint('ItemSaleLineID', name='PK_tItemSaleLinesTemp'),
    )

    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesTaxCalBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)


class TItemSaleLinesTruckAllocations(Base):
    __tablename__ = 'tItemSaleLinesTruckAllocations'
    __table_args__ = (
        PrimaryKeyConstraint('ItemSaleLineID', 'TruckID', name='PK_tItemSaleLinesTruckAllocations'),
    )

    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TruckID: Mapped[str] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'), primary_key=True)
    Units2BShippedPerPallet: Mapped[float] = mapped_column(Float(53), nullable=False)
    Pallets2BShipped: Mapped[float] = mapped_column(Float(53), nullable=False)
    Units2BShipped: Mapped[float] = mapped_column(Float(53), nullable=False)


class TItemSaleLinesWeb(Base):
    __tablename__ = 'tItemSaleLinesWeb'
    __table_args__ = (
        PrimaryKeyConstraint('ItemSaleLineID', name='PK_tItemSaleLinesWeb'),
    )

    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesTaxCalBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    PackSlipPrinted: Mapped[Optional[bool]] = mapped_column(Boolean)
    QtyReceived: Mapped[Optional[int]] = mapped_column(Integer)
    InvoiceClosed: Mapped[Optional[bool]] = mapped_column(Boolean)


class TItems(Base):
    __tablename__ = 'tItems'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', name='PK_tItems'),
        Index('IX_tItems_CatSearch_1', 'CatSearch_1', mssql_clustered=False, mssql_include=[]),
        Index('IX_tItems_CatSearch_2', 'CatSearch_2', mssql_clustered=False, mssql_include=[]),
        Index('IX_tItems_ChangeControl_RICG', 'ChangeControl_RICG', mssql_clustered=False, mssql_include=[]),
        Index('IX_tItems_Change_Control', 'ChangeControl', mssql_clustered=False, mssql_include=[]),
        Index('IX_tItems_CustomField1', 'CustomField1', mssql_clustered=False, mssql_include=[]),
        Index('IX_tItems_CustomField2', 'CustomField2', mssql_clustered=False, mssql_include=[]),
        Index('IX_tItems_CustomField3', 'CustomField3', mssql_clustered=False, mssql_include=[])
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    IsInactive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    ItemNumber: Mapped[str] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'), nullable=False)
    QuantityOnHand: Mapped[float] = mapped_column(Float(53), nullable=False)
    ValueOnHand: Mapped[float] = mapped_column(Float(53), nullable=False)
    SellOnOrder: Mapped[float] = mapped_column(Float(53), nullable=False)
    PurchaseOnOrder: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemIsSold: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    ItemIsBought: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    ItemIsInventoried: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    IncomeAccountID: Mapped[int] = mapped_column(Integer, nullable=False)
    Picture: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    UseDescription: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    BaseSellingPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    PriceIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    SellTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    SalesTaxCalcBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    SellUnitQuantity: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    TaxInclusiveLastPurchasePrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    BuyUnitMeasure: Mapped[str] = mapped_column(Unicode(5, 'Latin1_General_CI_AS'), nullable=False)
    BuyUnitQuantity: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    MinLevelBeforeReorder: Mapped[float] = mapped_column(Float(53), nullable=False)
    ChangeControl: Mapped[str] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'), nullable=False)
    ItemName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    ExpenseAccountID: Mapped[Optional[int]] = mapped_column(Integer)
    InventoryAccountID: Mapped[Optional[int]] = mapped_column(Integer)
    ItemDescription: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    CustomList1ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomList2ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomList3ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomField1: Mapped[Optional[str]] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'))
    CustomField2: Mapped[Optional[str]] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'))
    CustomField3: Mapped[Optional[str]] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'))
    SellUnitMeasure: Mapped[Optional[str]] = mapped_column(Unicode(15, 'Latin1_General_CI_AS'))
    BuyTaxCodeID: Mapped[Optional[int]] = mapped_column(Integer)
    PrimarySupplierID: Mapped[Optional[int]] = mapped_column(Integer)
    SupplierItemNumber: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    DefaultReoderQuantity: Mapped[Optional[float]] = mapped_column(Float(53))
    CustomListName1: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    CustomListText1: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    CustomListName2: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    CustomListText2: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    CustomListName3: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    CustomListText3: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SupplierName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TaxExclusiveLastPurchasePrice: Mapped[Optional[float]] = mapped_column(Float(53))
    TaxPerCentageRate: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    DefaultReorderQuantity: Mapped[Optional[float]] = mapped_column(Float(53))
    TaxExclusiveStandardCost: Mapped[Optional[float]] = mapped_column(Float(53))
    DatapelLocationID: Mapped[Optional[int]] = mapped_column(Integer)
    SellPrice1: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice2: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice3: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice4: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice5: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice6: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice7: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice8: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice9: Mapped[Optional[Any]] = mapped_column(MONEY)
    SellPrice10: Mapped[Optional[Any]] = mapped_column(MONEY)
    BatchTracked: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    SerialTracked: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    X_RICG_Barcode2Multiplier: Mapped[Optional[int]] = mapped_column(SmallInteger)
    X_RICG_Barcode3Multiplier: Mapped[Optional[int]] = mapped_column(SmallInteger)
    DefaultLocationID: Mapped[Optional[int]] = mapped_column(Integer)
    DefaultBinID: Mapped[Optional[int]] = mapped_column(Integer)
    ChangeControl_RICG: Mapped[Optional[int]] = mapped_column(BigInteger)
    CatSearch_1: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    CatSearch_2: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    CatSearch_3: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    CatSearch_4: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    DateLastModified: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))


class TItemsQtyOHTemp(Base):
    __tablename__ = 'tItemsQtyOHTemp'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', name='PK_tItemsQtyOHTemp'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    QtyOnHand: Mapped[Optional[float]] = mapped_column(REAL(24))


class TItemsChinese(Base):
    __tablename__ = 'tItems_Chinese'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', name='PK_tItems_Chinese'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ItemName: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ItemNameInChinese: Mapped[Optional[str]] = mapped_column(Unicode(155, 'Latin1_General_CI_AS'))
    ItemNumber: Mapped[Optional[str]] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'))


class TJobbing4EXOStockTakeHdr(Base):
    __tablename__ = 'tJobbing4EXOStockTake_Hdr'
    __table_args__ = (
        PrimaryKeyConstraint('StockTakeID', name='PK_tJobbing4EXOStockTake_Hdr'),
    )

    StockTakeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LocationNo: Mapped[int] = mapped_column(Integer, nullable=False)
    StockTakeDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)


class TJobbing4EXOStockTakeLines(Base):
    __tablename__ = 'tJobbing4EXOStockTake_Lines'
    __table_args__ = (
        PrimaryKeyConstraint('StockTakeLineID', name='PK_tJobbing4EXOStockTake_Lines'),
    )

    StockTakeLineID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    StockTakeID: Mapped[int] = mapped_column(Integer, nullable=False)
    LocationNo: Mapped[str] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'), nullable=False)
    SupplierID: Mapped[int] = mapped_column(Integer, nullable=False)
    CoilCode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    PackCode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    Mass: Mapped[Optional[float]] = mapped_column(Float(53))
    Barcode: Mapped[Optional[str]] = mapped_column(Unicode(70, 'Latin1_General_CI_AS'))


class TJobs(Base):
    __tablename__ = 'tJobs'
    __table_args__ = (
        PrimaryKeyConstraint('JobID', name='PK_tJobs'),
    )

    JobID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ParentJobID: Mapped[Optional[int]] = mapped_column(Integer)
    IsInactive: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    JobName: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    JobNumber: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    IsHeader: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    JobLevel: Mapped[Optional[int]] = mapped_column(Integer)
    IsTrackingReimburseable: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    JobDescription: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    ContactName: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    Manager: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    PercentCompleted: Mapped[Optional[float]] = mapped_column(Float(53))
    StartDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FinishDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CustomerID: Mapped[Optional[int]] = mapped_column(Integer)


class TJobsHdr(Base):
    __tablename__ = 'tJobs_Hdr'
    __table_args__ = (
        PrimaryKeyConstraint('JobNo', name='PK_tJobs_Hdr'),
    )

    JobNo: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), primary_key=True)
    DateCreated: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    EmployeeID: Mapped[Optional[str]] = mapped_column(Unicode(5, 'Latin1_General_CI_AS'))
    Status: Mapped[Optional[int]] = mapped_column(Integer)
    X_RICG_PutAway_Location: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))


class TJobsLines(Base):
    __tablename__ = 'tJobs_Lines'
    __table_args__ = (
        PrimaryKeyConstraint('JobNo', 'JobLineNo', name='PK_tJobs_Lines'),
        Index('IX_tJobs_Lines_SalesOrderNo', 'SalesOrderNo', mssql_clustered=False, mssql_include=[]),
        Index('IX_tJobs_Lines_Status', 'Status', mssql_clustered=False, mssql_include=[]),
        Index('IX_tJobs_Lines_X_RunNumber', 'X_RunNumber', mssql_clustered=False, mssql_include=[])
    )

    JobNo: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), primary_key=True)
    JobLineNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    SalesOrderNo: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), nullable=False)
    X_RICG_PutAway_Location: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    EmployeeIDRolled: Mapped[Optional[str]] = mapped_column(Unicode(5, 'Latin1_General_CI_AS'))
    EmployeeIDFolded: Mapped[Optional[str]] = mapped_column(Unicode(5, 'Latin1_General_CI_AS'))
    EmployeeIDPutAway: Mapped[Optional[str]] = mapped_column(Unicode(5, 'Latin1_General_CI_AS'))
    EmployeeIDLoaded: Mapped[Optional[str]] = mapped_column(Unicode(5, 'Latin1_General_CI_AS'))
    EmployeeIDDelivered: Mapped[Optional[str]] = mapped_column(Unicode(5, 'Latin1_General_CI_AS'))
    TimeRolled: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TimeFolded: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TimePutAway: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TimeLoaded: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TimeDelivered: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Status: Mapped[Optional[int]] = mapped_column(Integer)
    X_RunNumber: Mapped[Optional[int]] = mapped_column(Integer)
    X_ReasonCodenotLoaded: Mapped[Optional[int]] = mapped_column(Integer)
    X_LOADFAILREASONCODE: Mapped[Optional[int]] = mapped_column(Integer)
    PDA_ID: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))


class TJobsStatus(Base):
    __tablename__ = 'tJobs_Status'
    __table_args__ = (
        PrimaryKeyConstraint('Status', name='PK_tJobs_Status'),
    )

    Status: Mapped[int] = mapped_column(Integer, primary_key=True)
    StatusDesc: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), nullable=False)


t_tKanbanCardData = Table(
    'tKanbanCardData', Base.metadata,
    Column('KanbanUniqueID', Integer, Identity(start=1, increment=1), nullable=False),
    Column('KanbanItemID', CHAR(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanItemName', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanItemNumber', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanItemDescription', CHAR(200, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanItemSupplier', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanSalesLocation', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanRevNo', CHAR(10, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanCardNo', CHAR(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanTubCode', CHAR(10, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanLeadTime', CHAR(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('KanbanReoderQuantity', Integer, nullable=False),
    Column('KanbanVendorKBNo', CHAR(10, 'Latin1_General_CI_AS'), nullable=False),
    Column('SupplierItemNumber', CHAR(50, 'Latin1_General_CI_AS'), nullable=False)
)


class TLatestNumbers(Base):
    __tablename__ = 'tLatestNumbers'
    __table_args__ = (
        PrimaryKeyConstraint('Company_ID', 'LatestNumberType', 'LatestNumberSubType', name='PK_tLatestNumbers'),
    )

    Company_ID: Mapped[str] = mapped_column(CHAR(6, 'Latin1_General_CI_AS'), primary_key=True)
    LatestNumberType: Mapped[str] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'), primary_key=True)
    LatestNumberSubType: Mapped[str] = mapped_column(CHAR(4, 'Latin1_General_CI_AS'), primary_key=True)
    LatestNumber: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False, server_default=text('((0))'))


class TLocationTillMYOBImportCategories(Base):
    __tablename__ = 'tLocationTillMYOBImportCategories'
    __table_args__ = (
        PrimaryKeyConstraint('LocationIdentification', 'TillID', name='PK_tLocationTillMYOBImportCategories'),
    )

    LocationIdentification: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    TillID: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    CategoryData: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    JobData: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))


class TLocations(Base):
    __tablename__ = 'tLocations'
    __table_args__ = (
        PrimaryKeyConstraint('LocationID', name='PK_tLocations'),
    )

    LocationID: Mapped[int] = mapped_column(Integer, primary_key=True)
    IsInactive: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    CanBeSold: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    LocationIdentification: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    LocationName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    Street: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    City: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    State: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    PostCode: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    Country: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Contact: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    ContacPhone: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    Notes: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TLog(Base):
    __tablename__ = 'tLog'
    __table_args__ = (
        PrimaryKeyConstraint('LogID', name='PK_tLog'),
    )

    LogID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Log_Type: Mapped[str] = mapped_column(CHAR(4, 'Latin1_General_CI_AS'), nullable=False)
    Log_Entry_Owner_HRID: Mapped[int] = mapped_column(Integer, nullable=False)
    Server: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Date_created: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    Long_Name: Mapped[Optional[str]] = mapped_column(String(4096, 'Latin1_General_CI_AS'))


class TLog2DPrintQueue(Base):
    __tablename__ = 'tLog2DPrintQueue'
    __table_args__ = (
        PrimaryKeyConstraint('PrintID', name='PK_t2DPrintQueue'),
    )

    PrintID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DateInserted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    BarcodeText: Mapped[str] = mapped_column(String(8000, 'Latin1_General_CI_AS'), nullable=False)
    Printed: Mapped[Optional[bool]] = mapped_column(Boolean)
    DatePrinted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TMYOBBOsLoaded(Base):
    __tablename__ = 'tMYOBBOsLoaded'
    __table_args__ = (
        PrimaryKeyConstraint('MYOBSaleID', name='PK_tMYOBBOsLoaded'),
    )

    MYOBSaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    InvoiceNumber: Mapped[Optional[str]] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'))
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    DateRemoved: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsPrinted: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))


class TMYOBLabelsforDelivery(Base):
    __tablename__ = 'tMYOBLabelsforDelivery'
    __table_args__ = (
        PrimaryKeyConstraint('recseed', name='PK_tMYOBLabelsforDelivery'),
    )

    recseed: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    CardIdentification: Mapped[str] = mapped_column(Unicode(16, 'Latin1_General_CI_AS'), nullable=False)
    Name: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ItemName: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ItemNumber: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    Useby: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    Run: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    OrderRun: Mapped[int] = mapped_column(Integer, nullable=False)
    Qty: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    Notes: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Dept: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    SortField: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    InvoiceNumber: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))


class TMYOBPremierFieldCheck(Base):
    __tablename__ = 'tMYOBPremierFieldCheck'
    __table_args__ = (
        PrimaryKeyConstraint('tablename', 'fieldname', name='PK_tMYOBPremierFieldCheck'),
    )

    tablename: Mapped[str] = mapped_column(CHAR(50, 'Latin1_General_CI_AS'), primary_key=True)
    fieldname: Mapped[str] = mapped_column(CHAR(50, 'Latin1_General_CI_AS'), primary_key=True)
    fieldaction: Mapped[str] = mapped_column(CHAR(2, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('C')"))


class TNonDutyCustomers(Base):
    __tablename__ = 'tNonDutyCustomers'
    __table_args__ = (
        PrimaryKeyConstraint('CustomerID', name='PK_tNonDutyCustomers'),
    )

    CustomerID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Name: Mapped[str] = mapped_column(Unicode(32, 'Latin1_General_CI_AS'), nullable=False)


class TOSTEMPLOYEERATESCALES(Base):
    __tablename__ = 'tOSTEMPLOYEERATESCALES'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTEMPLOYEERATESCALES'),
    )

    RATESCALE: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(Integer, primary_key=True)
    RATESCALEDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    RATESCALEFACTOR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    SYSDATECREATED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSDATEMODIFIED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSUSERCREATED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SYSUSERMODIFIED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TOSTINVENTORYCOUNTLINES(Base):
    __tablename__ = 'tOSTINVENTORYCOUNTLINES'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTINVENTORYCOUNTLINES '),
    )

    COUNTENTERED: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    COUNTNO: Mapped[Optional[int]] = mapped_column(Integer)
    ITEMCODE: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    ITEMDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(100, 'Latin1_General_CI_AS'))
    WAREHOUSECODE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    LOCATIONCODE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    COUNTUNIT: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    SYSTEMQTY: Mapped[Optional[float]] = mapped_column(REAL(24))
    COUNTQTY: Mapped[Optional[float]] = mapped_column(REAL(24))
    SERIALNO: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    EXPIRYDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    BATCHNO: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    REVISIONNO: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    ITEMGRADE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    ITEMCOLOUR: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    ITEMSIZE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    HEADERSYSUNIQUEID: Mapped[Optional[float]] = mapped_column(REAL(24))
    SYSDATECREATED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSDATEMODIFIED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSUSERCREATED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SYSUSERMODIFIED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TOSTINVENTORYCOUNTS(Base):
    __tablename__ = 'tOSTINVENTORYCOUNTS'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTINVENTORYCOUNTS '),
    )

    COUNTNO: Mapped[int] = mapped_column(Integer, nullable=False)
    COUNTSTATUS: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    INCNOCURRENTTRANS: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    COUNTREFERENCE: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    COUNTDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    POSTEDDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FROMWAREHOUSE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    TOWAREHOUSE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    FROMLOCATION: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    TOLOCATION: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    FROMCATEGORY: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    TOCATEGORY: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    FROMITEM: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    TOITEM: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    CYCLECODE: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    ABCCLASS: Mapped[Optional[str]] = mapped_column(String(1, 'Latin1_General_CI_AS'))
    COUNTNOTES: Mapped[Optional[str]] = mapped_column(
        Unicode(16, collation="Latin1_General_CI_AS"),
        nullable=True
    )
    SYSDATECREATED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSDATEMODIFIED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSUSERCREATED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SYSUSERMODIFIED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TOSTItemBarCodes(Base):
    __tablename__ = 'tOSTItemBarCodes'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTitemBarCodes'),
        Index('IX_tOSTItemBarCodes_ITEMBARCODE_ITEMCODE', 'ITEMBARCODE', 'ITEMCODE', mssql_clustered=False, mssql_include=[])
    )

    ITEMCODE: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    ITEMBARCODE: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ITEMUNIT: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    ITEMCOLOUR: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    ITEMSIZE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))


class TOSTItemColours(Base):
    __tablename__ = 'tOSTItemColours'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTItemColours'),
        Index('IX_tOSTItemColours_ITEMCODE', 'ITEMCODE', mssql_clustered=False, mssql_include=[])
    )

    ITEMCODE: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    COLOURCODE: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class TOSTItemRevisions(Base):
    __tablename__ = 'tOSTItemRevisions'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTItemRevisions'),
        Index('IX_tOSTItemRevisions_ITEMCODE_REVISIONDATE', 'ITEMCODE', 'REVISIONDATE', mssql_clustered=False, mssql_include=[])
    )

    ITEMCODE: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    REVISIONNO: Mapped[str] = mapped_column(String(10, 'Latin1_General_CI_AS'), nullable=False)
    REVISIONDATE: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class TOSTItemSizes(Base):
    __tablename__ = 'tOSTItemSizes'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTItemSizes'),
        Index('IX_tOSTItemSizes_ITEMCODE', 'ITEMCODE', mssql_clustered=False, mssql_include=[])
    )

    ITEMCODE: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    SIZECODE: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class TOSTJobTasks(Base):
    __tablename__ = 'tOSTJobTasks'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTJobTasks'),
        Index('IX_tOSTJobTasks_ORDERNUMBER', 'ORDERNUMBER', mssql_clustered=False, mssql_include=[])
    )

    SYSUNIQUEID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ORDERNUMBER: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TASKSEQUENCE: Mapped[Optional[int]] = mapped_column(Integer)
    TASKNAME: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TASKDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TASKSTATUS: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


class TOSTJobs(Base):
    __tablename__ = 'tOSTJobs'
    __table_args__ = (
        PrimaryKeyConstraint('JobID', name='PK_tOSTJobs'),
        Index('IX_tOSTJobs_JobNo', 'JobNo', mssql_clustered=False, mssql_include=[])
    )

    JobID: Mapped[int] = mapped_column(Integer, primary_key=True)
    JobNo: Mapped[Optional[int]] = mapped_column(Integer)
    StartDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DueDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Completed: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    JobCode: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    AccNo: Mapped[Optional[int]] = mapped_column(Integer)
    ExchRate: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    WipLoc: Mapped[Optional[int]] = mapped_column(Integer)
    Name: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Status: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Latin1_General_CI_AS'))
    IsActive: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    DESCRIPTION: Mapped[Optional[str]] = mapped_column(String(1000, 'Latin1_General_CI_AS'))
    Private_Note: Mapped[Optional[str]] = mapped_column(String(1000, 'Latin1_General_CI_AS'))


class TOSTLABOURMASTER(Base):
    __tablename__ = 'tOSTLABOURMASTER'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTLABOURMASTER'),
    )

    SYSUNIQUEID: Mapped[float] = mapped_column(Float(53), primary_key=True)
    LABOURCODE: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    LABOURDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(100, 'Latin1_General_CI_AS'))
    LABOURUNIT: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    LABOURSTATUS: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    LABOURBARCODE: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    LABOURCATEGORY: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    TAXGROUP: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    ANALYSISGROUP: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    PRICINGGROUP: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    COSTCENTRECODE: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    DEPARTMENTCODE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    STDSELLRATE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    STANDARDCOST: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    LABOURDIRECTCOST: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    LABOURFIXEDOHCOST: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    LABOURVAROHPERCENT: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    LASTCOST: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    AVERAGECOST: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    WARRANTYAPPLIES: Mapped[Optional[bool]] = mapped_column(Boolean)
    WARRANTYCODE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    LASTRATEUPDATEDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DAILYCAPACITY: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    LABOURNOTES: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    SALESNOTES: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    JOBNOTES: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    PURCHASENOTES: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    ASSEMBLYNOTES: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    SYSDATECREATED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSDATEMODIFIED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDITIONALFIELD_1: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDITIONALFIELD_2: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDITIONALFIELD_3: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDITIONALFIELD_4: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDITIONALFIELD_5: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDITIONALFIELD_6: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDITIONALFIELD_7: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDITIONALFIELD_8: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ADDITIONALDATEFIELD_1: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDITIONALDATEFIELD_2: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDITIONALDATEFIELD_3: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDITIONALDATEFIELD_4: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDITIONALDATEFIELD_5: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDITIONALDATEFIELD_6: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDITIONALDATEFIELD_7: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDITIONALDATEFIELD_8: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ADDLINECODESTYLE: Mapped[Optional[bool]] = mapped_column(Boolean)
    SYSUSERCREATED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SYSUSERMODIFIED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    LABOURSUBCATEGORY: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    SALESMESSAGE: Mapped[Optional[str]] = mapped_column(String(200, 'Latin1_General_CI_AS'))
    JOBMESSAGE: Mapped[Optional[str]] = mapped_column(String(200, 'Latin1_General_CI_AS'))
    PURCHASEMESSAGE: Mapped[Optional[str]] = mapped_column(String(200, 'Latin1_General_CI_AS'))
    ASSEMBLYMESSAGE: Mapped[Optional[str]] = mapped_column(String(200, 'Latin1_General_CI_AS'))


class TOSTLabourCode(Base):
    __tablename__ = 'tOSTLabourCode'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTLabourCode'),
        Index('IX_tOSTLabourCode_LABOURCODE', 'LABOURCODE', mssql_clustered=False, mssql_include=[])
    )

    SYSUNIQUEID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LABOURCODE: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    LABOURDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(100, 'Latin1_General_CI_AS'))
    LABOURSTATUS: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    LABOURBARCODE: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TOSTLocationMaster(Base):
    __tablename__ = 'tOSTLocationMaster'
    __table_args__ = (
        PrimaryKeyConstraint('WAREHOUSECODE', 'LOCATIONCODE', name='PK_tOSTLocationMaster'),
    )

    WAREHOUSECODE: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), primary_key=True)
    LOCATIONCODE: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), primary_key=True)
    LOCATIONDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    LOCATIONGROUP: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    LOCATIONSEQUENCE: Mapped[Optional[int]] = mapped_column(Integer)
    SYSUNIQUEID: Mapped[Optional[int]] = mapped_column(BigInteger)
    SYSUSERCREATED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SYSUSERMODIFIED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TOSTPURCHASESHIPMENTLINES(Base):
    __tablename__ = 'tOSTPURCHASESHIPMENTLINES'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTPURCHASESHIPMENTLINES'),
        Index('IX_tOSTPURCHASESHIPMENTLINES_SHIPMENTNUMBER_Lines', 'SHIPMENTNUMBER', 'ORDERNUMBER', 'LINENUMBER', 'CODETYPE', 'LINECODE', mssql_clustered=False, mssql_include=[])
    )

    SHIPMENTNUMBER: Mapped[int] = mapped_column(Integer, nullable=False)
    CODETYPE: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    ORDERUNITPRICE: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    SYSUNIQUEID: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ORDERNUMBER: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    CURRENCYCODE: Mapped[Optional[str]] = mapped_column(String(3, 'Latin1_General_CI_AS'))
    LINENUMBER: Mapped[Optional[int]] = mapped_column(Integer)
    LINECODE: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    LINEDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(100, 'Latin1_General_CI_AS'))
    LINEUNIT: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    ORDERQTY: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))


class TOSTPURCHASESHIPMENTORDERS(Base):
    __tablename__ = 'tOSTPURCHASESHIPMENTORDERS'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTPURCHASESHIPMENTORDERS'),
        Index('IX_tOSTPURCHASESHIPMENTORDERS_SHIPMENTNUMBER', 'SHIPMENTNUMBER', 'ORDERNUMBER', mssql_clustered=False, mssql_include=[])
    )

    SHIPMENTNUMBER: Mapped[int] = mapped_column(Integer, nullable=False)
    SYSUNIQUEID: Mapped[float] = mapped_column(Float(53), primary_key=True)
    ORDERNUMBER: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    SUPPLIER: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    CURRENCYCODE: Mapped[Optional[str]] = mapped_column(String(3, 'Latin1_General_CI_AS'))
    EXCHANGERATE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    ORDERDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(100, 'Latin1_General_CI_AS'))


class TOSTPurchaseShipments(Base):
    __tablename__ = 'tOSTPurchaseShipments'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTPurchaseShipments'),
        Index('IX_tOSTPurchaseShipments_SHIPMENTNUMBER', 'SHIPMENTNUMBER', mssql_clustered=False, mssql_include=[])
    )

    SHIPMENTNUMBER: Mapped[int] = mapped_column(Integer, nullable=False)
    SHIPMENTSTATUS: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    SINGLESUPPLIERSHIPMENT: Mapped[int] = mapped_column(Integer, nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SHIPMENTREFERENCE: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    SHIPMENTDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SHIPMENTTYPE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    SHIPMENTMETHOD: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    SHIPMENTETADATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SHIPMENTARRIVALDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DOCUMENTREFERENCE: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    DEPARTUREPORT: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ARRIVALPORT: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SUPPLIER: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


class TOSTSALESTYPES(Base):
    __tablename__ = 'tOSTSALESTYPES'
    __table_args__ = (
        PrimaryKeyConstraint('ORDERTYPE', name='PK_tOSTSALESTYPES'),
    )

    ORDERTYPE: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), primary_key=True)
    ORDERSTATUS: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    ORDERNUMBERING: Mapped[str] = mapped_column(String(10, 'Latin1_General_CI_AS'), nullable=False)
    ORDERSTYLE: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    RENTALORDER: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    TYPEDESCRIPTION: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    ORDERPREFIX: Mapped[Optional[str]] = mapped_column(String(5, 'Latin1_General_CI_AS'))
    SYSDATECREATED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSDATEMODIFIED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSUNIQUEID: Mapped[Optional[int]] = mapped_column(Integer)
    SYSUSERCREATED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SYSUSERMODIFIED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TOSTUSERMASTER(Base):
    __tablename__ = 'tOSTUSERMASTER'
    __table_args__ = (
        PrimaryKeyConstraint('SYSUNIQUEID', name='PK_tOSTUSERMASTER '),
    )

    ADLEVEL: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    SAVEGRIDLAYOUT: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ALLOWLISTCONFIG: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ALLOWAPPROVALS: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    PURCHASEORDERLIMIT: Mapped[Any] = mapped_column(MONEY, nullable=False)
    AUTOREFRESH_1: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    AUTOREFRESH_2: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    AUTOREFRESH_3: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    AUTOREFRESH_4: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ENABLEDESKTOPVIEWS: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ENABLEWORKFLOW: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    STARTONWORKFLOW: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    DISABLEWORKFLOWEDIT: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    ALLOWCHANGINGCUSTOMERPRICE: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    SYSUNIQUEID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    USERNAME: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    FIRSTNAME: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    LASTNAME: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    SYSTEMSTYLE: Mapped[Optional[int]] = mapped_column(Integer)
    PWORD: Mapped[Optional[str]] = mapped_column(String(100, 'Latin1_General_CI_AS'))
    CANNOTCHANGEORDERPRICES: Mapped[Optional[int]] = mapped_column(SmallInteger)
    NOALERTDISPLAYONSTARTUP: Mapped[Optional[int]] = mapped_column(SmallInteger)
    DEFAULTPOSSITENAME: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    VIEWTYPE_1: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    DESKTOPVIEW_1: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    VIEWTYPE_2: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    DESKTOPVIEW_2: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    VIEWTYPE_3: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    DESKTOPVIEW_3: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    VIEWTYPE_4: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    DESKTOPVIEW_4: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    REFRESHINTERVAL_1: Mapped[Optional[int]] = mapped_column(Integer)
    REFRESHINTERVAL_2: Mapped[Optional[int]] = mapped_column(Integer)
    REFRESHINTERVAL_3: Mapped[Optional[int]] = mapped_column(Integer)
    REFRESHINTERVAL_4: Mapped[Optional[int]] = mapped_column(Integer)
    WORKFLOWFILENAME: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    SYSDATECREATED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSDATEMODIFIED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SYSUSERCREATED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    SYSUSERMODIFIED: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TOnOrderbyItemID(Base):
    __tablename__ = 'tOnOrderbyItemID'
    __table_args__ = (
        PrimaryKeyConstraint('ETA', 'ItemID', name='PK_tOnOrderbyItemNumber'),
    )

    ETA: Mapped[str] = mapped_column(CHAR(7, 'Latin1_General_CI_AS'), primary_key=True)
    ItemID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    TotQtyOnOrder: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 3), nullable=False)
    NewOrderAmount: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 3), nullable=False)
    LastPurchaseExTax: Mapped[Any] = mapped_column(MONEY, nullable=False)
    LastPurchaseTaxRate: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    LastNewOrderAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 3))
    Marked: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))


class TOnOrderbyItemIDbyWeek(Base):
    __tablename__ = 'tOnOrderbyItemIDbyWeek'
    __table_args__ = (
        PrimaryKeyConstraint('ETA', 'ItemID', name='PK_tOnOrderbyItemIDbyWeek'),
    )

    ETA: Mapped[str] = mapped_column(CHAR(7, 'Latin1_General_CI_AS'), primary_key=True)
    ItemID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    TotQtyOnOrder: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 3), nullable=False)
    NewOrderAmount: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 3), nullable=False)
    LastPurchaseExTax: Mapped[Any] = mapped_column(MONEY, nullable=False)
    LastPurchaseTaxRate: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    LastNewOrderAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 3))
    Marked: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))


class TOrderStatus(Base):
    __tablename__ = 'tOrderStatus'
    __table_args__ = (
        PrimaryKeyConstraint('OrderStatusCode', name='PK_tOrderStatus'),
    )

    OrderStatusCode: Mapped[str] = mapped_column(CHAR(5, 'Latin1_General_CI_AS'), primary_key=True)
    OrderStatusDesc: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)


class TOverseasCharges(Base):
    __tablename__ = 'tOverseasCharges'
    __table_args__ = (
        PrimaryKeyConstraint('ChargeID', name='PK_tOverseasCharges'),
    )

    ChargeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ChargeDesc: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)


class TOverseasForecastN(Base):
    __tablename__ = 'tOverseasForecastN'
    __table_args__ = (
        PrimaryKeyConstraint('YearMonth', 'ItemNumber', name='PK_tOverseasForecast'),
    )

    YearMonth: Mapped[str] = mapped_column(String(7, 'Latin1_General_CI_AS'), primary_key=True)
    ItemNumber: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), primary_key=True)
    itemid: Mapped[int] = mapped_column(Integer, nullable=False)
    LastCost: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    OpenQOH: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 1), nullable=False)
    QOO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 1), nullable=False)
    BuildRate: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 1), nullable=False)
    BuildNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 1), nullable=False)
    WeeksStock: Mapped[int] = mapped_column(Integer, nullable=False)
    QtyLeft: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 1), nullable=False)
    ProdDaysperMonth: Mapped[int] = mapped_column(Integer, nullable=False)
    ProdDaysperWeek: Mapped[int] = mapped_column(Integer, nullable=False)


class TOverseasReceiptCharges(Base):
    __tablename__ = 'tOverseasReceiptCharges'
    __table_args__ = (
        PrimaryKeyConstraint('ReceiptID', 'ChargeID', name='PK_tReceiptCharges'),
    )

    ReceiptID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ChargeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ChargeAmount: Mapped[float] = mapped_column(Float(53), nullable=False)


class TOverseasSuppliers(Base):
    __tablename__ = 'tOverseasSuppliers'
    __table_args__ = (
        PrimaryKeyConstraint('SupplierID', name='PK_tOverseasSuppliers'),
    )

    SupplierID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Name: Mapped[str] = mapped_column(Unicode(52, 'Latin1_General_CI_AS'), nullable=False)


class TPDAMobilePlusTransfers(Base):
    __tablename__ = 'tPDAMobilePlus_Transfers'
    __table_args__ = (
        PrimaryKeyConstraint('TransferLineGUID', name='PK_tPDAMobilePlus_Transfers'),
    )

    TransferLineGUID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    ITEMCODE: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    UNIT: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    FROMWAREHOUSE: Mapped[Optional[int]] = mapped_column(Integer)
    TOWAREHOUSE: Mapped[Optional[int]] = mapped_column(Integer)
    FROMLOCATION: Mapped[Optional[int]] = mapped_column(Integer)
    TOLOCATION: Mapped[Optional[int]] = mapped_column(Integer)
    TRANSFERQTY: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    SERIALNO: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    Reference: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    EXPIRYDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    BATCHNO: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    datetimeInserted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))
    IsImported: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    BATCHNO_TO: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    EXPIRYDATE_TO: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DeviceName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TransferID: Mapped[Optional[int]] = mapped_column(Integer)


class TPOSCustomerItemPricing(Base):
    __tablename__ = 'tPOSCustomerItemPricing'
    __table_args__ = (
        PrimaryKeyConstraint('CardRecordID', 'ItemID', name='PK_tPOSCustomerItemPricing'),
    )

    CardRecordID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)


class TPOSDenominations(Base):
    __tablename__ = 'tPOSDenominations'
    __table_args__ = (
        PrimaryKeyConstraint('POSTenderDenominations', name='PK_tPOSDenominations'),
    )

    POSTenderDenominations: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DenominationCode: Mapped[str] = mapped_column(CHAR(4, 'Latin1_General_CI_AS'), nullable=False)
    DenominationValue: Mapped[Any] = mapped_column(MONEY, nullable=False)
    DenominationLabel: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    Order: Mapped[Optional[int]] = mapped_column(SmallInteger)


class TPackageType(Base):
    __tablename__ = 'tPackageType'
    __table_args__ = (
        PrimaryKeyConstraint('PackageTypeID', name='PK_tPackageType'),
    )

    PackageTypeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PackageType: Mapped[str] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'), nullable=False)


class TPackageWeights(Base):
    __tablename__ = 'tPackageWeights'
    __table_args__ = (
        PrimaryKeyConstraint('PackageTieBreaker', 'SaleID', 'SalePackID', name='PK_tPackageWeights'),
    )

    PackageTieBreaker: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SalePackID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PackageWeight: Mapped[float] = mapped_column(Float(53), nullable=False)


class TParameters(Base):
    __tablename__ = 'tParameters'
    __table_args__ = (
        PrimaryKeyConstraint('ParmType', name='PK_tParameters'),
    )

    ParmType: Mapped[str] = mapped_column(CHAR(4, 'Latin1_General_CI_AS'), primary_key=True)
    BuildRateperDay: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 1), nullable=False)


t_tPickAudit = Table(
    'tPickAudit', Base.metadata,
    Column('DatePicked', DateTime),
    Column('InvoiceNumber', Unicode(8, 'Latin1_General_CI_AS'))
)


class TPremierConstants(Base):
    __tablename__ = 'tPremierConstants'
    __table_args__ = (
        PrimaryKeyConstraint('Type', 'TypeNo', name='PK_tPremierConstants'),
    )

    Type: Mapped[str] = mapped_column(CHAR(50, 'Latin1_General_CI_AS'), primary_key=True)
    TypeNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    Text: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


t_tPremierInvoiceSpecialTerms = Table(
    'tPremierInvoiceSpecialTerms', Base.metadata,
    Column('PaymentsTerms', String(255, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('If paid by end of month, pay only ~~SP~~ ')")),
    Column('PaymentDiscountPercentage', Numeric(18, 4), nullable=False, server_default=text('((3.0))')),
    Column('DaysAllowed', Integer, nullable=False, server_default=text('((7))'))
)


class TPremierPOSBarcodes(Base):
    __tablename__ = 'tPremierPOSBarcodes'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', name='PK_tPremierPOSBarcodes'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Barcode: Mapped[int] = mapped_column(BigInteger, nullable=False)


class TPremierPOSCashup(Base):
    __tablename__ = 'tPremierPOSCashup'
    __table_args__ = (
        PrimaryKeyConstraint('CashupDate', name='PK_tPremierPOSCashup'),
    )

    OpeningFloat: Mapped[float] = mapped_column(Float(53), nullable=False)
    CashupDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    ClosingFloat: Mapped[Optional[float]] = mapped_column(Float(53))
    TransPaymentTtl: Mapped[Optional[float]] = mapped_column(Float(53))
    CashupPaymentTtl: Mapped[Optional[float]] = mapped_column(Float(53))


t_tPremierPOSCashupTrans = Table(
    'tPremierPOSCashupTrans', Base.metadata,
    Column('PaymentMethodID', Integer, nullable=False),
    Column('PaymentMethodAmt', Float(53), nullable=False),
    Column('CashupDate', DateTime)
)


class TPremierPOSDelivery(Base):
    __tablename__ = 'tPremierPOSDelivery'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tPremierPOSDelivery'),
        Index('IX_tPremierPOSDelivery_ConsignmentNo', 'ConsignmentNo', mssql_clustered=False, mssql_include=[])
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    DeliveryDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    RunNo: Mapped[str] = mapped_column(CHAR(15, 'Latin1_General_CI_AS'), nullable=False)
    FreightCompany: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    ConsignmentNo: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)


class TPremierPOSFreightInformation(Base):
    __tablename__ = 'tPremierPOSFreightInformation'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tPremierPOSFreightInformation'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ShippingCost: Mapped[Optional[float]] = mapped_column(Float(53))
    ShippingInsurance: Mapped[Optional[float]] = mapped_column(Float(53))
    SaleOrderNo: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    AustralianPartNo: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


class TPremierPOSInventoryStats(Base):
    __tablename__ = 'tPremierPOSInventoryStats'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', 'ILocID', name='PK_tPremierPOSInventoryStats'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ILocID: Mapped[int] = mapped_column(Integer, primary_key=True)
    QtyonHand: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)


class TPremierPOSItemQtyLocations(Base):
    __tablename__ = 'tPremierPOSItemQtyLocations'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'ILocID', name='PK_tPremierPOSItemQtyLocations'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ILocID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    Multiplier: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)


class TPremierPOSItemQtyLocations03(Base):
    __tablename__ = 'tPremierPOSItemQtyLocations03'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'ILocID', name='PK_tPremierPOSItemQtyLocations03'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ILocID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    Multiplier: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)


class TPremierPOSItemSalesPrompt(Base):
    __tablename__ = 'tPremierPOSItemSalesPrompt'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', name='PK_tPremierPOSItemSalesPrompt'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SalesPrompt: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TPremierPOSItemSerials(Base):
    __tablename__ = 'tPremierPOSItemSerials'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'SerialNumber1', name='PK_tPremierPOSItemSerials'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SerialNumber1: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    SerialNumber2: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)


class TPremierPOSItemSerials03(Base):
    __tablename__ = 'tPremierPOSItemSerials03'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'SerialNumber1', name='PK_tPremierPOSItemSerials03'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SerialNumber1: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    SerialNumber2: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)


class TPremierPOSJewellery(Base):
    __tablename__ = 'tPremierPOSJewellery'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tPremierPOSJewellery'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    DiamondWeightPerItem: Mapped[Optional[float]] = mapped_column(Float(53))
    StoneWeightPerItem: Mapped[Optional[float]] = mapped_column(Float(53))
    MetalWeightPerItem: Mapped[Optional[float]] = mapped_column(Float(53))
    GoldWeightPerItem: Mapped[Optional[float]] = mapped_column(Float(53))
    NetWeight: Mapped[Optional[float]] = mapped_column(Float(53))
    GrossWeightOfShipment: Mapped[Optional[float]] = mapped_column(Float(53))
    MetalGoldWeightPerItem: Mapped[Optional[float]] = mapped_column(Float(53))


class TPremierPOSJewelleryL(Base):
    __tablename__ = 'tPremierPOSJewelleryL'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'LineNumber', name='PK_tPremierPOSJewelleryL'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LineNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    DiamondWeightPerItem: Mapped[float] = mapped_column(Float(53), nullable=False)
    StoneWeightPerItem: Mapped[float] = mapped_column(Float(53), nullable=False)
    MetalGoldWeightPerItem: Mapped[float] = mapped_column(Float(53), nullable=False)
    GrossWeightOfShipment: Mapped[float] = mapped_column(Float(53), nullable=False)
    NetWeight: Mapped[float] = mapped_column(Float(53), nullable=False)


class TPremierPOSJobs(Base):
    __tablename__ = 'tPremierPOSJobs'
    __table_args__ = (
        PrimaryKeyConstraint('JobID', name='PK_tPremierPOSJobs'),
    )

    JobID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ParentJobID: Mapped[Optional[int]] = mapped_column(Integer)
    IsInactive: Mapped[Optional[bool]] = mapped_column(Boolean)
    JobName: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    JobNumber: Mapped[Optional[str]] = mapped_column(String(15, 'Latin1_General_CI_AS'))
    IsHeader: Mapped[Optional[bool]] = mapped_column(Boolean)
    JobLevel: Mapped[Optional[int]] = mapped_column(Integer)
    IsTrackingReimburseable: Mapped[Optional[bool]] = mapped_column(Boolean)
    JobDescription: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    ContactName: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    Manager: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    PercentCompleted: Mapped[Optional[float]] = mapped_column(Float(53))
    StartDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FinishDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CustomerID: Mapped[Optional[int]] = mapped_column(Integer)


class TPremierPOSMovements(Base):
    __tablename__ = 'tPremierPOSMovements'
    __table_args__ = (
        PrimaryKeyConstraint('MovID', name='PK_tPremierPOSMovements'),
    )

    MovID: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1), primary_key=True)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    ILocID: Mapped[int] = mapped_column(Integer, nullable=False)
    ILocIDTo: Mapped[int] = mapped_column(Integer, nullable=False)
    MovType: Mapped[str] = mapped_column(CHAR(2, 'Latin1_General_CI_AS'), nullable=False)
    MovAudit: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), nullable=False)
    MovDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    MovQty: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False, server_default=text('((0))'))
    Processed: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    ProcessedDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Description: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


class TPremierPOSOptions(Base):
    __tablename__ = 'tPremierPOSOptions'
    __table_args__ = (
        PrimaryKeyConstraint('OptionIDKey', name='PK_tPremierPOSOptions'),
    )

    OptionIDKey: Mapped[int] = mapped_column(Integer, primary_key=True)
    DepositAmt: Mapped[float] = mapped_column(Float(53), nullable=False)


class TPremierPOSPurchaseLocationQtyBreakdowns(Base):
    __tablename__ = 'tPremierPOSPurchaseLocationQtyBreakdowns'
    __table_args__ = (
        PrimaryKeyConstraint('PurchaseID', 'PurchaseLineID', 'LocID', name='PK_tPremierPOSPurchaseLocationQtyBreakdowns'),
    )

    PurchaseID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PurchaseLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LocID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Qty: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)


class TPremierPOSRuns(Base):
    __tablename__ = 'tPremierPOSRuns'
    __table_args__ = (
        PrimaryKeyConstraint('RunNo', name='PK_tPremierPOSRuns'),
    )

    RunNo: Mapped[str] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'), primary_key=True)
    ValidDays: Mapped[str] = mapped_column(String(7, 'Latin1_General_CI_AS'), nullable=False)


class TPremierPOSSerialRegister(Base):
    __tablename__ = 'tPremierPOSSerialRegister'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', 'SerialNumber1', name='PK_tPremierPOSSerialRegister'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SerialNumber1: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    SerialNumber2: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    DateReceived: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    PurchaseID: Mapped[Optional[int]] = mapped_column(Integer)
    PurchaseOrderNumber: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    ReceiptNumber: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    SaleIDSold: Mapped[Optional[int]] = mapped_column(Integer)
    InvoiceNumberSold: Mapped[Optional[str]] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'))
    SaleIDReturned: Mapped[Optional[int]] = mapped_column(Integer)
    InvoiceNumberReturned: Mapped[Optional[str]] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'))
    DateSold: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TPremierPOSTenderTrans(Base):
    __tablename__ = 'tPremierPOSTenderTrans'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'TenderID', name='PK_tPremierPOSTenderTrans'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TenderID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TenderAmount: Mapped[Optional[float]] = mapped_column(Float(53))
    TransDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    UserID: Mapped[Optional[int]] = mapped_column(Integer)
    TILL: Mapped[Optional[int]] = mapped_column(Integer)
    ActualTendered: Mapped[Optional[float]] = mapped_column(Float(53))


class TPremierPOSTenderTrans03(Base):
    __tablename__ = 'tPremierPOSTenderTrans03'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'TenderID', name='PK_tPremierPOSTenderTrans03'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TenderID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TenderAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TransDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    UserID: Mapped[int] = mapped_column(Integer, nullable=False)
    TILL: Mapped[int] = mapped_column(Integer, nullable=False)
    ActualTendered: Mapped[float] = mapped_column(Float(53), nullable=False)


class TPremierPOSTenderTypes(Base):
    __tablename__ = 'tPremierPOSTenderTypes'
    __table_args__ = (
        PrimaryKeyConstraint('PaymentMethodID', name='PK_tPremierPOSTenderTypes'),
    )

    PaymentMethodID: Mapped[int] = mapped_column(Integer, primary_key=True)
    MethodCode: Mapped[str] = mapped_column(CHAR(255, 'Latin1_General_CI_AS'), nullable=False)
    MethodType: Mapped[str] = mapped_column(CHAR(11, 'Latin1_General_CI_AS'), nullable=False)


t_tPremierPOSUserSession = Table(
    'tPremierPOSUserSession', Base.metadata,
    Column('UserID', Integer, nullable=False),
    Column('SessionStart', DateTime, nullable=False),
    Column('SessionEnd', DateTime)
)


class TPremierPOSUsers(Base):
    __tablename__ = 'tPremierPOSUsers'
    __table_args__ = (
        PrimaryKeyConstraint('UserID', name='PK_tPremierPOSUsers'),
    )

    UserID: Mapped[int] = mapped_column(Integer, primary_key=True)
    UserName: Mapped[str] = mapped_column(String(30, 'Latin1_General_CI_AS'), nullable=False)
    UserPassword: Mapped[str] = mapped_column(String(15, 'Latin1_General_CI_AS'), nullable=False)
    UserSecurityLevel: Mapped[Optional[str]] = mapped_column(CHAR(2, 'Latin1_General_CI_AS'))


class TPremierPOSAUSPostCodesMyPOS4(Base):
    __tablename__ = 'tPremierPOS_AUS_PostCodes_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('PostCode', 'Locality', name='PK_tPremierPOS_AUS_PostCodes_MyPOS4'),
    )

    PostCode: Mapped[str] = mapped_column(String(10, 'Latin1_General_CI_AS'), primary_key=True)
    Locality: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    State: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)
    ChangeControl_RICG: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1), nullable=False)
    ParcelZone: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))


class TPremierPOSCustomersMyPOS4(Base):
    __tablename__ = 'tPremierPOS_Customers_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('myPOS4_ID', name='PK_tPremierPOS_Customers_MyPOS4'),
        Index('IX_tPremierPOS_Customers_MyPOS4_ChangeControl_RICG', 'ChangeControl_RICG', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Customers_MyPOS4_CustomerID', 'CustomerID', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Customers_MyPOS4_Name', 'Name', mssql_clustered=False, mssql_include=[])
    )

    myPOS4_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    CustomerID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    CardIdentification: Mapped[str] = mapped_column(Unicode(16, 'Latin1_General_CI_AS'), nullable=False)
    Name: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    LastName: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    FirstName: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    IsIndividual: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    IsInactive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    UseCustomerTaxCode: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    CreditLimit: Mapped[float] = mapped_column(Float(53), nullable=False)
    CurrentBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    ChangeControl: Mapped[str] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'), nullable=False)
    CardRecordID: Mapped[Optional[int]] = mapped_column(BigInteger)
    CurrencyID: Mapped[Optional[int]] = mapped_column(Integer)
    Notes: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Identifiers: Mapped[Optional[str]] = mapped_column(Unicode(26, 'Latin1_General_CI_AS'))
    IdentifierID: Mapped[Optional[str]] = mapped_column(Unicode(26, 'Latin1_General_CI_AS'))
    CustomList1ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomList2ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomList3ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomField1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    CustomField2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    CustomField3: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    TermsID: Mapped[Optional[int]] = mapped_column(Integer)
    PriceLevelID: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    FreightTaxCodeID: Mapped[Optional[int]] = mapped_column(Integer)
    ACCNO: Mapped[Optional[int]] = mapped_column(Integer)
    ONHOLD: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    Street: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    City: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    State: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    PostCode: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Country: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Phone1: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Phone2: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Phone3: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Fax: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Email: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    WWW: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Salutation: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    ContactName: Mapped[Optional[str]] = mapped_column(CHAR(50, 'Latin1_General_CI_AS'))
    StreetLine1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    StreetLine2: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    StreetLine3: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    StreetLine4: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    VolumeDiscount: Mapped[Optional[float]] = mapped_column(Float(53))
    DateLastModified: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))
    ChangeControl_RICG: Mapped[Optional[int]] = mapped_column(BigInteger)


class TPremierPOSEmailConfigListsMyPOS4(Base):
    __tablename__ = 'tPremierPOS_Email_Config_Lists_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('ProgramGroup', 'EmailAddress', name='PK_tPremierPOS_Email_Config_Lists_MyPOS4'),
    )

    ProgramGroup: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    EmailAddress: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), primary_key=True)


class TPremierPOSExtraFieldConfigListsMyPOS4(Base):
    __tablename__ = 'tPremierPOS_ExtraField_Config_Lists_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('ProgramGroup', name='PK_tPremierPOS_ExtraField_Config_Lists_MyPOS4'),
    )

    ProgramGroup: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), primary_key=True)
    FieldName: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)


class TPremierPOSItemLocationsMyPOS4(Base):
    __tablename__ = 'tPremierPOS_ItemLocations_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('ItemLocationID', name='PK_tPremierPOS_ItemLocations_MyPOS4'),
        Index('IX_tPremierPOS_ItemLocations_MyPOS4_ItemID', 'ItemID', mssql_clustered=False, mssql_include=[])
    )

    ItemLocationID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    LocationID: Mapped[int] = mapped_column(Integer, nullable=False)
    QuantityOnHand: Mapped[Optional[float]] = mapped_column(Float(53))
    SellOnOrder: Mapped[Optional[float]] = mapped_column(Float(53))
    PurchaseOnOrder: Mapped[Optional[float]] = mapped_column(Float(53))


class TPremierPOSItemSaleLinesMyPOS4(Base):
    __tablename__ = 'tPremierPOS_ItemSaleLines_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('myPOS4_ID', 'ItemSaleLineID', name='PK_tPremierPOS_ItemSaleLines_MyPOS4'),
        Index('IX_tPremierPOS_ItemSaleLines_MyPOS4_ItemSaleLineID', 'ItemSaleLineID', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_ItemSaleLines_MyPOS4_SaleID', 'SaleID', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_ItemSaleLines_MyPOS4_StockCode', 'StockCode', mssql_clustered=False, mssql_include=[])
    )

    myPOS4_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesTaxCalBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemPriceContainedTax: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    LocationID: Mapped[Optional[int]] = mapped_column(Integer)
    OriginalQtyOrdered: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyPicked: Mapped[Optional[float]] = mapped_column(Float(53))
    BOQty: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyintoMYOB: Mapped[Optional[float]] = mapped_column(Float(53))
    ExtraBinCode: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_SOLINEID: Mapped[Optional[int]] = mapped_column(Integer)
    PickingStatus: Mapped[Optional[int]] = mapped_column(Integer)
    DivNo: Mapped[Optional[int]] = mapped_column(Integer)
    CartonsUsed: Mapped[Optional[int]] = mapped_column(Integer)
    OverRide4PickingItemNumber: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    OverRide4PickingBarCode1: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    OverRide4PickingQty2BPicked: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    OverRide4PickingPackAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    X_OST_SALESYSUNIQUEID: Mapped[Optional[int]] = mapped_column(BigInteger)
    TimeSalePicked: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickedBYID: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    OriginalQOH: Mapped[Optional[float]] = mapped_column(Float(53))
    OST_SYSUNIQUEID_DELLINE: Mapped[Optional[int]] = mapped_column(Integer)
    OST_GUID_RECEIPT: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    BoxNo: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    OldNewLaybyEditIndicator: Mapped[Optional[str]] = mapped_column(CHAR(3, 'Latin1_General_CI_AS'))
    StockCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))


class TPremierPOSPOSCustomerItemPricingMyPOS4(Base):
    __tablename__ = 'tPremierPOS_POSCustomerItemPricing_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('myPOS4_ID_Customer', 'ItemID', name='PK_tPremierPOS_POSCustomerItemPricing_MyPOS4'),
    )

    myPOS4_ID_Customer: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    myPOS4_ID_Docket: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    DateLastUpdated: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)


class TPremierPOSPricingMatrixMyPOS4(Base):
    __tablename__ = 'tPremierPOS_PricingMatrix_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('SalesCategoryID', 'myPOS4_ID_Customer', name='PK_tPremierPOS_PricingMatrix_MyPOS4'),
        Index('IX_tPremierPOS_PricingMatrix_MyPOS4_ChangeControl_RICG', 'ChangeControl_RICG', mssql_clustered=False, mssql_include=[])
    )

    SalesCategoryID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    myPOS4_ID_Customer: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    PMID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), nullable=False)
    Rule: Mapped[Optional[str]] = mapped_column(CHAR(8, 'Latin1_General_CI_AS'))
    Value: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(18, 4))
    ChangeControl_RICG: Mapped[Optional[int]] = mapped_column(BigInteger)


class TPremierPOSSalesMyPOS4(Base):
    __tablename__ = 'tPremierPOS_Sales_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('myPOS4_ID', name='PK_tPremierPOS_Sales_MyPOS4'),
        Index('IX_tPremierPOS_Sales_MyPOS4_CardRecordID', 'CardRecordID', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Sales_MyPOS4_IsLaybyCompleted', 'IsLaybyCompleted', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Sales_MyPOS4_Latest_Layby_Sale_Guid', 'Latest_Layby_Sale_Guid', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Sales_MyPOS4_LaybyCustomerSearch', 'LaybyCustomerSearch', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Sales_MyPOS4_LaybyNumber', 'LaybyNumber', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Sales_MyPOS4_LaybyStatus', 'LaybyStatus', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Sales_MyPOS4_SaleID', 'SaleID', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Sales_MyPOS4_TransType', 'TransType', mssql_clustered=False, mssql_include=[])
    )

    myPOS4_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    InvoiceNumber: Mapped[Optional[str]] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'))
    CustomerPONumber: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    IsHistorical: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IsThirteenthPeriod: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    ShipToAddress: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine3: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine4: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    InvoiceTypeID: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    InvoiceStatusID: Mapped[Optional[str]] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'))
    Memo: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Comment: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsTaxInclusive: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    IsPrinted: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    CostCentreID: Mapped[Optional[int]] = mapped_column(Integer)
    LinesPurged: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    PreAuditTrail: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    InvoiceDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickingStatus: Mapped[Optional[int]] = mapped_column(SmallInteger)
    PrintCount: Mapped[Optional[int]] = mapped_column(Integer)
    OverrideCustomerName: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine2: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine3: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverridePostCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TimeSalePicked: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickedBYID: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    BOLoaded: Mapped[Optional[bool]] = mapped_column(Boolean)
    OrderStatus: Mapped[Optional[int]] = mapped_column(Integer)
    LocNo: Mapped[Optional[int]] = mapped_column(Integer)
    ProfileID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    OST_POS_Header_SYSUNIQUEID: Mapped[Optional[int]] = mapped_column(BigInteger)
    OST_Direct_Invoice_Number: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    Original_Layby_Sale_Guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    Latest_Layby_Sale_Guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    TenderChange: Mapped[Optional[float]] = mapped_column(Float(53))
    AmounttoPay: Mapped[Optional[float]] = mapped_column(Float(53))
    IsLaybyCompleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    LaybyCompletedDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IsLaybyCancelled: Mapped[Optional[bool]] = mapped_column(Boolean)
    LaybyCancelledDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IsLayby: Mapped[Optional[bool]] = mapped_column(Boolean)
    IsSale: Mapped[Optional[bool]] = mapped_column(Boolean)
    IsTransfer: Mapped[Optional[bool]] = mapped_column(Boolean)
    LocationIdentificationTo: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    IsOrder: Mapped[Optional[bool]] = mapped_column(Boolean)
    IsPayment: Mapped[Optional[bool]] = mapped_column(Boolean)
    UserID: Mapped[Optional[int]] = mapped_column(Integer)
    myPOS4_ID_Customers: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    LocationIdentification: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TillID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TransType: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    IsSent2Host: Mapped[Optional[bool]] = mapped_column(Boolean)
    DateTimeSent2Host: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IsUpdatedonHost: Mapped[Optional[bool]] = mapped_column(Boolean)
    DateTimeUpdatedonHost: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LaybyNumber: Mapped[Optional[int]] = mapped_column(Integer)
    LaybyStatus: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    LaybyCustomerName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    LaybyCustomerSearch: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    ExtraField1: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    DeliveryYN: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    DeliveryWareHouse: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    ExtraField2: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    LaybyCustomerContact1: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    LaybyCustomerAddress1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TPremierPOSSalesMyPOS4EMailLog(Base):
    __tablename__ = 'tPremierPOS_Sales_MyPOS4_EMail_Log'
    __table_args__ = (
        PrimaryKeyConstraint('LogID', name='PK_tPremierPOS_Sales_MyPOS4_EMail_Log'),
    )

    LogID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Log_Type: Mapped[str] = mapped_column(CHAR(4, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('')"))
    Log_Entry_Owner_HRID: Mapped[int] = mapped_column(Integer, nullable=False)
    Server: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Date_created: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    Long_Name: Mapped[Optional[str]] = mapped_column(String(4096, 'Latin1_General_CI_AS'))


class TPremierPOSSalesMyPOS4EMailQ(Base):
    __tablename__ = 'tPremierPOS_Sales_MyPOS4_EMail_Q'
    __table_args__ = (
        PrimaryKeyConstraint('EMailQid', name='PK_tPremierPOS_Sales_MyPOS4_EMail_Q'),
    )

    EMailQid: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    FromEmail: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ToEmail: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Status: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    DateTimeInserted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    EmailSubject: Mapped[Optional[str]] = mapped_column(String(4096, 'Latin1_General_CI_AS'))
    EmailBody: Mapped[Optional[str]] = mapped_column(String(8000, 'Latin1_General_CI_AS'))
    AttachmentPath: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    DateTimePrinted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EmailCC: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TPremierPOSSalesMyPOS4ErrorQ(Base):
    __tablename__ = 'tPremierPOS_Sales_MyPOS4_Error_Q'
    __table_args__ = (
        PrimaryKeyConstraint('ErrorID', name='PK_tPremierPOS_Sales_MyPOS4_Error_Q'),
        Index('IX_tPremierPOS_Sales_MyPOS4_Error_Q_BatchProcessed', 'BatchProcessed', mssql_clustered=False, mssql_include=[]),
        Index('IX_tPremierPOS_Sales_MyPOS4_Error_Q_InvoiceNumber', 'InvoiceNumber', mssql_clustered=False, mssql_include=[])
    )

    ErrorID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Message: Mapped[Optional[str]] = mapped_column(String(1024, 'Latin1_General_CI_AS'))
    DateTimeInserted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ErrorCode: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))
    BatchNo: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    SendEmail: Mapped[Optional[bool]] = mapped_column(Boolean)
    InvoiceNumber: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    MainID: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Memo: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    ErrorType: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))
    BatchProcessed: Mapped[Optional[bool]] = mapped_column(Boolean)


class TPremierPOSTenderTransMyPOS4(Base):
    __tablename__ = 'tPremierPOS_TenderTrans_MyPOS4'
    __table_args__ = (
        PrimaryKeyConstraint('myPOS4_ID', 'TenderTypeID', name='PK_tPremierPOS_TenderTrans_MyPOS4'),
        Index('IX_tPremierPOS_TenderTrans_MyPOS4_SaleID', 'SaleID', mssql_clustered=False, mssql_include=[])
    )

    myPOS4_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    TenderTypeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TenderAmount: Mapped[Optional[float]] = mapped_column(Float(53))
    TransDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    UserID: Mapped[Optional[int]] = mapped_column(Integer)
    TILL: Mapped[Optional[int]] = mapped_column(Integer)
    ActualTendered: Mapped[Optional[float]] = mapped_column(Float(53))


t_tPremierUpdateChanges = Table(
    'tPremierUpdateChanges', Base.metadata,
    Column('TableName', CHAR(15, 'Latin1_General_CI_AS'), nullable=False),
    Column('PrimaryKey', CHAR(25, 'Latin1_General_CI_AS')),
    Column('PrimaryKeyValue', String(50, 'Latin1_General_CI_AS')),
    Column('Key1', CHAR(25, 'Latin1_General_CI_AS')),
    Column('Key1Value', String(50, 'Latin1_General_CI_AS')),
    Column('Key2', CHAR(25, 'Latin1_General_CI_AS')),
    Column('Key2Value', String(25, 'Latin1_General_CI_AS')),
    Column('Key3', CHAR(25, 'Latin1_General_CI_AS')),
    Column('Key3Value', String(50, 'Latin1_General_CI_AS'))
)


class TPricingMatrix(Base):
    __tablename__ = 'tPricingMatrix'
    __table_args__ = (
        PrimaryKeyConstraint('SalesCategoryID', 'CustomerID', name='PK_tPricingMatrix'),
    )

    SalesCategoryID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CustomerID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PMID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), nullable=False)
    Rule: Mapped[Optional[str]] = mapped_column(CHAR(8, 'Latin1_General_CI_AS'))
    Value: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(18, 4))


class TPrintReport(Base):
    __tablename__ = 'tPrintReport'
    __table_args__ = (
        PrimaryKeyConstraint('PrintJobNumber', name='PK_tPrintReport_PrintJobNumber'),
        Index('IX_tPrintReport_Printed', 'Printed', mssql_clustered=False, mssql_include=[])
    )

    PrintJobNumber: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    ReportName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    Criteria1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Criteria2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    DateInserted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Printed: Mapped[Optional[bool]] = mapped_column(Boolean)
    DatePrinted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LabelCount: Mapped[Optional[int]] = mapped_column(Integer)


class TPurchaseLines(Base):
    __tablename__ = 'tPurchaseLines'
    __table_args__ = (
        PrimaryKeyConstraint('PurchaseLineID', name='PK_tPurchaseLines'),
    )

    PurchaseLineID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    PurchaseID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    LineNumber: Mapped[int] = mapped_column(BigInteger, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(CHAR(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)


class TPurchases(Base):
    __tablename__ = 'tPurchases'
    __table_args__ = (
        PrimaryKeyConstraint('PurchaseID', name='PK_tPurchases'),
    )

    PurchaseID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    SupplierInvoiceNumber: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    IsHistorical: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    BackorderPurchaseID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsThirteenthPeriod: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddress: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine1: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine2: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine3: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine4: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    PurchaseTypeID: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    PurchaseStatusID: Mapped[str] = mapped_column(String(2, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDebits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    Memo: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Comment: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsTaxInclusive: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    IsPrinted: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    PurchaseNumber: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CostCentreID: Mapped[Optional[int]] = mapped_column(Integer)
    LinesPurged: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    PreAuditTrail: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    PurchaseDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    GroupNo: Mapped[Optional[int]] = mapped_column(Integer)
    LocNo: Mapped[Optional[int]] = mapped_column(Integer)
    OrderStatus: Mapped[Optional[int]] = mapped_column(Integer)
    LOGINID: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TQuestItemSaleLines(Base):
    __tablename__ = 'tQuestItemSaleLines'
    __table_args__ = (
        PrimaryKeyConstraint('ItemSaleLineID', name='PK_tQuestItemSaleLines'),
    )

    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    LineTypeID: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    Description: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    TaxBasisAmountIsInclusive: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    SalesTaxCalBasisID: Mapped[Optional[str]] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'))
    ExtraBinCode: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_SOLINEID: Mapped[Optional[int]] = mapped_column(Integer)
    PickingStatus: Mapped[Optional[int]] = mapped_column(Integer)
    DivNo: Mapped[Optional[int]] = mapped_column(Integer)
    CartonsUsed: Mapped[Optional[int]] = mapped_column(Integer)
    LocationID: Mapped[Optional[int]] = mapped_column(Integer)
    OriginalQtyOrdered: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyPicked: Mapped[Optional[float]] = mapped_column(Float(53))
    BOQty: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyintoMYOB: Mapped[Optional[float]] = mapped_column(Float(53))
    ItemNumber: Mapped[Optional[str]] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'))


class TQuestJournal(Base):
    __tablename__ = 'tQuestJournal'
    __table_args__ = (
        PrimaryKeyConstraint('JournalID', name='PK_tQuestJournal'),
    )

    JournalID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    QuestSaleID: Mapped[Optional[int]] = mapped_column(Integer)
    MirrorSaleID: Mapped[Optional[int]] = mapped_column(Integer)
    ReceiptNo: Mapped[Optional[int]] = mapped_column(Integer)
    ReceiptDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SaleTotal: Mapped[Optional[float]] = mapped_column(Float(53))


class TQuestJournalAudit(Base):
    __tablename__ = 'tQuestJournalAudit'
    __table_args__ = (
        PrimaryKeyConstraint('AuditID', name='PK_tQuestJournalAudit'),
    )

    AuditID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    JournalID: Mapped[Optional[int]] = mapped_column(Integer)
    ExonetSaleID: Mapped[Optional[int]] = mapped_column(Integer)
    ImportDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Status: Mapped[Optional[bool]] = mapped_column(Boolean)


class TQuestSales(Base):
    __tablename__ = 'tQuestSales'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tQuestSales'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    InvoiceNumber: Mapped[Optional[str]] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'))
    CustomerPONumber: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    IsHistorical: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsThirteenthPeriod: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    ShipToAddress: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine3: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine4: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    InvoiceTypeID: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    InvoiceStatusID: Mapped[Optional[str]] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'))
    Memo: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Comment: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsTaxInclusive: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    IsPrinted: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    CostCentreID: Mapped[Optional[int]] = mapped_column(Integer)
    LinesPurged: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    PreAuditTrail: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    InvoiceDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PrintCount: Mapped[Optional[int]] = mapped_column(Integer)
    PickingStatus: Mapped[Optional[int]] = mapped_column(SmallInteger)


class TREMOTEMYOBOrders(Base):
    __tablename__ = 'tREMOTEMYOBOrders'
    __table_args__ = (
        PrimaryKeyConstraint('OrderHeaderGUID', name='PK_tREMOTEMYOBOrders'),
        Index('IX_tREMOTEMYOBOrders_PDAOrderHeaderGUID', 'PDAOrderHeaderGUID', mssql_clustered=False, mssql_include=[])
    )

    OrderHeaderGUID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    Order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    revision: Mapped[str] = mapped_column(String(10, 'Latin1_General_CI_AS'), nullable=False)
    order_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    due_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    staff_id: Mapped[str] = mapped_column(String(10, 'Latin1_General_CI_AS'), nullable=False)
    supplier_id: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))
    order_suffix: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    comments: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    archive: Mapped[Optional[bool]] = mapped_column(Boolean)
    order_type: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    New_order_id: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Sent2Host: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Sent2HostDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PDAOrderHeaderGUID: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)


class TREMOTEMYOBOrdersLine(Base):
    __tablename__ = 'tREMOTEMYOBOrdersLine'
    __table_args__ = (
        PrimaryKeyConstraint('OrderHeaderGUID', 'Order_id', 'line_id', name='PK_tREMOTEMYOBOrdersLine'),
    )

    OrderHeaderGUID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    line_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    cost_ex: Mapped[Any] = mapped_column(MONEY, nullable=False)
    Stock_id: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    supcode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    cost_inc: Mapped[Optional[Any]] = mapped_column(MONEY)
    goods_tax: Mapped[Optional[str]] = mapped_column(String(4, 'Latin1_General_CI_AS'))
    quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    status: Mapped[Optional[int]] = mapped_column(SmallInteger)
    goods_id: Mapped[Optional[int]] = mapped_column(Integer)
    unitof_measure: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Sent2Host: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Sent2HostDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TREMOTETransCustomer(Base):
    __tablename__ = 'tREMOTETransCustomer'
    __table_args__ = (
        PrimaryKeyConstraint('Company_ID', 'StoreCode', 'PostingDate', 'TransID', name='PK_tREMOTETransCustomer'),
    )

    Company_ID: Mapped[str] = mapped_column(NCHAR(6, 'Latin1_General_CI_AS'), primary_key=True)
    StoreCode: Mapped[str] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'), primary_key=True)
    PostingDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    TransID: Mapped[str] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'), primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    Address1: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    Address2: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    Suburb: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    PostCode: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    FaxNo: Mapped[Optional[str]] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'))
    PhoneNo1: Mapped[Optional[str]] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'))
    PhoneNo2: Mapped[Optional[str]] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'))
    EmailAddress: Mapped[Optional[str]] = mapped_column(NCHAR(50, 'Latin1_General_CI_AS'))
    SalesPerson: Mapped[Optional[str]] = mapped_column(NCHAR(10, 'Latin1_General_CI_AS'))
    ContactName1: Mapped[Optional[str]] = mapped_column(NCHAR(50, 'Latin1_General_CI_AS'))
    DateTimeLastChanged: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AccountCode: Mapped[Optional[str]] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'))
    ShipToName: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    ShipToAddress1: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    ShipToAddress2: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    ShipToSuburb: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    ShipToPostCode: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    Sent2Host: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Sent2HostDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TREMOTETransHeader(Base):
    __tablename__ = 'tREMOTETransHeader'
    __table_args__ = (
        PrimaryKeyConstraint('Company_ID', 'StoreCode', 'PostingDate', 'TransID', name='PK_tREMOTETransHeader'),
    )

    Company_ID: Mapped[str] = mapped_column(NCHAR(6, 'Latin1_General_CI_AS'), primary_key=True)
    StoreCode: Mapped[str] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'), primary_key=True)
    PostingDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    TransID: Mapped[str] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'), primary_key=True)
    TransDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ClosedYN: Mapped[str] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    ClosedBy: Mapped[Optional[str]] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'))
    SaleType: Mapped[Optional[str]] = mapped_column(NCHAR(2, 'Latin1_General_CI_AS'))
    Status: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Cashier: Mapped[Optional[str]] = mapped_column(NCHAR(10, 'Latin1_General_CI_AS'))
    Salesperson: Mapped[Optional[str]] = mapped_column(NCHAR(10, 'Latin1_General_CI_AS'))
    CustomerID: Mapped[Optional[str]] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'))
    Till: Mapped[Optional[str]] = mapped_column(NCHAR(10, 'Latin1_General_CI_AS'))
    OriginalSaleType: Mapped[Optional[str]] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'))
    TransactionTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    VoidYN: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    VoidedTransID: Mapped[Optional[str]] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'))
    DeletedTransaction: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Period: Mapped[Optional[int]] = mapped_column(Integer)
    WeekNo: Mapped[Optional[int]] = mapped_column(Integer)
    WeekStartDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    OriginalTransID: Mapped[Optional[str]] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'))
    Notes: Mapped[Optional[str]] = mapped_column(NCHAR(255, 'Latin1_General_CI_AS'))
    Change: Mapped[Optional[Any]] = mapped_column(MONEY)
    Sent2Host: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Sent2HostDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DueDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Special1: Mapped[Optional[str]] = mapped_column(NCHAR(30, 'Latin1_General_CI_AS'))
    Special2: Mapped[Optional[str]] = mapped_column(NCHAR(30, 'Latin1_General_CI_AS'))
    Special3: Mapped[Optional[str]] = mapped_column(NCHAR(30, 'Latin1_General_CI_AS'))


class TREMOTETransSaleLineSerials(Base):
    __tablename__ = 'tREMOTETransSaleLineSerials'
    __table_args__ = (
        PrimaryKeyConstraint('Company_ID', 'StoreCode', 'PostingDate', 'TransID', 'SaleLineNo', 'SerialBatch', 'ItemNumberThisSerialBatch', name='PK_tREMOTETransSaleLineSerials'),
    )

    Company_ID: Mapped[str] = mapped_column(NCHAR(6, 'Latin1_General_CI_AS'), primary_key=True)
    StoreCode: Mapped[str] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'), primary_key=True)
    PostingDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    TransID: Mapped[str] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'), primary_key=True)
    SaleLineNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    SerialBatch: Mapped[str] = mapped_column(NCHAR(50, 'Latin1_General_CI_AS'), primary_key=True)
    QtyThisSerialBatch: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    ItemNumberThisSerialBatch: Mapped[str] = mapped_column(NCHAR(55, 'Latin1_General_CI_AS'), primary_key=True)
    ExpiryDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Sent2Host: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Sent2HostDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TREMOTETransSaleLines(Base):
    __tablename__ = 'tREMOTETransSaleLines'
    __table_args__ = (
        PrimaryKeyConstraint('Company_ID', 'StoreCode', 'PostingDate', 'TransID', 'SaleLineNo', name='PK_tREMOTETransSaleLines'),
    )

    Company_ID: Mapped[str] = mapped_column(NCHAR(6, 'Latin1_General_CI_AS'), primary_key=True)
    StoreCode: Mapped[str] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'), primary_key=True)
    PostingDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    TransID: Mapped[str] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'), primary_key=True)
    SaleLineNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    SKU: Mapped[str] = mapped_column(NCHAR(50, 'Latin1_General_CI_AS'), nullable=False)
    SaleQty: Mapped[decimal.Decimal] = mapped_column(Numeric(9, 2), nullable=False)
    SaleUnitAmountIncTax: Mapped[Any] = mapped_column(MONEY, nullable=False)
    SaleTaxRate: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    SaleUnitDiscount: Mapped[Any] = mapped_column(MONEY, nullable=False)
    ItemID: Mapped[str] = mapped_column(NCHAR(50, 'Latin1_General_CI_AS'), nullable=False)
    SalesPerson: Mapped[Optional[str]] = mapped_column(NCHAR(10, 'Latin1_General_CI_AS'))
    SaleRRP: Mapped[Optional[Any]] = mapped_column(MONEY)
    SaleTaxUnitAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    SKUDescription: Mapped[Optional[str]] = mapped_column(NCHAR(50, 'Latin1_General_CI_AS'))
    CurrencyCode: Mapped[Optional[str]] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'))
    HOSKU: Mapped[Optional[str]] = mapped_column(NCHAR(50, 'Latin1_General_CI_AS'))
    Cost: Mapped[Optional[Any]] = mapped_column(MONEY)
    Sent2Host: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Sent2HostDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TREMOTETransSaleTenders(Base):
    __tablename__ = 'tREMOTETransSaleTenders'
    __table_args__ = (
        PrimaryKeyConstraint('Company_ID', 'StoreCode', 'PostingDate', 'TransID', 'TenderLine', name='PK_tREMOTETransSaleTenders'),
    )

    Company_ID: Mapped[str] = mapped_column(NCHAR(6, 'Latin1_General_CI_AS'), primary_key=True)
    StoreCode: Mapped[str] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'), primary_key=True)
    PostingDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    TransID: Mapped[str] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'), primary_key=True)
    TenderLine: Mapped[int] = mapped_column(Integer, primary_key=True)
    TenderType: Mapped[str] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'), nullable=False)
    TenderAmount: Mapped[Any] = mapped_column(MONEY, nullable=False)
    TDets1: Mapped[Optional[str]] = mapped_column(NCHAR(30, 'Latin1_General_CI_AS'))
    TDets2: Mapped[Optional[str]] = mapped_column(NCHAR(30, 'Latin1_General_CI_AS'))
    CurrencyCode: Mapped[Optional[str]] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'))
    ForeignTenderAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Search: Mapped[Optional[str]] = mapped_column(NCHAR(50, 'Latin1_General_CI_AS'))
    Sent2Host: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Sent2HostDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TREMOTETransSignature(Base):
    __tablename__ = 'tREMOTETransSignature'
    __table_args__ = (
        PrimaryKeyConstraint('Company_ID', 'StoreCode', 'PostingDate', 'TransID', 'SigFileName', name='PK_tREMOTETransSignature'),
    )

    Company_ID: Mapped[str] = mapped_column(NCHAR(6, 'Latin1_General_CI_AS'), primary_key=True)
    StoreCode: Mapped[str] = mapped_column(NCHAR(4, 'Latin1_General_CI_AS'), primary_key=True)
    PostingDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    TransID: Mapped[str] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'), primary_key=True)
    TransDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    SigFileName: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), primary_key=True)
    SigContents: Mapped[Optional[str]] = mapped_column(String(4000, 'Latin1_General_CI_AS'))
    Sent2Host: Mapped[Optional[str]] = mapped_column(NCHAR(1, 'Latin1_General_CI_AS'))
    Sent2HostDateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TRICGInstall(Base):
    __tablename__ = 'tRICGInstall'
    __table_args__ = (
        PrimaryKeyConstraint('AppCode', name='PK_tRICGInstall'),
    )

    AppCode: Mapped[str] = mapped_column(String(30, 'Latin1_General_CI_AS'), primary_key=True)
    InstallDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    LastLoginDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    InstallType: Mapped[str] = mapped_column(CHAR(8, 'Latin1_General_CI_AS'), nullable=False)


class TRICGConsolidatedStocktakeScans(Base):
    __tablename__ = 'tRICG_Consolidated_Stocktake_Scans'
    __table_args__ = (
        PrimaryKeyConstraint('ScanID', name='PK_tRICG_Consolidated_Stocktake_Scans'),
        Index('IX_tRICG_Consolidated_Stocktake_Scans_Batch_Serial_No', 'Batch_Serial_No', mssql_clustered=False, mssql_include=[])
    )

    ScanID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    StocktakeID: Mapped[str] = mapped_column(CHAR(55, 'Latin1_General_CI_AS'), nullable=False)
    SectionID: Mapped[str] = mapped_column(CHAR(55, 'Latin1_General_CI_AS'), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    ItemNumber: Mapped[str] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'), nullable=False)
    ItemCount: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    CountDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    InHOSystem: Mapped[Optional[bool]] = mapped_column(Boolean)
    LOCNO: Mapped[Optional[int]] = mapped_column(Integer)
    Batch_Serial_No: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Expiry_Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SEQNO: Mapped[Optional[int]] = mapped_column(Integer)
    BinID: Mapped[Optional[int]] = mapped_column(Integer)
    ITEMCOLOUR: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    ITEMSIZE: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    LOCATION: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TRICGCubeTapeAudit(Base):
    __tablename__ = 'tRICG_Cube_Tape_Audit'
    __table_args__ = (
        PrimaryKeyConstraint('RecordID', name='PK_tRICG_Cube_Tape_Audit'),
    )

    RecordID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    DateTimeInserted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Length: Mapped[Optional[int]] = mapped_column(Integer)
    Width: Mapped[Optional[int]] = mapped_column(Integer)
    Height: Mapped[Optional[int]] = mapped_column(Integer)
    Volume: Mapped[Optional[int]] = mapped_column(Integer)
    SeqNo: Mapped[Optional[int]] = mapped_column(BigInteger)


class TRICGMOBPOSXMLFilesProcessed(Base):
    __tablename__ = 'tRICG_MOBPOS_XML_Files_Processed'
    __table_args__ = (
        PrimaryKeyConstraint('XML_File_Name', name='PK_tRICG_MOBPOS_XML_Files_Processed'),
    )

    XML_File_Name: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), primary_key=True)
    Modified_Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TRICGMobileAssemblyOrderLines(Base):
    __tablename__ = 'tRICG_Mobile_AssemblyOrderLines'
    __table_args__ = (
        PrimaryKeyConstraint('GUID_ID', 'SysUniqueID', 'OrderNumber', 'LineNumber', name='PK_tRICG_AssemblyOrderLines'),
        Index('IX_tRICG_Mobile_AssemblyOrderLines_Processed2ERP', 'Processed2ERP', mssql_clustered=False, mssql_include=[])
    )

    GUID_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    SysUniqueID: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    OrderNumber: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    LineNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    ItemID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    StockCode: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    LocationID: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    LocationBinID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    Quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    Batch_Serial_No: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Expiry_Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    BarCodeScanned: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    Processed2ERP: Mapped[Optional[str]] = mapped_column(CHAR(12, 'Latin1_General_CI_AS'))
    LabelDetails: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))


class TRICGPDACustomerStockTemplate(Base):
    __tablename__ = 'tRICG_PDA_Customer_Stock_Template'
    __table_args__ = (
        PrimaryKeyConstraint('CustomerID', 'ProfileID', 'StockCode', 'StockID', name='PK_tRICG_PDA_Customer_Stock_Template'),
    )

    CustomerID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ProfileID: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True, server_default=text("('N/A')"))
    StockCode: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    StockID: Mapped[int] = mapped_column(Integer, primary_key=True)
    IdealStock: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    MinReorderAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    Note: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TRICGPDAIDs(Base):
    __tablename__ = 'tRICG_PDA_IDs'
    __table_args__ = (
        PrimaryKeyConstraint('PDA_ID', name='PK_tRICG_PDA_IDs'),
    )

    PDA_ID: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    Owner: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    LoggedIn: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    WhenLastloggedIn: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AllowMultipleLogIn: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))
    PassWord: Mapped[Optional[str]] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'))
    IISurl: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    InternetLogin: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    InternetPassword: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    SQLVirtualFolder: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    SQLUserID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    SQLPassword: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    ExoDBName: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    MirrorDataSource: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    ExtDataSource: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TRICGPDAJobHeader(Base):
    __tablename__ = 'tRICG_PDA_JobHeader'
    __table_args__ = (
        PrimaryKeyConstraint('JobHeaderID', name='PK_tRICG_PDA_JobHeader'),
    )

    JobHeaderID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    JobNO: Mapped[Optional[int]] = mapped_column(Integer)
    JobCode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    DateInserted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PODSignature: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    PODSignatureName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    PDA_ID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    BranchNo: Mapped[Optional[int]] = mapped_column(BigInteger)
    StaffNo: Mapped[Optional[int]] = mapped_column(BigInteger)
    SYSUNIQUEID_JOB_TASK_RESOURCES: Mapped[Optional[int]] = mapped_column(BigInteger)
    JobCompleted: Mapped[Optional[bool]] = mapped_column(Boolean)
    Private_Note: Mapped[Optional[str]] = mapped_column(String(3500, 'Latin1_General_CI_AS'))
    Customer_Name: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TRICGPDAJobTimeAllocations(Base):
    __tablename__ = 'tRICG_PDA_JobTimeAllocations'
    __table_args__ = (
        PrimaryKeyConstraint('JobTimeAllocationID', name='PK_tRICG_PDA_JobTimeAllocations'),
    )

    JobTimeAllocationID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    JobNO: Mapped[Optional[int]] = mapped_column(Integer)
    JobCode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    LabourCode: Mapped[Optional[str]] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'))
    FromTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ToTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Hours: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    JobScaleID: Mapped[Optional[int]] = mapped_column(Integer)
    Status: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    Notes: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    JobTaskID: Mapped[Optional[int]] = mapped_column(Integer)
    StaffNo: Mapped[Optional[int]] = mapped_column(Integer)
    DateInserted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    JobHeaderID: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)


class TRICGPDAJobs(Base):
    __tablename__ = 'tRICG_PDA_Jobs'
    __table_args__ = (
        PrimaryKeyConstraint('JobID', name='PK_tRICG_PDA_Jobs'),
        Index('IX_tRICG_PDA_Jobs_JobNo', 'JobNO', mssql_clustered=False, mssql_include=[])
    )

    JobID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    JobNO: Mapped[Optional[int]] = mapped_column(Integer)
    JobCode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    StockCode: Mapped[Optional[str]] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'))
    Quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    DateInserted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Batch_Serial_No: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Expiry_Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LocationID: Mapped[Optional[int]] = mapped_column(Integer)
    LocationBinID: Mapped[Optional[int]] = mapped_column(Integer)
    Status: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    JobTaskID: Mapped[Optional[int]] = mapped_column(Integer)
    StaffNo: Mapped[Optional[int]] = mapped_column(Integer)
    SYSUNIQUEID_JOB_TASK_RESOURCES: Mapped[Optional[int]] = mapped_column(BigInteger)
    JobHeaderID: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    SeqNo: Mapped[Optional[int]] = mapped_column(BigInteger)
    QtyScanned: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    ScannedtoInvoice: Mapped[Optional[bool]] = mapped_column(Boolean)
    BarCode1: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    BarCode2: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    BarCode3: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    X_RICG_Barcode1Multiplier: Mapped[Optional[int]] = mapped_column(SmallInteger)
    X_RICG_Barcode2Multiplier: Mapped[Optional[int]] = mapped_column(SmallInteger)
    X_RICG_Barcode3Multiplier: Mapped[Optional[int]] = mapped_column(SmallInteger)


class TRICGPDAMobileConfig(Base):
    __tablename__ = 'tRICG_PDA_Mobile_Config'
    __table_args__ = (
        PrimaryKeyConstraint('ConfigID', name='PK_tRICG_PDA_Mobile_Config'),
    )

    ConfigID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    SMTPServer: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    SMTPUser: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    SMTPPass: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    FROMEmail: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    PDA_Sales_Show_Cost: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('((0))'))


class TRICGPDAMobileSalesHeader(Base):
    __tablename__ = 'tRICG_PDA_Mobile_Sales_Header'
    __table_args__ = (
        PrimaryKeyConstraint('salesorder_id_Seqno', name='PK_tRICG_PDA_Mobile_Sales_Header'),
        Index('IX_tRICG_PDA_Mobile_Sales_Header_salesorder_id', 'salesorder_id', mssql_clustered=False, mssql_include=[])
    )

    salesorder_id_Seqno: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    salesorder_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    expiry_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    staff_id: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('((0))'))
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('((0))'))
    transaction: Mapped[str] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'), nullable=False)
    original_id: Mapped[str] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'), nullable=False)
    custom: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), nullable=False)
    comments: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    subtotal: Mapped[Any] = mapped_column(MONEY, nullable=False, server_default=text('((0))'))
    discount: Mapped[Any] = mapped_column(MONEY, nullable=False, server_default=text('((0))'))
    rounding: Mapped[Any] = mapped_column(MONEY, nullable=False, server_default=text('((0))'))
    total_ex: Mapped[Any] = mapped_column(MONEY, nullable=False, server_default=text('((0))'))
    total_inc: Mapped[Any] = mapped_column(MONEY, nullable=False, server_default=text('((0))'))
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default=text('((0))'))
    exported: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('((0))'))
    salesorder_id: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    Customer_Name: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    PDA_Mobile_Sales_Header_GUID: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('(newid())'))


class TRICGPDAMobileSalesOrdersLine(Base):
    __tablename__ = 'tRICG_PDA_Mobile_Sales_OrdersLine'
    __table_args__ = (
        PrimaryKeyConstraint('line_id_Seqno', name='PK_tRICG_PDA_Mobile_Sales_OrdersLine'),
        Index('IX_tRICG_PDA_Mobile_Sales_OrdersLine_salesorder_id_line_id', 'salesorder_id', 'line_id', mssql_clustered=False, mssql_include=[])
    )

    line_id_Seqno: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    line_id: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('((0))'))
    package: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('((0))'))
    salesorder_id: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    stock_id: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    cost_ex: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    cost_inc: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    sales_tax: Mapped[Optional[str]] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'))
    sell_ex: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    sell_inc: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    rrp: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    print_ex: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    print_inc: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    quantity: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    parentline_id: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    status: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    orderline_id: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    unitof_measure: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))


class TRICGPDAMobileSalesUsers(Base):
    __tablename__ = 'tRICG_PDA_Mobile_Sales_Users'
    __table_args__ = (
        PrimaryKeyConstraint('Sales_User_Name', name='PK_tRICG_PDA_Mobile_Sales_Users'),
    )

    Sales_User_Name: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), primary_key=True)
    PDA_ID: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)
    Sales_User_Email: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Sales_Group_Name: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))


class TRICGPDAPalletBuildDetails(Base):
    __tablename__ = 'tRICG_PDA_Pallet_Build_Details'
    __table_args__ = (
        PrimaryKeyConstraint('PalletBuild_ID', 'Pallet_Type', 'PalletBuild_LineNumber', name='PK_tRICG_PDA_Pallet_Build_Details'),
        Index('IX_tRICG_PDA_Pallet_Build_Details_PalletBuild_LineNumber', 'PalletBuild_LineNumber', mssql_clustered=False, mssql_include=[]),
        Index('IX_tRICG_PDA_Pallet_Build_Details_Pallet_ID', 'Pallet_ID', mssql_clustered=False, mssql_include=[]),
        Index('IX_tRICG_PDA_Pallet_Build_Details_StockCode', 'StockCode', mssql_clustered=False, mssql_include=[])
    )

    PalletBuild_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    Pallet_ID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    Pallet_Type: Mapped[str] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'), primary_key=True)
    PalletBuild_LineNumber: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    StockCode: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)
    QtyBuilt: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 4), nullable=False)
    DateInserted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    DateModified: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    QtyAudited: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(18, 4))
    Batch_Serial_No: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Expiry_Date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Status: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    Checked: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    LocationID: Mapped[Optional[int]] = mapped_column(BigInteger)
    LocationIDChecked: Mapped[Optional[int]] = mapped_column(BigInteger)


class TRICGPDASurveys(Base):
    __tablename__ = 'tRICG_PDA_Surveys'
    __table_args__ = (
        PrimaryKeyConstraint('QuestionID', name='PK_tPDA_Surveys'),
    )

    QuestionID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    SurveyName: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    QuestionNumber: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    Type: Mapped[str] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'), nullable=False, server_default=text("('T')"))
    Question: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ListValues: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Length: Mapped[Optional[int]] = mapped_column(SmallInteger)
    ReliesOnQuestionNumber: Mapped[Optional[int]] = mapped_column(SmallInteger)
    ReliesonQuestionValue: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TRICGPDASurveysAnswers(Base):
    __tablename__ = 'tRICG_PDA_Surveys_Answers'
    __table_args__ = (
        PrimaryKeyConstraint('AnswerID', name='PK_tRICG_PDA_Surveys_Answers'),
        Index('IX_tRICG_PDA_Surveys_Answers_Related_Header_GUID', 'Related_Header_GUID', mssql_clustered=False, mssql_include=[])
    )

    AnswerID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    SurveyName: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    Customer_ID: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False, server_default=text('((0))'))
    QuestionNumber: Mapped[Optional[int]] = mapped_column(SmallInteger)
    Type: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))
    DateInserted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Status: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    Answer: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    PDA_ID: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    Related_System_Key_1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Related_System_Key_2: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    Related_Header_GUID: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    SYSTEM_FROM: Mapped[Optional[str]] = mapped_column(String(40, 'Latin1_General_CI_AS'))


class TRICGPDATItemSaleLines(Base):
    __tablename__ = 'tRICG_PDA_tItemSaleLines'
    __table_args__ = (
        PrimaryKeyConstraint('SaleGUID', 'ItemSaleLineGUID', name='PK_tRICG_PDA_tItemSaleLines'),
        Index('IX_tRICG_PDA_tItemSaleLines', 'SaleID', mssql_clustered=False, mssql_include=[])
    )

    SaleGUID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    ItemSaleLineGUID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    ItemSaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesTaxCalBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemPriceContainedTax: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    LocationID: Mapped[Optional[int]] = mapped_column(Integer)
    OriginalQtyOrdered: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyPicked: Mapped[Optional[float]] = mapped_column(Float(53))
    BOQty: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyintoMYOB: Mapped[Optional[float]] = mapped_column(Float(53))
    ExtraBinCode: Mapped[Optional[str]] = mapped_column(String(12, 'Latin1_General_CI_AS'))
    X_SOLINEID: Mapped[Optional[int]] = mapped_column(Integer)
    PickingStatus: Mapped[Optional[int]] = mapped_column(Integer)
    DivNo: Mapped[Optional[int]] = mapped_column(Integer)
    CartonsUsed: Mapped[Optional[int]] = mapped_column(Integer)
    OverRide4PickingItemNumber: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    OverRide4PickingBarCode1: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    OverRide4PickingQty2BPicked: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    OverRide4PickingPackAmount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    X_OST_SALESYSUNIQUEID: Mapped[Optional[int]] = mapped_column(BigInteger)
    TimeSalePicked: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickedBYID: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    Min: Mapped[Optional[float]] = mapped_column(Float(53))
    Max: Mapped[Optional[float]] = mapped_column(Float(53))
    QOH: Mapped[Optional[float]] = mapped_column(Float(53))
    QOO: Mapped[Optional[float]] = mapped_column(Float(53))
    QOSO: Mapped[Optional[float]] = mapped_column(Float(53))
    StockCode: Mapped[Optional[str]] = mapped_column(Unicode(23, 'Latin1_General_CI_AS'))
    Sales1: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales2: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales3: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales4: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales5: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales6: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales7: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales8: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales9: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales10: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales11: Mapped[Optional[float]] = mapped_column(Float(53))
    Sales12: Mapped[Optional[float]] = mapped_column(Float(53))
    OriginalQOH: Mapped[Optional[float]] = mapped_column(Float(53))


class TRICGPDATSales(Base):
    __tablename__ = 'tRICG_PDA_tSales'
    __table_args__ = (
        PrimaryKeyConstraint('SaleGUID', name='PK_tRICG_PDA_tSales'),
        Index('IX_tRICG_PDA_tSales_OrderStatus', 'OrderStatus', mssql_clustered=False, mssql_include=[]),
        Index('IX_tRICG_PDA_tSales_SaleID', 'SaleID', mssql_clustered=False, mssql_include=[])
    )

    SaleGUID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    InvoiceNumber: Mapped[Optional[str]] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'))
    CustomerPONumber: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    IsHistorical: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsThirteenthPeriod: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    ShipToAddress: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine3: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine4: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    InvoiceTypeID: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    InvoiceStatusID: Mapped[Optional[str]] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'))
    Memo: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Comment: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsTaxInclusive: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    IsPrinted: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    CostCentreID: Mapped[Optional[int]] = mapped_column(Integer)
    LinesPurged: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    PreAuditTrail: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    InvoiceDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickingStatus: Mapped[Optional[int]] = mapped_column(SmallInteger)
    PrintCount: Mapped[Optional[int]] = mapped_column(Integer)
    OverrideCustomerName: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine2: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine3: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverridePostCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TimeSalePicked: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickedBYID: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    BOLoaded: Mapped[Optional[bool]] = mapped_column(Boolean)
    OrderStatus: Mapped[Optional[int]] = mapped_column(Integer)
    LocNo: Mapped[Optional[int]] = mapped_column(Integer)
    ProfileID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))


class TRICGPODDetailsHeader(Base):
    __tablename__ = 'tRICG_POD_Details_Header'
    __table_args__ = (
        PrimaryKeyConstraint('POD_GUID_ID', name='PK_tRICG_POD_Details_Header'),
    )

    POD_GUID_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    DateInserted: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    DateModified: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    Reference: Mapped[str] = mapped_column(NCHAR(55, 'Latin1_General_CI_AS'), nullable=False)
    PDA_ID: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)
    Payment_Amount_1: Mapped[Any] = mapped_column(MONEY, nullable=False)
    Tender_Type_1: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)
    Payment_Amount_2: Mapped[Any] = mapped_column(MONEY, nullable=False)
    Tender_Type_2: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)
    PODSignature: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    PODSignatureName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    Status: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    InvoicePaid: Mapped[Optional[bool]] = mapped_column(Boolean)
    CustomerID: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    CustomerName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    CartonsConsigned: Mapped[Optional[int]] = mapped_column(SmallInteger)
    CartonsDelivered: Mapped[Optional[int]] = mapped_column(SmallInteger)
    DeliveryPDA_ID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    POD_Header_Extra1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra2: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra3: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra4: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra5: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra6: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra7: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra8: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra9: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    POD_Header_Extra10: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TRICGPODDetailsLines(Base):
    __tablename__ = 'tRICG_POD_Details_Lines'
    __table_args__ = (
        PrimaryKeyConstraint('POD_GUID_ID', 'LineNumber', name='PK_tRICG_POD_Details_Lines'),
    )

    POD_GUID_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    LineNumber: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    Invoice_Number: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), nullable=False)


class TRICGReSyncAudit(Base):
    __tablename__ = 'tRICG_ReSync_Audit'
    __table_args__ = (
        PrimaryKeyConstraint('ReSyncTableName', name='PK_tRICG_ReSync_Audit'),
    )

    ReSyncTableName: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    DateTimeReSynced: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TRICGRecycling4Pickups(Base):
    __tablename__ = 'tRICG_Recycling4_Pickups'
    __table_args__ = (
        PrimaryKeyConstraint('Pickup_ID', 'Type', 'StockCode', name='PK_tRICG_Recycling4_Pickups'),
        Index('IX_tRICG_Recycling4_Pickups_ScrapRef', 'ScrapRef', mssql_clustered=False, mssql_include=[])
    )

    Pickup_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    Type: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), primary_key=True)
    StockCode: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    StockID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    QtyPickedUp: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    QtyDroppedOff: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    UnitPriceEx: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    AccNo: Mapped[int] = mapped_column(BigInteger, nullable=False)
    AccNoSO: Mapped[int] = mapped_column(BigInteger, nullable=False)
    PickupSOType: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    InsertedDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ModifiedDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    LocNo: Mapped[int] = mapped_column(Integer, nullable=False)
    DeliveryLocNo: Mapped[int] = mapped_column(Integer, nullable=False)
    PostedPOintoEXO: Mapped[bool] = mapped_column(Boolean, nullable=False)
    PostedSOintoEXO: Mapped[bool] = mapped_column(Boolean, nullable=False)
    ScrapRef: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Status: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    POSeqno: Mapped[Optional[int]] = mapped_column(BigInteger)
    SOSeqno: Mapped[Optional[int]] = mapped_column(BigInteger)
    ApprovalNo: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    PODSignature: Mapped[Optional[str]] = mapped_column(String(1024, 'Latin1_General_CI_AS'))
    PODSignatureName: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    PDA_ID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    BranchNo: Mapped[Optional[int]] = mapped_column(BigInteger)


class TRICGRunManagementCycles(Base):
    __tablename__ = 'tRICG_Run_Management_Cycles'
    __table_args__ = (
        PrimaryKeyConstraint('RunNumber', name='PK_tRICG_Run_Management_Cycles'),
    )

    RunNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    RunCycle: Mapped[str] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'), nullable=False)


class TRICGRunManagementMaster(Base):
    __tablename__ = 'tRICG_Run_Management_Master'
    __table_args__ = (
        PrimaryKeyConstraint('RunNumber', name='PK_tRICG_Run_Management_Master'),
    )

    RunNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    RunName: Mapped[str] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'), nullable=False)


class TRICGRunManagementPostCodes(Base):
    __tablename__ = 'tRICG_Run_Management_PostCodes'
    __table_args__ = (
        PrimaryKeyConstraint('RunNumber', 'PostCode', name='PK_tRICG_Run_Management_PostCodes'),
    )

    RunNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    PostCode: Mapped[str] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'), primary_key=True)


class TRICGSTOCKLOCATIONS(Base):
    __tablename__ = 'tRICG_STOCK_LOCATIONS'
    __table_args__ = (
        PrimaryKeyConstraint('LOCNO', name='PK__tRICG_STOCK_LOCATIONS__LOCNO'),
    )

    LOCNO: Mapped[int] = mapped_column(Integer, primary_key=True)
    LCODE: Mapped[Optional[str]] = mapped_column(String(8, 'Latin1_General_CI_AS'))
    LNAME: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ISACTIVE: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    EXCLUDE_FROMVALUATION: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    EXCLUDE_FROMFREE_STOCK: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    EXCLUDE_FROMSALES: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    DELADDR1: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR2: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR3: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR4: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR5: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR6: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TRICGTruckIDs(Base):
    __tablename__ = 'tRICG_Truck_IDs'
    __table_args__ = (
        PrimaryKeyConstraint('TruckTypeID', name='PK_tRICG_Truck_IDs'),
    )

    TruckTypeID: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    NoPallets: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))


t_tRMCustomer = Table(
    'tRMCustomer', Base.metadata,
    Column('customer_id', Integer, nullable=False),
    Column('barcode', Unicode(15, 'Latin1_General_CI_AS'), nullable=False),
    Column('grade', SmallInteger, nullable=False),
    Column('notes', Unicode(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('comments', Unicode(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('status', Boolean, nullable=False),
    Column('custom1', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('custom2', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('inactive', Boolean, nullable=False),
    Column('date_modified', SMALLDATETIME, nullable=False),
    Column('surname', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('given_names', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('position', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('company', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('salutation', Unicode(10, 'Latin1_General_CI_AS')),
    Column('account', Boolean, nullable=False),
    Column('opened_id', Integer, nullable=False),
    Column('owner_id', Integer, nullable=False),
    Column('limit', MONEY, nullable=False),
    Column('days', SmallInteger, nullable=False),
    Column('fromEOM', Boolean, nullable=False),
    Column('addr1', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('addr2', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('addr3', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('suburb', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('state', Unicode(30, 'Latin1_General_CI_AS')),
    Column('postcode', Unicode(10, 'Latin1_General_CI_AS'), nullable=False),
    Column('country', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('phone', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('fax', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('mobile', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('email', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('abn', Unicode(11, 'Latin1_General_CI_AS'), nullable=False),
    Column('overseas', Boolean, nullable=False),
    Column('external', Boolean, nullable=False)
)


t_tRMStock = Table(
    'tRMStock', Base.metadata,
    Column('stock_id', Float(53)),
    Column('dept_id', Integer),
    Column('Barcode', Unicode(15, 'Latin1_General_CI_AS')),
    Column('PLU', Integer),
    Column('custom1', Unicode(50, 'Latin1_General_CI_AS')),
    Column('custom2', Unicode(50, 'Latin1_General_CI_AS')),
    Column('sales_prompt', Unicode(50, 'Latin1_General_CI_AS')),
    Column('inactive', Boolean, nullable=False),
    Column('allow_renaming', Boolean, nullable=False),
    Column('allow_fractions', Boolean, nullable=False),
    Column('package', Boolean, nullable=False),
    Column('tax_components', Boolean, nullable=False),
    Column('print_components', Boolean, nullable=False),
    Column('description', Unicode(40, 'Latin1_General_CI_AS')),
    Column('longdesc', Unicode(255, 'Latin1_General_CI_AS')),
    Column('cat1', Unicode(6, 'Latin1_General_CI_AS')),
    Column('cat2', Unicode(6, 'Latin1_General_CI_AS')),
    Column('goods_tax', Unicode(3, 'Latin1_General_CI_AS')),
    Column('cost', MONEY),
    Column('sales_tax', Unicode(3, 'Latin1_General_CI_AS')),
    Column('sell', MONEY),
    Column('quantity', Float(53)),
    Column('layby_qty', Float(53)),
    Column('salesorder_qty', Float(53)),
    Column('date_created', DateTime),
    Column('track_serial', Boolean, nullable=False),
    Column('static_quantity', Boolean, nullable=False),
    Column('bonus', MONEY),
    Column('order_threshold', Float(53)),
    Column('order_quantity', Float(53)),
    Column('supplier_id', Integer),
    Column('date_modified', DateTime),
    Column('freight', Boolean, nullable=False),
    Column('tare_weight', Float(53)),
    Column('unitof_measure', TINYINT),
    Column('weighted', Boolean, nullable=False),
    Column('external', Boolean, nullable=False)
)


t_tRMSupplier = Table(
    'tRMSupplier', Base.metadata,
    Column('supplier_id', Integer, nullable=False),
    Column('barcode', Unicode(15, 'Latin1_General_CI_AS'), nullable=False),
    Column('supplier', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('grade', SmallInteger, nullable=False),
    Column('inactive', Boolean, nullable=False),
    Column('main_contact', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_position', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_addr1', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_addr2', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_addr3', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_suburb', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_state', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_postcode', Unicode(10, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_country', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_phone', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_fax', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('main_email', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_contact', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_position', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_addr1', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_addr2', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_addr3', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_suburb', Unicode(40, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_state', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_postcode', Unicode(10, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_country', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_phone', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_fax', Unicode(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('other_email', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('freight_free', Boolean, nullable=False),
    Column('reject_backorders', Boolean, nullable=False),
    Column('exported', Boolean, nullable=False),
    Column('date_modified', DateTime, nullable=False),
    Column('custom1', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('custom2', CHAR(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('delivery_delay', Integer, nullable=False),
    Column('abn', Unicode(11, 'Latin1_General_CI_AS'), nullable=False)
)


class TRMTaxCodes(Base):
    __tablename__ = 'tRMTaxCodes'
    __table_args__ = (
        PrimaryKeyConstraint('code', name='PK_tRMTaxCodes'),
    )

    code: Mapped[str] = mapped_column(CHAR(3, 'Latin1_General_CI_AS'), primary_key=True)
    export: Mapped[str] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'), nullable=False)
    description: Mapped[str] = mapped_column(CHAR(30, 'Latin1_General_CI_AS'), nullable=False)
    percentage: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 0), nullable=False)
    tax_type: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    sales_ac: Mapped[str] = mapped_column(CHAR(31, 'Latin1_General_CI_AS'), nullable=False)
    goods_ac: Mapped[str] = mapped_column(CHAR(31, 'Latin1_General_CI_AS'), nullable=False)
    tax_id: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    date_modified: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)


class TReceiptAllocations(Base):
    __tablename__ = 'tReceiptAllocations'
    __table_args__ = (
        PrimaryKeyConstraint('PurchaseID', 'LineNumber', 'SerialNumber1', 'TieBreaker', name='PK_tReceiptAllocations'),
    )

    PurchaseID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LineNumber: Mapped[int] = mapped_column(Integer, primary_key=True)
    SerialNumber1: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    TieBreaker: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsBatchNumber: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    ItemNumber: Mapped[Optional[str]] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'))
    PurchaseOrderNumber: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    P4PSaleIDSold: Mapped[Optional[int]] = mapped_column(Integer)
    P4PSaleLineIDSold: Mapped[Optional[int]] = mapped_column(Integer)
    InvoiceNumberSold: Mapped[Optional[str]] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'))
    P4PSaleIDReturned: Mapped[Optional[int]] = mapped_column(Integer)
    P4PSaleLineIDReturned: Mapped[Optional[int]] = mapped_column(Integer)
    InvoiceNumberReturned: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    DateSold: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DateReceived: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SupplierInvoiceNumber: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TSItemSaleLines(Base):
    __tablename__ = 'tSItemSaleLines'
    __table_args__ = (
        PrimaryKeyConstraint('ItemSaleLineID', name='PK_tSItemSaleLines'),
    )

    ItemSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveTotal: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxExclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveUnitPrice: Mapped[float] = mapped_column(Float(53), nullable=False)
    Discount: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesTaxCalBasisID: Mapped[str] = mapped_column(Unicode(3, 'Latin1_General_CI_AS'), nullable=False)
    CostOfGoodsSoldAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    ItemPriceContainedTax: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    LocationID: Mapped[Optional[int]] = mapped_column(Integer)
    OriginalQtyOrdered: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyPicked: Mapped[Optional[float]] = mapped_column(Float(53))
    QtyintoMYOB: Mapped[Optional[float]] = mapped_column(Float(53))
    BOQty: Mapped[Optional[float]] = mapped_column(Float(53))


class TSPremierPOSItemQtyLocations(Base):
    __tablename__ = 'tSPremierPOSItemQtyLocations'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'ILocID', name='PK_tSPremierPOSItemQtyLocations'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ILocID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)
    Multiplier: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)


class TSPremierPOSItemSerials(Base):
    __tablename__ = 'tSPremierPOSItemSerials'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'SaleLineID', 'SerialNumber1', name='PK_tSPremierPOSItemSerials'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SerialNumber1: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), primary_key=True)
    SerialNumber2: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)


class TSPremierPOSTenderTrans(Base):
    __tablename__ = 'tSPremierPOSTenderTrans'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'TenderID', name='PK_tSPremierPOSTenderTrans'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TenderID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TenderAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TransDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    UserID: Mapped[int] = mapped_column(Integer, nullable=False)
    TILL: Mapped[int] = mapped_column(Integer, nullable=False)
    ActualTendered: Mapped[float] = mapped_column(Float(53), nullable=False)


class TSSales(Base):
    __tablename__ = 'tSSales'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tSSales'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    InvoiceNumber: Mapped[str] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'), nullable=False)
    CustomerPONumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), nullable=False)
    IsHistorical: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsThirteenthPeriod: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddress: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine1: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine2: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine3: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine4: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceStatusID: Mapped[str] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    Memo: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsTaxInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    IsPrinted: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    Comment: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    CostCentreID: Mapped[Optional[int]] = mapped_column(Integer)
    LinesPurged: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    PreAuditTrail: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    InvoiceDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickingStatus: Mapped[Optional[int]] = mapped_column(SmallInteger)


class TSTOCKLOCATIONS(Base):
    __tablename__ = 'tSTOCK_LOCATIONS'
    __table_args__ = (
        PrimaryKeyConstraint('LOCNO', name='PK__STOCK_LOC__LOCNO__04BA9F53'),
    )

    LOCNO: Mapped[int] = mapped_column(Integer, primary_key=True)
    LCODE: Mapped[Optional[str]] = mapped_column(String(8, 'Latin1_General_CI_AS'))
    LNAME: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    ISACTIVE: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('Y')"))
    EXCLUDE_FROMVALUATION: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('N')"))
    EXCLUDE_FROMFREE_STOCK: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('N')"))
    EXCLUDE_FROMSALES: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), server_default=text("('N')"))
    DELADDR1: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR2: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR3: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR4: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR5: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    DELADDR6: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))


class TSaleDespatchLabels(Base):
    __tablename__ = 'tSaleDespatchLabels'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'ShipmentID', 'LineID', name='PK_tSaleDespatchLabels'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ShipmentID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PalletNumber: Mapped[Optional[str]] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    LabelCount: Mapped[Optional[int]] = mapped_column(Integer)


class TSaleLines(Base):
    __tablename__ = 'tSaleLines'
    __table_args__ = (
        PrimaryKeyConstraint('SaleLineID', name='PK_tSaleLines'),
    )

    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)


t_tSaleLinesWeb = Table(
    'tSaleLinesWeb', Base.metadata,
    Column('SaleLineID', Integer, nullable=False),
    Column('SaleID', Integer, nullable=False),
    Column('LineNumber', Integer, nullable=False),
    Column('LineTypeID', Unicode(1, 'Latin1_General_CI_AS'), nullable=False),
    Column('Description', Unicode(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('TaxExclusiveAmount', Float(53), nullable=False),
    Column('TaxInclusiveAmount', Float(53), nullable=False),
    Column('JobID', Integer, nullable=False),
    Column('TaxCodeID', Integer, nullable=False),
    Column('TaxBasisAmount', Float(53), nullable=False),
    Column('TaxBasisAmountIsInclusive', Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
)


class TSales(Base):
    __tablename__ = 'tSales'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tSales'),
        Index('IX_tSales_PickingStatus', 'PickingStatus', mssql_clustered=False, mssql_include=[])
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    InvoiceNumber: Mapped[Optional[str]] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'))
    CustomerPONumber: Mapped[Optional[str]] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'))
    IsHistorical: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsThirteenthPeriod: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    ShipToAddress: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine1: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine2: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine3: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    ShipToAddressLine4: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    InvoiceTypeID: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    InvoiceStatusID: Mapped[Optional[str]] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'))
    Memo: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Comment: Mapped[Optional[str]] = mapped_column(String(2048, 'Latin1_General_CI_AS'))
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    IsTaxInclusive: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    IsPrinted: Mapped[Optional[str]] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'))
    CostCentreID: Mapped[Optional[int]] = mapped_column(Integer)
    LinesPurged: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    PreAuditTrail: Mapped[Optional[str]] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    InvoiceDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PickingStatus: Mapped[Optional[int]] = mapped_column(SmallInteger)
    PrintCount: Mapped[Optional[int]] = mapped_column(Integer)
    OverrideCustomerName: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine1: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine2: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverrideStreetLine3: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    OverridePostCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    PickedBYID: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    ProfileID: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    TimeSalePicked: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LocNo: Mapped[Optional[int]] = mapped_column(Integer)
    OrderStatus: Mapped[Optional[int]] = mapped_column(Integer)
    WareHouseCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    ShippingMethod: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    X_PalletPosition: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


class TSalesHold(Base):
    __tablename__ = 'tSalesHold'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tSalesHold'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    InvoiceNumber: Mapped[str] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'), nullable=False)
    CustomerPONumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), nullable=False)
    IsHistorical: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsThirteenthPeriod: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddress: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine1: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine2: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine3: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine4: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceStatusID: Mapped[str] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    Memo: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    Comment: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsTaxInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    IsPrinted: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)


class TSalesOrderCartonWeights(Base):
    __tablename__ = 'tSalesOrderCartonWeights'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'BoxNo', name='PK_tSalesOrderCartonWeights'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    BoxNo: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), primary_key=True)
    Weight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    ArticleNo: Mapped[Optional[str]] = mapped_column(String(30, 'Latin1_General_CI_AS'))
    eParcelBarcode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    eParcelDeliveryPostCode: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    eParcelConsignmentNumber: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    eParcelDateTimeUpdated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TSalesOrderTrucksAvailable(Base):
    __tablename__ = 'tSalesOrderTrucksAvailable'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'TruckID', name='PK_tSalesOrderTrucksAvailable'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TruckID: Mapped[str] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'), primary_key=True)
    TruckTypeID: Mapped[str] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'), nullable=False)
    NoPallets: Mapped[float] = mapped_column(Float(53), nullable=False)


class TSalesReceiptHeader(Base):
    __tablename__ = 'tSalesReceiptHeader'
    __table_args__ = (
        PrimaryKeyConstraint('GReceiptID', name='PK_tSalesReceipts'),
    )

    GReceiptID: Mapped[int] = mapped_column(Integer, primary_key=True)
    GRDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    SupplierID: Mapped[int] = mapped_column(Integer, nullable=False)
    InMYOB: Mapped[bool] = mapped_column(Boolean, nullable=False)
    SupplierInvNo: Mapped[Optional[str]] = mapped_column(CHAR(15, 'Latin1_General_CI_AS'))


class TSalesReceiptLines(Base):
    __tablename__ = 'tSalesReceiptLines'
    __table_args__ = (
        PrimaryKeyConstraint('GReceiptID', 'GReceiptLineNo', name='PK_tSalesReceiptLines'),
    )

    GReceiptID: Mapped[int] = mapped_column(Integer, primary_key=True)
    GReceiptLineNo: Mapped[int] = mapped_column(Integer, primary_key=True)
    Barcode: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    Quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    ItemNumber: Mapped[str] = mapped_column(String(32, 'Latin1_General_CI_AS'), nullable=False)
    ItemName: Mapped[str] = mapped_column(String(32, 'Latin1_General_CI_AS'), nullable=False)
    InMYOB: Mapped[bool] = mapped_column(Boolean, nullable=False)


class TSalesTemp(Base):
    __tablename__ = 'tSalesTemp'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tSalesTemp'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    InvoiceNumber: Mapped[str] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'), nullable=False)
    CustomerPONumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), nullable=False)
    IsHistorical: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsThirteenthPeriod: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddress: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine1: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine2: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine3: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine4: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceStatusID: Mapped[str] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    Memo: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    Comment: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsTaxInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    IsPrinted: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)


class TSalesWeb(Base):
    __tablename__ = 'tSalesWeb'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tSalesWeb'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceNumber: Mapped[str] = mapped_column(Unicode(8, 'Latin1_General_CI_AS'), nullable=False)
    CustomerPONumber: Mapped[str] = mapped_column(Unicode(20, 'Latin1_General_CI_AS'), nullable=False)
    IsHistorical: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsThirteenthPeriod: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Name: Mapped[str] = mapped_column(Unicode(55, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddress: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine1: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine2: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine3: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine4: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceTypeID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceStatusID: Mapped[str] = mapped_column(Unicode(2, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalCredits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    SalesPersonID: Mapped[int] = mapped_column(Integer, nullable=False)
    Memo: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    Comment: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    ReferralSourceID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsTaxInclusive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    IsPrinted: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    Company: Mapped[Optional[str]] = mapped_column(Unicode(155, 'Latin1_General_CI_AS'))
    Phone: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    EMail: Mapped[Optional[str]] = mapped_column(Unicode(155, 'Latin1_General_CI_AS'))
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    PackSlipPrinted: Mapped[Optional[bool]] = mapped_column(Boolean)
    InvoiceClosed: Mapped[Optional[bool]] = mapped_column(Boolean)
    OrderStatus: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Latin1_General_CI_AS'))


class TSalesRunCustomers(Base):
    __tablename__ = 'tSales_Run_Customers'
    __table_args__ = (
        PrimaryKeyConstraint('CustomerID', 'RunNo', name='PK_tSales_Run_Customers'),
        Index('IX_tSales_Run_Customers_SaleID', 'SaleID', mssql_clustered=False, mssql_include=[])
    )

    CustomerID: Mapped[int] = mapped_column(Integer, primary_key=True)
    RunNo: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    Notes: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    MapReference: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    InvoiceNumber: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    ExtraInfo: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    SeqNo: Mapped[Optional[str]] = mapped_column(String(55, 'Latin1_General_CI_AS'))
    Comments: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TSalesRunNos(Base):
    __tablename__ = 'tSales_Run_Nos'
    __table_args__ = (
        PrimaryKeyConstraint('RunNo', name='PK_tSales_Run_Nos'),
    )

    RunNo: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    RunName: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)


class TSalesRunTemplateItems(Base):
    __tablename__ = 'tSales_Run_Template_Items'
    __table_args__ = (
        PrimaryKeyConstraint('CustomerID', 'RunNo', 'SaleID', 'ItemID', name='PK_tSales_Run_Template_Items'),
    )

    CustomerID: Mapped[int] = mapped_column(Integer, primary_key=True)
    RunNo: Mapped[str] = mapped_column(String(55, 'Latin1_General_CI_AS'), primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 4), nullable=False)


class TSalesRunsMOBPOSTempItemSaleLines(Base):
    __tablename__ = 'tSales_Runs_MOBPOS_Temp_ItemSaleLines'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', 'ItemID', name='PK_tSales_Runs_MOBPOS_Temp_ItemSaleLines'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Quantity: Mapped[float] = mapped_column(Float(53), nullable=False)


class TSalesRunsMOBPOSTempSales(Base):
    __tablename__ = 'tSales_Runs_MOBPOS_Temp_Sales'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tSales_Runs_MOBPOS_Temp_Sales'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    cardrecordid: Mapped[int] = mapped_column(Integer, nullable=False)
    InvoiceNumber: Mapped[str] = mapped_column(String(25, 'Latin1_General_CI_AS'), nullable=False)


class TScratchFile(Base):
    __tablename__ = 'tScratchFile'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', name='PK_tScratchFile'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    QuantityOnHand: Mapped[int] = mapped_column(BigInteger, nullable=False)
    QuantityOnOrder: Mapped[int] = mapped_column(BigInteger, nullable=False)
    FinalQtyDiff: Mapped[float] = mapped_column(Float(53), nullable=False)
    IsComponent: Mapped[Optional[bool]] = mapped_column(Boolean)
    SaleID: Mapped[Optional[int]] = mapped_column(Integer)


class TServiceSaleLines(Base):
    __tablename__ = 'tServiceSaleLines'
    __table_args__ = (
        PrimaryKeyConstraint('ServiceSaleLineID', 'SaleLineID', 'SaleID', name='PK_tServiceSaleLines'),
    )

    ServiceSaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleLineID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LineNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    LineTypeID: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    Description: Mapped[str] = mapped_column(CHAR(255, 'Latin1_General_CI_AS'), nullable=False)
    TaxExclusiveAmount: Mapped[Any] = mapped_column(MONEY, nullable=False)
    TaxInclusiveAmount: Mapped[Any] = mapped_column(MONEY, nullable=False)
    JobID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TaxBasisAmount: Mapped[Any] = mapped_column(MONEY, nullable=False)
    TaxBasisAmountIsInclusive: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'), nullable=False)
    AccountID: Mapped[int] = mapped_column(Integer, nullable=False)


class TShippingMethods(Base):
    __tablename__ = 'tShippingMethods'
    __table_args__ = (
        PrimaryKeyConstraint('ShippingMethodID', name='PK_tShippingMethods'),
    )

    ShippingMethodID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ShippingMethod: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))


class TSingleItemStocktake(Base):
    __tablename__ = 'tSingleItemStocktake'
    __table_args__ = (
        PrimaryKeyConstraint('StocktakeID', name='PK_tSingleItemStocktake'),
    )

    StocktakeID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    LocationID: Mapped[int] = mapped_column(Integer, nullable=False)
    Supplier: Mapped[int] = mapped_column(Integer, nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    ItemNumber: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    DeltaCount: Mapped[Optional[int]] = mapped_column(Integer)
    DateCreated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Operator: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))
    DatePosted: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Posted: Mapped[Optional[bool]] = mapped_column(Boolean)


t_tSlingReceipts = Table(
    'tSlingReceipts', Base.metadata,
    Column('ReceiptID', Integer),
    Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS')),
    Column('Qty', Integer),
    Column('ReceiptDate', DateTime),
    Column('SupplierID', Integer),
    Column('SupplierName', Unicode(52, 'Latin1_General_CI_AS')),
    Column('Processed', Boolean),
    Column('SlingNo', CHAR(10, 'Latin1_General_CI_AS')),
    Index('IX_tSlingReceipts_Processed', 'Processed', mssql_clustered=False, mssql_include=[]),
    Index('IX_tSlingReceipts_ReceiptID', 'ReceiptID', mssql_clustered=False, mssql_include=[])
)


t_tSlings = Table(
    'tSlings', Base.metadata,
    Column('SlingNo', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Product', CHAR(30, 'Latin1_General_CI_AS')),
    Column('Grade', CHAR(20, 'Latin1_General_CI_AS')),
    Column('Species', CHAR(4, 'Latin1_General_CI_AS')),
    Column('Width', Integer),
    Column('Thick', Integer),
    Column('FinishSize', CHAR(20, 'Latin1_General_CI_AS')),
    Column('Tally', Integer),
    Column('DateEntered', DateTime),
    Column('DateReceived', DateTime),
    Column('DateSold', DateTime),
    Column('InvoiceNo', CHAR(8, 'Latin1_General_CI_AS')),
    Column('GradedFaces', CHAR(10, 'Latin1_General_CI_AS')),
    Column('MC', CHAR(10, 'Latin1_General_CI_AS')),
    Column('OrigSling', CHAR(10, 'Latin1_General_CI_AS')),
    Column('SplitSling', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Samp1MC', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Samp2MC', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Samp3MC', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Samp4MC', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Samp1CW', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Samp2CW', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Samp3CW', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Samp4CW', CHAR(10, 'Latin1_General_CI_AS')),
    Column('Tester', CHAR(50, 'Latin1_General_CI_AS')),
    Column('Company', CHAR(50, 'Latin1_General_CI_AS')),
    Index('IX_tSlings_SlingNo', 'SlingNo', mssql_clustered=False, mssql_include=[])
)


class TStockSnapshot(Base):
    __tablename__ = 'tStockSnapshot'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', name='PK_tStockSnapshot'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ItemName: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ItemNumber: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ItemDescription: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    QuantityOnHand: Mapped[float] = mapped_column(Float(53), nullable=False)
    ValueOnHand: Mapped[float] = mapped_column(Float(53), nullable=False)
    SellOnOrder: Mapped[float] = mapped_column(Float(53), nullable=False)
    PurchaseOnOrder: Mapped[float] = mapped_column(Float(53), nullable=False)
    IncomeAccountID: Mapped[int] = mapped_column(Integer, nullable=False)
    ExpenseAccountID: Mapped[int] = mapped_column(Integer, nullable=False)
    InventoryAccountID: Mapped[int] = mapped_column(Integer, nullable=False)
    CountAppliedToMYOB: Mapped[bool] = mapped_column(Boolean, nullable=False)


class TStockTakeCount(Base):
    __tablename__ = 'tStockTakeCount'
    __table_args__ = (
        PrimaryKeyConstraint('StockTakeName', 'ItemID', 'ItemLocation', name='PK_tStockTakeCount'),
    )

    StockTakeName: Mapped[str] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'), primary_key=True)
    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ItemLocation: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), primary_key=True)
    ItemName: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ItemNumber: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ItemCount: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    CountDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ItemSupplierID: Mapped[Optional[int]] = mapped_column(Integer)
    InMYOB: Mapped[Optional[bool]] = mapped_column(Boolean)
    BarCode: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))


class TStockTakeCountfromPDA(Base):
    __tablename__ = 'tStockTakeCountfromPDA'
    __table_args__ = (
        PrimaryKeyConstraint('ScanID', name='PK_tStockTakeCountfromPDA'),
    )

    ScanID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    StockTakeName: Mapped[str] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'), nullable=False)
    ItemID: Mapped[int] = mapped_column(Integer, nullable=False)
    ItemLocation: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ItemNumber: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
    ItemCount: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    CountDateTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    BarCode: Mapped[Optional[str]] = mapped_column(String(50, 'Latin1_General_CI_AS'))
    Processed: Mapped[Optional[bool]] = mapped_column(Boolean)


class TStocktakeM(Base):
    __tablename__ = 'tStocktakeM'
    __table_args__ = (
        PrimaryKeyConstraint('AccountName', 'ItemNumber', name='PK_tStocktakeM'),
    )

    AccountName: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), primary_key=True)
    ItemNumber: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), primary_key=True)
    ItemName: Mapped[str] = mapped_column(Unicode(30, 'Latin1_General_CI_AS'), nullable=False)


class TStorageLevelDescriptions(Base):
    __tablename__ = 'tStorageLevelDescriptions'
    __table_args__ = (
        PrimaryKeyConstraint('StorageLevel', name='PK_tStorageLevelDescriptions'),
    )

    StorageLevel: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    Description: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)


class TStorageLevels(Base):
    __tablename__ = 'tStorageLevels'
    __table_args__ = (
        PrimaryKeyConstraint('LevelID', name='PK_tStorageLevel'),
    )

    LevelID: Mapped[int] = mapped_column(SmallInteger, Identity(start=1, increment=1), primary_key=True)
    LevelDescription: Mapped[str] = mapped_column(String(50, 'Latin1_General_CI_AS'), nullable=False)
    ShortDescription: Mapped[str] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'), nullable=False)
    StoreageLevel: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default=text('((1))'))


t_tSupplierStkSheet = Table(
    'tSupplierStkSheet', Base.metadata,
    Column('ItemID', Integer, nullable=False),
    Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('ComponentID', Integer, nullable=False),
    Column('ComponentItemName', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('ComponentItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('SupplierName', Unicode(52, 'Latin1_General_CI_AS'), nullable=False),
    Column('AccountName', Unicode(30, 'Latin1_General_CI_AS'), nullable=False)
)


class TSuppliers(Base):
    __tablename__ = 'tSuppliers'
    __table_args__ = (
        PrimaryKeyConstraint('SupplierID', name='PK_tSuppliers'),
    )

    SupplierID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    CardIdentification: Mapped[str] = mapped_column(Unicode(16, 'Latin1_General_CI_AS'), nullable=False)
    Name: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    LastName: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    FirstName: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    IsIndividual: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    IsInactive: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    Notes: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    IdentifierID: Mapped[str] = mapped_column(Unicode(26, 'Latin1_General_CI_AS'), nullable=False)
    CustomField1: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    CustomField2: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    CustomField3: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    ABN: Mapped[str] = mapped_column(Unicode(14, 'Latin1_General_CI_AS'), nullable=False)
    ABNBranch: Mapped[str] = mapped_column(Unicode(11, 'Latin1_General_CI_AS'), nullable=False)
    TaxIDNumber: Mapped[str] = mapped_column(Unicode(19, 'Latin1_General_CI_AS'), nullable=False)
    TaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    UseSupplierTaxCode: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    CreditLimit: Mapped[float] = mapped_column(Float(53), nullable=False)
    VolumeDiscount: Mapped[float] = mapped_column(Float(53), nullable=False)
    CurrentBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPayableDays: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalPaidPurchases: Mapped[int] = mapped_column(Integer, nullable=False)
    HighestPurchaseAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    HighestPayableAmount: Mapped[float] = mapped_column(Float(53), nullable=False)
    PaymentCardNumber: Mapped[str] = mapped_column(Unicode(25, 'Latin1_General_CI_AS'), nullable=False)
    PaymentNameOnCard: Mapped[str] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'), nullable=False)
    PaymentNotes: Mapped[str] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'), nullable=False)
    BSBCode: Mapped[str] = mapped_column(Unicode(7, 'Latin1_General_CI_AS'), nullable=False)
    BankAccountNumber: Mapped[str] = mapped_column(Unicode(19, 'Latin1_General_CI_AS'), nullable=False)
    BankAccountName: Mapped[str] = mapped_column(Unicode(32, 'Latin1_General_CI_AS'), nullable=False)
    HourlyBillingRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    EstimatedCostPerHour: Mapped[float] = mapped_column(Float(53), nullable=False)
    PurchaseLayoutID: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    PrintedForm: Mapped[str] = mapped_column(Unicode(34, 'Latin1_General_CI_AS'), nullable=False)
    IsPaidElectronically: Mapped[str] = mapped_column(Unicode(1, 'Latin1_General_CI_AS'), nullable=False)
    ChangeControl: Mapped[str] = mapped_column(CHAR(20, 'Latin1_General_CI_AS'), nullable=False)
    CurrencyID: Mapped[Optional[int]] = mapped_column(Integer)
    Picture: Mapped[Optional[str]] = mapped_column(Unicode(255, 'Latin1_General_CI_AS'))
    Identifiers: Mapped[Optional[str]] = mapped_column(Unicode(26, 'Latin1_General_CI_AS'))
    CustomList1ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomList2ID: Mapped[Optional[int]] = mapped_column(Integer)
    CustomList3ID: Mapped[Optional[int]] = mapped_column(Integer)
    SupplierSince: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    LastPuchaseDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    LastPaymentDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    MethodOfPaymentID: Mapped[Optional[int]] = mapped_column(Integer)
    PaymentExpirationDate: Mapped[Optional[str]] = mapped_column(Unicode(10, 'Latin1_General_CI_AS'))
    PaymentBSB: Mapped[Optional[str]] = mapped_column(Unicode(7, 'Latin1_General_CI_AS'))
    PaymentBankAccountNumber: Mapped[Optional[str]] = mapped_column(Unicode(11, 'Latin1_General_CI_AS'))
    PaymentBankAccountName: Mapped[Optional[str]] = mapped_column(Unicode(32, 'Latin1_General_CI_AS'))
    ExpenseAccountID: Mapped[Optional[int]] = mapped_column(Integer)
    PurchaseCommentID: Mapped[Optional[int]] = mapped_column(Integer)
    ShippingMethodID: Mapped[Optional[int]] = mapped_column(Integer)
    PaymentMemo: Mapped[Optional[str]] = mapped_column(String(255, 'Latin1_General_CI_AS'))
    BankParticulars: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    BankCode: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    BankReference: Mapped[Optional[str]] = mapped_column(String(20, 'Latin1_General_CI_AS'))
    PaymentBankBranch: Mapped[Optional[str]] = mapped_column(String(10, 'Latin1_General_CI_AS'))


class TSystemParams(Base):
    __tablename__ = 'tSystem_Params'
    __table_args__ = (
        PrimaryKeyConstraint('Param_Type', 'Param_Function_Name', 'ERPSystem', name='PK_tSystem_Params'),
    )

    Param_Type: Mapped[str] = mapped_column(NCHAR(10, 'Latin1_General_CI_AS'), primary_key=True)
    Param_Function_Name: Mapped[str] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'), primary_key=True)
    ERPSystem: Mapped[str] = mapped_column(NCHAR(20, 'Latin1_General_CI_AS'), primary_key=True)
    Param: Mapped[str] = mapped_column(Unicode(collation='Latin1_General_CI_AS'), nullable=False)


class TTaxCodeConsolidations(Base):
    __tablename__ = 'tTaxCodeConsolidations'
    __table_args__ = (
        PrimaryKeyConstraint('TaxCodeConsolidationId', name='PK_tTaxCodeConsolidations'),
    )

    TaxCodeConsolidationId: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ConsolidatedTaxCodeID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ElementTaxCodeID: Mapped[Optional[int]] = mapped_column(BigInteger)


class TTaxCodes(Base):
    __tablename__ = 'tTaxCodes'
    __table_args__ = (
        PrimaryKeyConstraint('TaxCodeID', name='PK_tTaxCodes'),
    )

    TaxCodeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    TaxCode: Mapped[str] = mapped_column(String(3, 'Latin1_General_CI_AS'), nullable=False)
    TaxCodeDescription: Mapped[str] = mapped_column(String(30, 'Latin1_General_CI_AS'), nullable=False)
    TaxPercentageRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxCodeTypeID: Mapped[str] = mapped_column(String(3, 'Latin1_General_CI_AS'), nullable=False)
    TaxThreshold: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxCollectedAccountID: Mapped[Optional[int]] = mapped_column(Integer)
    TaxPaidAccountID: Mapped[Optional[int]] = mapped_column(Integer)
    LinkedCardID: Mapped[Optional[int]] = mapped_column(Integer)


class TTerms(Base):
    __tablename__ = 'tTerms'
    __table_args__ = (
        PrimaryKeyConstraint('TermsID', name='PK_tTerms'),
    )

    TermsID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LatePaymentChargePercent: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    EarlyPaymentDiscountPercent: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 4))
    TermsOfPaymentID: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))
    ImportPaymentIsDue: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    DiscountDays: Mapped[Optional[int]] = mapped_column(Integer)
    BalanceDueDays: Mapped[Optional[int]] = mapped_column(Integer)
    DiscountDate: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))
    BalanceDueDate: Mapped[Optional[str]] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'))


class TTermsofPayment(Base):
    __tablename__ = 'tTermsofPayment'
    __table_args__ = (
        PrimaryKeyConstraint('TermsOfPaymentID', name='PK_tTermsofPayment'),
    )

    TermsOfPaymentID: Mapped[str] = mapped_column(CHAR(10, 'Latin1_General_CI_AS'), primary_key=True)
    Description: Mapped[str] = mapped_column(String(100, 'Latin1_General_CI_AS'), nullable=False)


class TWorkShift(Base):
    __tablename__ = 'tWorkShift'
    __table_args__ = (
        PrimaryKeyConstraint('WorkShit_GUID_ID', name='PK_tWorkShift'),
    )

    WorkShit_GUID_ID: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    EmployeeID: Mapped[int] = mapped_column(Integer, nullable=False)
    LogInTime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    LogOutTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PDA_ID: Mapped[Optional[str]] = mapped_column(String(25, 'Latin1_General_CI_AS'))
    Comment: Mapped[Optional[str]] = mapped_column(String(100, 'Latin1_General_CI_AS'))


class TePremInspectors(Base):
    __tablename__ = 'tePremInspectors'
    __table_args__ = (
        PrimaryKeyConstraint('InspectorID', name='PK_tePremInspectors'),
    )

    InspectorID: Mapped[int] = mapped_column(Integer, primary_key=True)
    InspectorName: Mapped[str] = mapped_column(CHAR(55, 'Latin1_General_CI_AS'), nullable=False)
    InspectorLabelCode: Mapped[Optional[str]] = mapped_column(CHAR(30, 'Latin1_General_CI_AS'))


t_tePremPurchaseLines = Table(
    'tePremPurchaseLines', Base.metadata,
    Column('ItemPurchaseLineID', BigInteger, nullable=False),
    Column('PurchaseLineID', BigInteger, nullable=False),
    Column('PurchaseID', BigInteger, nullable=False),
    Column('LineNumber', BigInteger, nullable=False),
    Column('LineTypeID', CHAR(1, 'Latin1_General_CI_AS'), nullable=False),
    Column('Description', CHAR(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('TaxExclusiveTotal', Float(53), nullable=False),
    Column('TaxInclusiveTotal', Float(53), nullable=False),
    Column('JobID', BigInteger, nullable=False),
    Column('TaxCodeID', BigInteger, nullable=False),
    Column('TaxBasisAmount', Float(53), nullable=False),
    Column('TaxBasisAmountIsInclusive', CHAR(1, 'Latin1_General_CI_AS'), nullable=False),
    Column('Quantity', Float(53), nullable=False),
    Column('ItemID', BigInteger, nullable=False),
    Column('TaxExclusiveUnitPrice', Float(53), nullable=False),
    Column('TaxInclusiveUnitPrice', Float(53), nullable=False),
    Column('Discount', Float(53), nullable=False),
    Column('QtyReceived', Integer),
    Column('Barcode', String(20, 'Latin1_General_CI_AS')),
    Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS')),
    Column('ItemName', Unicode(30, 'Latin1_General_CI_AS'))
)


class TePremPurchases(Base):
    __tablename__ = 'tePremPurchases'
    __table_args__ = (
        PrimaryKeyConstraint('PurchaseID', name='PK_tePremPurchases'),
    )

    PurchaseID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    PurchaseNumber: Mapped[str] = mapped_column(String(8, 'Latin1_General_CI_AS'), nullable=False)
    SupplierInvoiceNumber: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    IsHistorical: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    BackorderPurchaseID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsThirteenthPeriod: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddress: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine1: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine2: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine3: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine4: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    PurchaseTypeID: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    PurchaseStatusID: Mapped[str] = mapped_column(String(2, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalPaid: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDeposits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDebits: Mapped[float] = mapped_column(Float(53), nullable=False)
    TotalDiscounts: Mapped[float] = mapped_column(Float(53), nullable=False)
    OutstandingBalance: Mapped[float] = mapped_column(Float(53), nullable=False)
    Memo: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Comment: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsTaxInclusive: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    IsPrinted: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    OrderStatus: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Latin1_General_CI_AS'))


t_tePremSaleLines = Table(
    'tePremSaleLines', Base.metadata,
    Column('ItemSaleLineID', BigInteger, nullable=False),
    Column('SaleLineID', BigInteger, nullable=False),
    Column('SaleID', BigInteger, nullable=False),
    Column('LineNumber', BigInteger, nullable=False),
    Column('LineTypeID', CHAR(1, 'Latin1_General_CI_AS'), nullable=False),
    Column('Description', CHAR(255, 'Latin1_General_CI_AS')),
    Column('TaxExclusiveTotal', MONEY, nullable=False),
    Column('TaxInclusiveTotal', MONEY, nullable=False),
    Column('JobID', BigInteger, nullable=False),
    Column('TaxCodeID', BigInteger, nullable=False),
    Column('TaxBasisAmount', MONEY, nullable=False),
    Column('TaxBasisAmountIsInclusive', CHAR(1, 'Latin1_General_CI_AS'), nullable=False),
    Column('Quantity', Float(53), nullable=False),
    Column('ItemID', BigInteger, nullable=False),
    Column('TaxExclusiveUnitPrice', MONEY, nullable=False),
    Column('TaxInclusiveUnitPrice', MONEY, nullable=False),
    Column('Discount', Float(53), nullable=False),
    Column('QtyReceived', Integer),
    Column('Barcode', String(20, 'Latin1_General_CI_AS')),
    Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS')),
    Column('ItemName', Unicode(30, 'Latin1_General_CI_AS'))
)


class TePremSales(Base):
    __tablename__ = 'tePremSales'
    __table_args__ = (
        PrimaryKeyConstraint('SaleID', name='PK_tePremSales'),
    )

    SaleID: Mapped[int] = mapped_column(Integer, primary_key=True)
    CardRecordID: Mapped[int] = mapped_column(Integer, nullable=False)
    SaleNumber: Mapped[str] = mapped_column(String(8, 'Latin1_General_CI_AS'), nullable=False)
    SupplierInvoiceNumber: Mapped[str] = mapped_column(String(20, 'Latin1_General_CI_AS'), nullable=False)
    IsHistorical: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    BackorderSaleID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsThirteenthPeriod: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddress: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine1: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine2: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine3: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShipToAddressLine4: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    SaleTypeID: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    SaleStatusID: Mapped[str] = mapped_column(String(2, 'Latin1_General_CI_AS'), nullable=False)
    TermsID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalLines: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxExclusiveFreight: Mapped[float] = mapped_column(Float(53), nullable=False)
    TaxInclusiveFreight: Mapped[Any] = mapped_column(MONEY, nullable=False)
    FreightTaxCodeID: Mapped[int] = mapped_column(Integer, nullable=False)
    TotalTax: Mapped[Any] = mapped_column(MONEY, nullable=False)
    TotalPaid: Mapped[Any] = mapped_column(MONEY, nullable=False)
    TotalDeposits: Mapped[Any] = mapped_column(MONEY, nullable=False)
    TotalDebits: Mapped[Any] = mapped_column(MONEY, nullable=False)
    TotalDiscounts: Mapped[Any] = mapped_column(MONEY, nullable=False)
    OutstandingBalance: Mapped[Any] = mapped_column(MONEY, nullable=False)
    Memo: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    Comment: Mapped[str] = mapped_column(String(255, 'Latin1_General_CI_AS'), nullable=False)
    ShippingMethodID: Mapped[int] = mapped_column(Integer, nullable=False)
    IsTaxInclusive: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    IsPrinted: Mapped[str] = mapped_column(String(1, 'Latin1_General_CI_AS'), nullable=False)
    DaysTillPaid: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    CurrencyID: Mapped[int] = mapped_column(Integer, nullable=False)
    TransactionExchangeRate: Mapped[float] = mapped_column(Float(53), nullable=False)
    Date: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    PromisedDate: Mapped[Optional[datetime.datetime]] = mapped_column(SMALLDATETIME)
    OrderStatus: Mapped[Optional[str]] = mapped_column(CHAR(5, 'Latin1_General_CI_AS'))


t_tePremXMLPurchaseOrders = Table(
    'tePremXMLPurchaseOrders', Base.metadata,
    Column('PurchaseID', Integer, nullable=False),
    Column('SupplierName', String(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('PurchaseNumber', String(8, 'Latin1_General_CI_AS'), nullable=False),
    Column('SupplierInvoiceNumber', String(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('Date', SMALLDATETIME, nullable=False),
    Column('ShipToAddress', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('ShipToAddressLine1', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('ShipToAddressLine2', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('ShipToAddressLine3', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('ShipToAddressLine4', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('Terms', String(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('TaxExclusiveFreight', Float(53), nullable=False),
    Column('TaxInclusiveFreight', Float(53), nullable=False),
    Column('TotalTax', Float(53), nullable=False),
    Column('TotalPaid', Float(53), nullable=False),
    Column('TotalDeposits', Float(53), nullable=False),
    Column('TotalDiscounts', Float(53), nullable=False),
    Column('OutstandingBalance', Float(53), nullable=False),
    Column('Memo', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('Comment', String(255, 'Latin1_General_CI_AS'), nullable=False),
    Column('ShippingMethod', Unicode(155, 'Latin1_General_CI_AS'), nullable=False),
    Column('LineNumber', BigInteger, nullable=False),
    Column('TaxExclusiveTotal', Float(53), nullable=False),
    Column('TaxInclusiveTotal', Float(53), nullable=False),
    Column('TaxCode', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('Quantity', Float(53), nullable=False),
    Column('ItemID', BigInteger, nullable=False),
    Column('Barcode', CHAR(15, 'Latin1_General_CI_AS'), nullable=False),
    Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('ItemName', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
    Column('TaxExclusiveUnitPrice', Float(53), nullable=False),
    Column('TaxInclusiveUnitPrice', Float(53), nullable=False),
    Column('Discount', Float(53), nullable=False),
    Column('IsPrinted', String(1, 'Latin1_General_CI_AS'), nullable=False),
    Column('Currency', Unicode(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('TransactionExchangeRate', Float(53))
)


# t_vBuildWithComponents = Table(
#     'vBuildWithComponents', Base.metadata,
#     Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
#     Column('citemNumber', Unicode(30, 'Latin1_General_CI_AS')),
#     Column('ItemName', Unicode(30, 'Latin1_General_CI_AS'))
# )


# t_vItemsonOrderbyETA = Table(
#     'vItemsonOrderbyETA', Base.metadata,
#     Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
#     Column('ItemName', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
#     Column('ItemDescription', Unicode(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('ETA', CHAR(7, 'Latin1_General_CI_AS'), nullable=False),
#     Column('TotQtyOnOrder', Numeric(18, 3), nullable=False),
#     Column('NewOrderAmount', Numeric(18, 3), nullable=False)
# )


class VMYOBBarcodesConversion(Base):
    __tablename__ = 'vMYOBBarcodesConversion'
    __table_args__ = (
        PrimaryKeyConstraint('ItemID', 'Barcode', name='PK_vMYOBBarcodesConversion'),
    )

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Barcode: Mapped[str] = mapped_column(CHAR(25, 'Latin1_General_CI_AS'), primary_key=True)


# t_vOnOrderbyETAbyItemID = Table(
#     'vOnOrderbyETAbyItemID', Base.metadata,
#     Column('ETA', String(10, 'Latin1_General_CI_AS')),
#     Column('ItemID', Integer, nullable=False),
#     Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
#     Column('TotQtyOnOrder', Float(53))
# )


# t_vOnOrderbyItemID = Table(
#     'vOnOrderbyItemID', Base.metadata,
#     Column('ItemID', Integer, nullable=False),
#     Column('Description', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('TotQtyOnOrder', Float(53)),
#     Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
#     Column('PurchaseID', Integer, nullable=False),
#     Column('PurchaseNumber', String(8, 'Latin1_General_CI_AS'), nullable=False)
# )


# t_vPickingSlip = Table(
#     'vPickingSlip', Base.metadata,
#     Column('SaleID', Integer, nullable=False),
#     Column('InvoiceNumber', Unicode(8, 'Latin1_General_CI_AS')),
#     Column('LineNumber', Integer, nullable=False),
#     Column('MethodCode', CHAR(255, 'Latin1_General_CI_AS')),
#     Column('TenderAmount', Float(53)),
#     Column('TransDate', DateTime),
#     Column('ItemName', Unicode(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
#     Column('SellUnitQuantity', SmallInteger, nullable=False),
#     Column('SellUnitMeasure', Unicode(5, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Name', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Quantity', Float(53), nullable=False),
#     Column('TaxExclusiveUnitPrice', Float(53), nullable=False),
#     Column('TaxCodeID', Integer, nullable=False),
#     Column('TaxCode', String(3, 'Latin1_General_CI_AS')),
#     Column('Comment', String(2048, 'Latin1_General_CI_AS')),
#     Column('Date', SMALLDATETIME),
#     Column('ABN', String(14, 'Latin1_General_CI_AS'), nullable=False),
#     Column('CompanyName', String(50, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Address', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Phone', String(20, 'Latin1_General_CI_AS'), nullable=False),
#     Column('FaxNumber', String(20, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Email', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('TaxExclusiveTotal', Float(53), nullable=False),
#     Column('ShippingCost', Float(53)),
#     Column('ShippingInsurance', Float(53)),
#     Column('SaleOrderNo', String(50, 'Latin1_General_CI_AS')),
#     Column('AustralianPartNo', String(50, 'Latin1_General_CI_AS')),
#     Column('StoneWeightPerItem', Float(53)),
#     Column('DiamondWeightPerItem', Float(53)),
#     Column('MetalGoldWeightPerItem', Float(53)),
#     Column('NetWeight', Float(53)),
#     Column('TotalPaid', Float(53), nullable=False),
#     Column('TaxInclusiveFreight', Float(53), nullable=False),
#     Column('CardRecordID', Integer, nullable=False),
#     Column('TaxExclusiveFreight', Float(53), nullable=False),
#     Column('TotalTax', Float(53), nullable=False),
#     Column('GrossWeightOfShipment', Float(53)),
#     Column('LastName', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('FirstName', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Location', Integer),
#     Column('Street', String(255, 'Latin1_General_CI_AS')),
#     Column('City', String(255, 'Latin1_General_CI_AS')),
#     Column('State', String(255, 'Latin1_General_CI_AS')),
#     Column('PostCode', String(255, 'Latin1_General_CI_AS')),
#     Column('Country', String(255, 'Latin1_General_CI_AS')),
#     Column('ContactName', CHAR(50, 'Latin1_General_CI_AS')),
#     Column('StreetLine1', String(255, 'Latin1_General_CI_AS')),
#     Column('StreetLine2', String(255, 'Latin1_General_CI_AS')),
#     Column('StreetLine3', String(255, 'Latin1_General_CI_AS')),
#     Column('StreetLine4', String(255, 'Latin1_General_CI_AS')),
#     Column('ShipToAddress', Unicode(255, 'Latin1_General_CI_AS')),
#     Column('ShipToAddressLine1', Unicode(255, 'Latin1_General_CI_AS')),
#     Column('ShipToAddressLine2', Unicode(255, 'Latin1_General_CI_AS')),
#     Column('ShipToAddressLine3', Unicode(255, 'Latin1_General_CI_AS')),
#     Column('ShipToAddressLine4', Unicode(255, 'Latin1_General_CI_AS')),
#     Column('SalesName', String(60, 'Latin1_General_CI_AS')),
#     Column('SaleLastName', String(60, 'Latin1_General_CI_AS')),
#     Column('SalesFirstName', String(60, 'Latin1_General_CI_AS')),
#     Column('CustomerPONumber', Unicode(20, 'Latin1_General_CI_AS')),
#     Column('Discount', Float(53), nullable=False),
#     Column('DeliveryDate', DateTime),
#     Column('RunNo', CHAR(15, 'Latin1_General_CI_AS')),
#     Column('FreightCompany', String(50, 'Latin1_General_CI_AS')),
#     Column('ConsignmentNo', String(55, 'Latin1_General_CI_AS')),
#     Column('dup', String(55, 'Latin1_General_CI_AS')),
#     Column('QuantityOnHand', Float(53), nullable=False),
#     Column('SortField', String(55, 'Latin1_General_CI_AS'))
# )


# t_vPurchaseLinesbyOrder = Table(
#     'vPurchaseLinesbyOrder', Base.metadata,
#     Column('PurchaseID', Integer, nullable=False),
#     Column('PurchaseNumber', String(8, 'Latin1_General_CI_AS'), nullable=False),
#     Column('SupplierInvoiceNumber', String(20, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Date', DateTime),
#     Column('TaxExclusiveFreight', Float(53), nullable=False),
#     Column('TaxInclusiveFreight', Float(53), nullable=False),
#     Column('TotalTax', Float(53), nullable=False),
#     Column('PromisedDate', DateTime),
#     Column('Description', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('TaxExclusiveTotal', Float(53), nullable=False),
#     Column('TaxInclusiveTotal', Float(53), nullable=False),
#     Column('Quantity', Float(53), nullable=False),
#     Column('ItemID', Integer, nullable=False),
#     Column('TaxExclusiveUnitPrice', Float(53), nullable=False),
#     Column('TaxInclusiveUnitPrice', Float(53), nullable=False),
#     Column('Discount', Float(53), nullable=False)
# )


# t_vTaxInvoiceItems = Table(
#     'vTaxInvoiceItems', Base.metadata,
#     Column('ItemNumber', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
#     Column('ItemNameInChinese', Unicode(155, 'Latin1_General_CI_AS')),
#     Column('Quantity', Float(53), nullable=False),
#     Column('TaxExclusiveUnitPrice', Float(53), nullable=False),
#     Column('Discount', Float(53), nullable=False),
#     Column('TaxExclusiveTotal', Float(53), nullable=False),
#     Column('ShipToAddress', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('ShipToAddressLine1', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('ShipToAddressLine2', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Comment', String(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('ShipVia', String(255, 'Latin1_General_CI_AS')),
#     Column('ABN', Unicode(14, 'Latin1_General_CI_AS')),
#     Column('TaxCode', String(3, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Freight', Float(53), nullable=False),
#     Column('TotalTax', Float(53), nullable=False),
#     Column('OutstandingBalance', Float(53), nullable=False),
#     Column('TaxPercentageRate', Float(53), nullable=False),
#     Column('PurchaseID', Integer, nullable=False),
#     Column('Terms', String(100, 'Latin1_General_CI_AS')),
#     Column('ItemDescription', Unicode(255, 'Latin1_General_CI_AS'), nullable=False),
#     Column('Date', SMALLDATETIME),
#     Column('TotalPaid', Float(53), nullable=False),
#     Column('ItemName', Unicode(30, 'Latin1_General_CI_AS'), nullable=False),
#     Column('BuyUnitMeasure', Unicode(5, 'Latin1_General_CI_AS'), nullable=False),
#     Column('BuyUnitQuantity', SmallInteger, nullable=False),
#     Column('Name', Unicode(52, 'Latin1_General_CI_AS')),
#     Column('MethodOfPaymentID', Integer),
#     Column('BSBCode', Unicode(7, 'Latin1_General_CI_AS')),
#     Column('BankAccountNumber', Unicode(19, 'Latin1_General_CI_AS')),
#     Column('BankAccountName', Unicode(32, 'Latin1_General_CI_AS')),
#     Column('PaymentNotes', Unicode(255, 'Latin1_General_CI_AS'))
# )
