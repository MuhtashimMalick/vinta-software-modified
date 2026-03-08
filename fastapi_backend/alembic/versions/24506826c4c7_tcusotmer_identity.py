"""tcusotmer identity

Revision ID: 24506826c4c7
Revises: 5173500b2587
Create Date: 2026-03-07 22:16:05.829716

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '24506826c4c7'
down_revision = '5173500b2587'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Backup
    op.execute("SELECT * INTO dbo.tCustomers_backup FROM dbo.tCustomers")

    # Step 2: Drop all FK constraints pointing TO tCustomers
    op.execute("""
        DECLARE @sql NVARCHAR(MAX) = ''
        SELECT @sql += 'ALTER TABLE ' + QUOTENAME(tp.name) + 
                       ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + '; '
        FROM sys.foreign_keys fk
        JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
        JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        JOIN sys.columns c ON fkc.referenced_column_id = c.column_id 
            AND fkc.referenced_object_id = c.object_id
        JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
        WHERE tr.name = 'tCustomers' AND c.name = 'CustomerID'
        EXEC sp_executesql @sql
    """)

    # Step 3: Drop indexes
    op.execute("""
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_tCustomers_Change_Control' AND object_id = OBJECT_ID('dbo.tCustomers'))
            DROP INDEX IX_tCustomers_Change_Control ON dbo.tCustomers
        IF EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_tCustomers_Name' AND object_id = OBJECT_ID('dbo.tCustomers'))
            DROP INDEX IX_tCustomers_Name ON dbo.tCustomers
    """)

    # Step 4: Drop PK
    op.execute("""
        DECLARE @pkName NVARCHAR(256)
        SELECT @pkName = name FROM sys.key_constraints 
        WHERE type = 'PK' AND parent_object_id = OBJECT_ID('dbo.tCustomers')
        IF @pkName IS NOT NULL
            EXEC('ALTER TABLE dbo.tCustomers DROP CONSTRAINT ' + @pkName)
    """)

    # Step 5: Create new table with IDENTITY
    op.execute("""
        CREATE TABLE dbo.tCustomers_new (
            CustomerID                  INT IDENTITY(1,1) NOT NULL,
            CustomerCode                VARCHAR(10) COLLATE Latin1_General_CI_AS NULL,
            CardRecordID                INT NOT NULL,
            CardIdentification          NVARCHAR(16) COLLATE Latin1_General_CI_AS NOT NULL,
            Name                        VARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
            LastName                    VARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
            FirstName                   VARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
            IsIndividual                NVARCHAR(1) COLLATE Latin1_General_CI_AS NOT NULL,
            IsInactive                  NVARCHAR(1) COLLATE Latin1_General_CI_AS NOT NULL,
            Notes                       NVARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
            IdentifierID                NVARCHAR(26) COLLATE Latin1_General_CI_AS NOT NULL,
            CustomField1                NVARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
            CustomField2                NVARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
            CustomField3                NVARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
            TermsID                     INT NOT NULL,
            ABN                         NVARCHAR(14) COLLATE Latin1_General_CI_AS NOT NULL,
            ABNBranch                   NVARCHAR(11) COLLATE Latin1_General_CI_AS NOT NULL,
            PriceLevelID                NVARCHAR(3) COLLATE Latin1_General_CI_AS NOT NULL,
            TaxIDNumber                 NVARCHAR(19) COLLATE Latin1_General_CI_AS NOT NULL,
            TaxCodeID                   INT NOT NULL,
            FreightTaxCodeID            INT NOT NULL,
            UseCustomerTaxCode          NVARCHAR(1) COLLATE Latin1_General_CI_AS NOT NULL,
            CreditLimit                 FLOAT(53) NOT NULL,
            VolumeDiscount              FLOAT(53) NOT NULL,
            CurrentBalance              FLOAT(53) NOT NULL,
            TotalDeposits               FLOAT(53) NOT NULL,
            TotalReceivableDays         INT NOT NULL,
            TotalPaidInvoices           INT NOT NULL,
            HighestInvoiceAmount        FLOAT(53) NOT NULL,
            HighestReceivableAmount     FLOAT(53) NOT NULL,
            PaymentCardNumber           NVARCHAR(25) COLLATE Latin1_General_CI_AS NOT NULL,
            PaymentNameOnCard           NVARCHAR(50) COLLATE Latin1_General_CI_AS NOT NULL,
            PaymentBankAccountName      NVARCHAR(32) COLLATE Latin1_General_CI_AS NOT NULL,
            PaymentNotes                NVARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
            HourlyBillingRate           FLOAT(53) NOT NULL,
            SaleLayoutID                NVARCHAR(1) COLLATE Latin1_General_CI_AS NOT NULL,
            PrintedForm                 NVARCHAR(34) COLLATE Latin1_General_CI_AS NOT NULL,
            ChangeControl               CHAR(20) COLLATE Latin1_General_CI_AS NOT NULL,
            CurrencyID                  INT NULL,
            Picture                     NVARCHAR(255) COLLATE Latin1_General_CI_AS NULL,
            Identifiers                 NVARCHAR(26) COLLATE Latin1_General_CI_AS NULL,
            CustomList1ID               INT NULL,
            CustomList2ID               INT NULL,
            CustomList3ID               INT NULL,
            CustomerSince               SMALLDATETIME NULL,
            LastSaleDate                SMALLDATETIME NULL,
            LastPaymentDate             SMALLDATETIME NULL,
            MethodOfPaymentID           INT NULL,
            PaymentExpirationDate       NVARCHAR(10) COLLATE Latin1_General_CI_AS NULL,
            PaymentBSB                  VARCHAR(11) COLLATE Latin1_General_CI_AS NULL,
            PaymentBankAccountNumber    VARCHAR(20) COLLATE Latin1_General_CI_AS NULL,
            IncomeAccountID             INT NULL,
            SalespersonID               INT NULL,
            SaleCommentID               INT NULL,
            ShippingMethodID            INT NULL,
            GSTIDNumber                 VARCHAR(20) COLLATE Latin1_General_CI_AS NULL,
            ReceiptMemo                 VARCHAR(255) COLLATE Latin1_General_CI_AS NULL,
            PaymentBankBranch           VARCHAR(10) COLLATE Latin1_General_CI_AS NULL,
            PaymentAddress              VARCHAR(30) COLLATE Latin1_General_CI_AS NULL,
            PaymentZIP                  VARCHAR(10) COLLATE Latin1_General_CI_AS NULL,
            PaymentCardVerification     VARCHAR(10) COLLATE Latin1_General_CI_AS NULL,
            ACCNO                       INT NULL,
            ONHOLD                      CHAR(1) COLLATE Latin1_General_CI_AS NULL,
            CONSTRAINT PK_tCustomers PRIMARY KEY (CustomerID)
        )
    """)

    # Step 6: Copy ALL data preserving original CustomerID values
    op.execute("""
        SET IDENTITY_INSERT dbo.tCustomers_new ON

        INSERT INTO dbo.tCustomers_new (
            CustomerID, CustomerCode, CardRecordID, CardIdentification, Name, LastName,
            FirstName, IsIndividual, IsInactive, Notes, IdentifierID, CustomField1,
            CustomField2, CustomField3, TermsID, ABN, ABNBranch, PriceLevelID,
            TaxIDNumber, TaxCodeID, FreightTaxCodeID, UseCustomerTaxCode, CreditLimit,
            VolumeDiscount, CurrentBalance, TotalDeposits, TotalReceivableDays,
            TotalPaidInvoices, HighestInvoiceAmount, HighestReceivableAmount,
            PaymentCardNumber, PaymentNameOnCard, PaymentBankAccountName, PaymentNotes,
            HourlyBillingRate, SaleLayoutID, PrintedForm, ChangeControl, CurrencyID,
            Picture, Identifiers, CustomList1ID, CustomList2ID, CustomList3ID,
            CustomerSince, LastSaleDate, LastPaymentDate, MethodOfPaymentID,
            PaymentExpirationDate, PaymentBSB, PaymentBankAccountNumber, IncomeAccountID,
            SalespersonID, SaleCommentID, ShippingMethodID, GSTIDNumber, ReceiptMemo,
            PaymentBankBranch, PaymentAddress, PaymentZIP, PaymentCardVerification,
            ACCNO, ONHOLD
        )
        SELECT
            CustomerID, CustomerCode, CardRecordID, CardIdentification, Name, LastName,
            FirstName, IsIndividual, IsInactive, Notes, IdentifierID, CustomField1,
            CustomField2, CustomField3, TermsID, ABN, ABNBranch, PriceLevelID,
            TaxIDNumber, TaxCodeID, FreightTaxCodeID, UseCustomerTaxCode, CreditLimit,
            VolumeDiscount, CurrentBalance, TotalDeposits, TotalReceivableDays,
            TotalPaidInvoices, HighestInvoiceAmount, HighestReceivableAmount,
            PaymentCardNumber, PaymentNameOnCard, PaymentBankAccountName, PaymentNotes,
            HourlyBillingRate, SaleLayoutID, PrintedForm, ChangeControl, CurrencyID,
            Picture, Identifiers, CustomList1ID, CustomList2ID, CustomList3ID,
            CustomerSince, LastSaleDate, LastPaymentDate, MethodOfPaymentID,
            PaymentExpirationDate, PaymentBSB, PaymentBankAccountNumber, IncomeAccountID,
            SalespersonID, SaleCommentID, ShippingMethodID, GSTIDNumber, ReceiptMemo,
            PaymentBankBranch, PaymentAddress, PaymentZIP, PaymentCardVerification,
            ACCNO, ONHOLD
        FROM dbo.tCustomers

        SET IDENTITY_INSERT dbo.tCustomers_new OFF
    """)

    # Step 7: Reseed to continue from max existing ID
    op.execute("""
        DECLARE @maxID INT
        SELECT @maxID = ISNULL(MAX(CustomerID), 0) FROM dbo.tCustomers_new
        DBCC CHECKIDENT ('dbo.tCustomers_new', RESEED, @maxID)
    """)

    # Step 8: Drop old table
    op.execute("DROP TABLE dbo.tCustomers")

    # Step 9: Rename new table
    op.execute("EXEC sp_rename 'dbo.tCustomers_new', 'tCustomers'")

    # Step 10: Recreate indexes
    op.execute("""
        CREATE INDEX IX_tCustomers_Change_Control ON dbo.tCustomers (ChangeControl)
        CREATE INDEX IX_tCustomers_Name ON dbo.tCustomers (Name)
    """)

    # Step 11: Recreate any FK constraints that were dropped in Step 2
    # (they will be auto-detected from backup metadata and recreated)
    op.execute("""
        DECLARE @sql NVARCHAR(MAX) = ''
        SELECT @sql += 
            'ALTER TABLE ' + QUOTENAME(tp.name) + 
            ' ADD CONSTRAINT ' + QUOTENAME(fk.name) + 
            ' FOREIGN KEY (' + QUOTENAME(cc.name) + ')' +
            ' REFERENCES dbo.tCustomers(' + QUOTENAME(rc.name) + '); '
        FROM sys.foreign_keys fk
        JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
        JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        JOIN sys.columns cc ON fkc.parent_column_id = cc.column_id 
            AND fkc.parent_object_id = cc.object_id
        JOIN sys.columns rc ON fkc.referenced_column_id = rc.column_id 
            AND fkc.referenced_object_id = rc.object_id
        JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
        WHERE tr.name = 'tCustomers_backup'
        EXEC sp_executesql @sql
    """)


def downgrade():
    op.execute("""
        IF OBJECT_ID('dbo.tCustomers_backup') IS NOT NULL
        BEGIN
            DROP TABLE IF EXISTS dbo.tCustomers
            EXEC sp_rename 'dbo.tCustomers_backup', 'tCustomers'
        END
    """)