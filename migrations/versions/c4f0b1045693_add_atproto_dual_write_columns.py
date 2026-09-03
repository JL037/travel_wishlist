"""Add AT Protocol dual-write columns (Phase 2)

Revision ID: c4f0b1045693
Revises: b6c6eb06ba9a
Create Date: 2026-09-03 23:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4f0b1045693'
down_revision: Union[str, None] = 'b6c6eb06ba9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_SYNC_TABLES = ("wishlist_location", "visited_location", "travel_plans")


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('atproto_sync_enabled', sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    for table in _SYNC_TABLES:
        op.add_column(table, sa.Column('atproto_record_uri', sa.String(), nullable=True))
        op.add_column(table, sa.Column('atproto_record_cid', sa.String(), nullable=True))
        op.add_column(
            table,
            sa.Column('atproto_sync_pending', sa.Boolean(), nullable=False, server_default=sa.false()),
        )
        op.add_column(table, sa.Column('atproto_sync_error', sa.Text(), nullable=True))


def downgrade() -> None:
    for table in _SYNC_TABLES:
        op.drop_column(table, 'atproto_sync_error')
        op.drop_column(table, 'atproto_sync_pending')
        op.drop_column(table, 'atproto_record_cid')
        op.drop_column(table, 'atproto_record_uri')

    op.drop_column('users', 'atproto_sync_enabled')
