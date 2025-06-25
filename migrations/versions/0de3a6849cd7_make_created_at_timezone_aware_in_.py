"""Make created_at timezone-aware in refresh_tokens

Revision ID: 0de3a6849cd7
Revises: 1d8572dd11fd
Create Date: 2025-06-18 19:22:21.700063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0de3a6849cd7'
down_revision: Union[str, None] = '1d8572dd11fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Manually make created_at timezone-aware in refresh_tokens."""
    op.alter_column(
        'refresh_tokens',
        'created_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(timezone=False),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Revert created_at to timezone-naive in refresh_tokens."""
    op.alter_column(
        'refresh_tokens',
        'created_at',
        type_=sa.DateTime(timezone=False),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=True,
    )
