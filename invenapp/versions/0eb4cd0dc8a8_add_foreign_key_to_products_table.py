"""Add foreign key to products table

Revision ID: 0eb4cd0dc8a8
Revises: 301686dedbf9
Create Date: 2024-12-31 02:01:50.104088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0eb4cd0dc8a8'
down_revision: Union[str, None] = '301686dedbf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    """
        Upgrade the database schema.
        Add a foreign key constraint between the `products` table and the `financial_quarters` table.
        """
    op.create_foreign_key("fk_products_financial_quarters", 'products', 'financial_quarters', ['financial_quarter_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """
        Downgrade the database schema.
        Remove the foreign key constraint between the `products` table and the `financial_quarters` table.
        """
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_products_financial_quarters", 'products', type_='foreignkey')
    # ### end Alembic commands ###
