"""Add start_date, end_date

Revision ID: 9064b0fa285e
Revises: 3ce73f7cb147
Create Date: 2025-06-03 14:38:25.605405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9064b0fa285e'
down_revision: Union[str, None] = '3ce73f7cb147'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # The columns already exist in the Railway database, so skip adding them again.
    # op.add_column("travel_plans", sa.Column("start_date", sa.DateTime(), nullable=False))
    # op.add_column("travel_plans", sa.Column("end_date", sa.DateTime(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("travel_plans", "end_date")
    op.drop_column("travel_plans", "start_date")


