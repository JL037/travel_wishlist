"""add user_saved_cities table

Revision ID: 043964ab584e
Revises: 8ad8ecc605af
Create Date: 2025-06-02 19:34:34.511821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '043964ab584e'
down_revision: Union[str, None] = '8ad8ecc605af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_saved_cities",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("city", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user_saved_cities")