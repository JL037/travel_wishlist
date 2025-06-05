"""Recreate user_saved_cities table

Revision ID: 3ce73f7cb147
Revises: 94f826cfd104
Create Date: 2025-06-03 11:18:42.841861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ce73f7cb147'
down_revision: Union[str, None] = '94f826cfd104'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # The table already exists in the Railway database, so skip creating it again.
    # op.create_table(
    #     'user_saved_cities',
    #     sa.Column('id', sa.Integer(), primary_key=True),
    #     sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
    #     sa.Column('city', sa.String(), nullable=False),
    # )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user_saved_cities')
