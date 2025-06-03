"""Add username column to users

Revision ID: 8ad8ecc605af
Revises: 923abf01832a
Create Date: 2025-06-02 13:09:01.382931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ad8ecc605af'
down_revision: Union[str, None] = '923abf01832a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column("users", sa.Column("username", sa.String(), nullable=False))
    


def downgrade() -> None:
    op.drop_column("users", "username")
