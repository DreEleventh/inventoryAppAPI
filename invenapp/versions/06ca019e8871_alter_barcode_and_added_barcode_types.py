"""alter barcode and added barcode types

Revision ID: 06ca019e8871
Revises: 3cdc99604e5f
Create Date: 2025-01-05 16:39:57.879189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06ca019e8871'
down_revision: Union[str, None] = '3cdc99604e5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the Enum type 
barcode_type_enum = sa.Enum('UPC', 'EAN_13', 'EAN_8', 'CODE_128', 'QR_CODE', name='barcode_type')

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Create the ENUM type in the database
    barcode_type_enum.create(op.get_bind())
    op.add_column('products', sa.Column('barcode_type', barcode_type_enum, nullable=False))
    op.alter_column('products', 'barcode',
               existing_type=sa.VARCHAR(length=12),
               type_=sa.String(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'barcode',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=12),
               existing_nullable=False)
    op.drop_column('products', 'barcode_type')
    
    # Drop the enum type from the database
    barcode_type_enum.drop(op.get_bind)
    # ### end Alembic commands ###
