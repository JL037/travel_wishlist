"""remove date from travel_plans

Revision ID: 5ca0c3e64261
Revises: 9064b0fa285e
Create Date: 2025-06-03 14:47:14.613729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ca0c3e64261'
down_revision: Union[str, None] = '9064b0fa285e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
      op.drop_column("travel_plans", "date")


def downgrade() -> None:
    op.add_column(
        "travel_plans",
        sa.Column("date", sa.Date(), nullable=False)
    )
