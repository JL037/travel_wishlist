"""Manually add ON DELETE CASCADE to location FKs

Revision ID: 1d8572dd11fd
Revises: 8edd4036eb6d
Create Date: 2025-06-11 22:49:20.438009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d8572dd11fd'
down_revision: Union[str, None] = '8edd4036eb6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Drop and recreate foreign key on wishlist_location.owner_id
    op.drop_constraint('wishlist_location_owner_id_fkey', 'wishlist_location', type_='foreignkey')
    op.create_foreign_key(
        'wishlist_location_owner_id_fkey',
        'wishlist_location', 'users',
        ['owner_id'], ['id'],
        ondelete='CASCADE'
    )

    # Drop and recreate foreign key on visited_location.owner_id
    op.drop_constraint('visited_location_owner_id_fkey', 'visited_location', type_='foreignkey')
    op.create_foreign_key(
        'visited_location_owner_id_fkey',
        'visited_location', 'users',
        ['owner_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    # Reverse CASCADE logic by recreating the FKs without ondelete
    op.drop_constraint('wishlist_location_owner_id_fkey', 'wishlist_location', type_='foreignkey')
    op.create_foreign_key(
        'wishlist_location_owner_id_fkey',
        'wishlist_location', 'users',
        ['owner_id'], ['id']
    )

    op.drop_constraint('visited_location_owner_id_fkey', 'visited_location', type_='foreignkey')
    op.create_foreign_key(
        'visited_location_owner_id_fkey',
        'visited_location', 'users',
        ['owner_id'], ['id']
    )
