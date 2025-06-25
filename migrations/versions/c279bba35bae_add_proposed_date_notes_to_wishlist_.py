"""add proposed_date, notes to wishlist_location

Revision ID: c279bba35bae
Revises: 0de3a6849cd7
Create Date: 2025-06-20 19:31:55.567283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c279bba35bae'
down_revision: Union[str, None] = '0de3a6849cd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('wishlist_location', sa.Column('proposed_date', sa.Date(), nullable=True))
    op.add_column('wishlist_location', sa.Column('notes', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('wishlist_location', 'notes')
    op.drop_column('wishlist_location', 'proposed_date')
