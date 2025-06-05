"""Add latitude and longitude to visited_location

Revision ID: 0bf340480665
Revises: 3d09dcaf9723
Create Date: 2025-06-01 10:32:25.908740

"""
from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = '0bf340480665'
down_revision: Union[str, None] = '3d09dcaf9723'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
