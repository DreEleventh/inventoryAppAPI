"""upgrade product category relationship

Revision ID: 7f8193bf1fe6
Revises: 2b5846f78671
Create Date: 2025-01-01 13:32:22.499253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f8193bf1fe6'
down_revision: Union[str, None] = '2b5846f78671'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
