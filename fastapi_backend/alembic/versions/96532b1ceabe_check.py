"""check

Revision ID: 96532b1ceabe
Revises: dff5b328c652
Create Date: 2026-03-01 21:56:07.897523
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '96532b1ceabe'
down_revision = 'dff5b328c652'
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column(
        'eParcel_Header', 'TransactionId',
        existing_type=sa.NVARCHAR(length=20, collation='Latin1_General_CI_AS'),
        type_=sa.Unicode(length=40, collation='Latin1_General_CI_AS'),
        existing_nullable=False
    )

    op.alter_column(
        'eParcel_Header', 'ParentId',
        existing_type=sa.NVARCHAR(length=20, collation='Latin1_General_CI_AS'),
        type_=sa.Unicode(length=40, collation='Latin1_General_CI_AS'),
        existing_nullable=True
    )

    op.alter_column(
        'eParcel_Header', 'TransactionSequence',
        existing_type=sa.NVARCHAR(length=20, collation='Latin1_General_CI_AS'),
        type_=sa.Unicode(length=40, collation='Latin1_General_CI_AS'),
        existing_nullable=True
    )

    op.alter_column(
        'eParcel_Header', 'ApplicationId',
        existing_type=sa.NVARCHAR(length=10, collation='Latin1_General_CI_AS'),
        type_=sa.Unicode(length=20, collation='Latin1_General_CI_AS'),
        existing_nullable=True
    )

    # FIXED COLUMN
    op.alter_column(
        'tOSTINVENTORYCOUNTS', 'COUNTNOTES',
        existing_type=sa.TEXT(collation='Latin1_General_CI_AS'),
        type_=sa.Unicode(length=16, collation='Latin1_General_CI_AS'),
        existing_nullable=True
    )


def downgrade():

    op.alter_column(
        'tOSTINVENTORYCOUNTS', 'COUNTNOTES',
        existing_type=sa.Unicode(length=16, collation='Latin1_General_CI_AS'),
        type_=sa.TEXT(collation='Latin1_General_CI_AS'),
        existing_nullable=True
    )

    op.alter_column(
        'eParcel_Header', 'ApplicationId',
        existing_type=sa.Unicode(length=20, collation='Latin1_General_CI_AS'),
        type_=sa.NVARCHAR(length=10, collation='Latin1_General_CI_AS'),
        existing_nullable=True
    )

    op.alter_column(
        'eParcel_Header', 'TransactionSequence',
        existing_type=sa.Unicode(length=40, collation='Latin1_General_CI_AS'),
        type_=sa.NVARCHAR(length=20, collation='Latin1_General_CI_AS'),
        existing_nullable=True
    )

    op.alter_column(
        'eParcel_Header', 'ParentId',
        existing_type=sa.Unicode(length=40, collation='Latin1_General_CI_AS'),
        type_=sa.NVARCHAR(length=20, collation='Latin1_General_CI_AS'),
        existing_nullable=True
    )

    op.alter_column(
        'eParcel_Header', 'TransactionId',
        existing_type=sa.Unicode(length=40, collation='Latin1_General_CI_AS'),
        type_=sa.NVARCHAR(length=20, collation='Latin1_General_CI_AS'),
        existing_nullable=False
    )