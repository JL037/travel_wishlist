"""Actually add latitude and longitude to visited_location

Revision ID: 923abf01832a
Revises: 0bf340480665
Create Date: 2025-06-01 10:35:35.405157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '923abf01832a'
down_revision: Union[str, None] = '0bf340480665'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("visited_location", sa.Column("latitude", sa.Float(), nullable=True))
    op.add_column("visited_location", sa.Column("longitude", sa.Float(), nullable=True))



def downgrade() -> None:
    op.drop_column("visited_location", "longitude")
    op.drop_column("visited_location", "latitude")
