"""add column

Revision ID: 6bc549f30cec
Revises: e3c08487cc1a
Create Date: 2025-01-25 10:18:39.591810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bc549f30cec'
down_revision: Union[str, None] = 'e3c08487cc1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reportWaste', sa.Column('qrCodeUpdatedAt', sa.DateTime(), nullable=True))
    op.add_column('reportWaste', sa.Column('qrCodeAddedBy', sa.String(), nullable=True))
    op.create_foreign_key(None, 'reportWaste', 'users', ['qrCodeAddedBy'], ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reportWaste', type_='foreignkey')
    op.drop_column('reportWaste', 'qrCodeAddedBy')
    op.drop_column('reportWaste', 'qrCodeUpdatedAt')
    # ### end Alembic commands ###
