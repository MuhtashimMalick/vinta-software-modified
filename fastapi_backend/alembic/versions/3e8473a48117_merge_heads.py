"""merge_heads

Revision ID: 3e8473a48117
Revises: 17b5515f26bc, 24506826c4c7
Create Date: 2026-03-08 20:29:09.495273

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '3e8473a48117'
down_revision = ('17b5515f26bc', '24506826c4c7')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
