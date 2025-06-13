"""Add notes column to travel_plans

Revision ID: 8edd4036eb6d
Revises: 1b671c0ebb26
Create Date: 2025-06-11 18:35:55.655140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8edd4036eb6d'
down_revision: Union[str, None] = '1b671c0ebb26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    from alembic import op
    import sqlalchemy as sa
    op.add_column('travel_plans', sa.Column('notes', sa.String(), nullable=True))

def downgrade() -> None:
    from alembic import op
    op.drop_column('travel_plans', 'notes')

