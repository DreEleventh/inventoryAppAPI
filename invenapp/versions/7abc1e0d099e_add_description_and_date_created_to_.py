"""Add description and date_created to user_group table

Revision ID: 7abc1e0d099e
Revises: 
Create Date: 2024-12-30 23:51:45.761915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '7abc1e0d099e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'description' column
    op.add_column(
        'user_groups',
        sa.Column('description',
                  sa.String(length=150),
                  nullable=True)
    )

    # Add 'date_created' column with default value
    op.add_column(
        'user_groups',
        sa.Column('date_created',
                  sa.TIMESTAMP(),
                  server_default=text('CURRENT_TIMESTAMP'),
                  nullable=False)
    )



def downgrade() -> None:
    pass
