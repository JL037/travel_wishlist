"""Make name and description optional for wishlist_location

Revision ID: f6eabf2b9c7b
Revises: bcdba63a64af
Create Date: 2025-06-08 13:05:15.737229
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f6eabf2b9c7b'
down_revision: Union[str, None] = 'bcdba63a64af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: make name and description optional in wishlist_location."""
    op.alter_column('wishlist_location', 'name',
               existing_type=sa.String(length=255),
               nullable=True)
    op.alter_column('wishlist_location', 'description',
               existing_type=sa.Text(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema: revert name and description to NOT NULL."""
    op.alter_column('wishlist_location', 'description',
               existing_type=sa.Text(),
               nullable=False)
    op.alter_column('wishlist_location', 'name',
               existing_type=sa.String(length=255),
               nullable=False)
