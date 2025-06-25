"""Make WishlistLocation.name nullable

Revision ID: 47c18d3434d2
Revises: c279bba35bae
Create Date: 2025-06-25 21:21:14.432646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47c18d3434d2'
down_revision: Union[str, None] = 'c279bba35bae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('wishlist_location', 'name',
                    existing_type=sa.String(),
                    nullable=True)


def downgrade() -> None:
    op.alter_column('wishlist_location', 'name',
                    existing_type=sa.String(),
                    nullable=False)

