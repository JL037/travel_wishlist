"""Add location column to travel_plans

Revision ID: 1b671c0ebb26
Revises: f6eabf2b9c7b
Create Date: 2025-06-11 18:25:42.534070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1b671c0ebb26'
down_revision: Union[str, None] = 'f6eabf2b9c7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('travel_plans', sa.Column('location', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('travel_plans', 'location')
