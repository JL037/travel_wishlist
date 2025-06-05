"""add travel_plan table

Revision ID: 94f826cfd104
Revises: 74d7c6a2ea3c
Create Date: 2025-06-03 10:42:50.794849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94f826cfd104'
down_revision: Union[str, None] = '74d7c6a2ea3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # The table already exists in the Railway database, so comment out the creation commands.
    # op.create_table('travel_plans',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('user_id', sa.Integer(), nullable=False),
    #     sa.Column('date', sa.Date(), nullable=False),
    #     sa.Column('location', sa.String(), nullable=False),
    #     sa.Column('notes', sa.String(), nullable=True),
    #     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    #     sa.PrimaryKeyConstraint('id')
    # )
    # op.create_index(op.f('ix_travel_plans_id'), 'travel_plans', ['id'], unique=False)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # These remain active, so you can still drop the table if rolling back.
    op.drop_index(op.f('ix_travel_plans_id'), table_name='travel_plans')
    op.drop_table('travel_plans')
