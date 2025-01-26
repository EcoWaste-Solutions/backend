"""fix data type

Revision ID: e3c08487cc1a
Revises: 567de8b4c990
Create Date: 2025-01-24 22:57:52.140857
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e3c08487cc1a'
down_revision: Union[str, None] = '567de8b4c990'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Change the data type of the "image" column to String
    op.alter_column(
        table_name='reportWaste',
        column_name='image',
        existing_type=sa.ARRAY(sa.String()),  # Original type
        type_=sa.String(),  # New type
        existing_nullable=False
    )

def downgrade() -> None:
    # Revert the data type of the "image" column back to ARRAY(String)
    op.alter_column(
        table_name='reportWaste',
        column_name='image',
        existing_type=sa.String(),  # Current type
        type_=sa.ARRAY(sa.String()),  # Original type
        existing_nullable=False
    )