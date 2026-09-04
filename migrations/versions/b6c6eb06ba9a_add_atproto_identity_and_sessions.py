"""Add AT Protocol identity and OAuth session tables

Revision ID: b6c6eb06ba9a
Revises: 47c18d3434d2
Create Date: 2026-09-03 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6c6eb06ba9a'
down_revision: Union[str, None] = '47c18d3434d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # AT Protocol-only accounts have no local password and may not share an
    # email with us.
    op.alter_column('users', 'hashed_password', existing_type=sa.String(), nullable=True)
    op.alter_column('users', 'email', existing_type=sa.String(), nullable=True)

    op.add_column('users', sa.Column('did', sa.String(), nullable=True))
    op.add_column('users', sa.Column('pds_url', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_did'), 'users', ['did'], unique=True)

    op.create_table(
        'atproto_sessions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('did', sa.String(), nullable=False, index=True),
        sa.Column('pds_url', sa.String(), nullable=False),
        sa.Column('authorization_server', sa.String(), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=False),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('access_token_expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('dpop_private_key_pem', sa.Text(), nullable=False),
        sa.Column('dpop_authserver_nonce', sa.String(), nullable=True),
        sa.Column('dpop_pds_nonce', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'atproto_oauth_requests',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('state', sa.String(), nullable=False, unique=True),
        sa.Column('handle', sa.String(), nullable=False),
        sa.Column('did', sa.String(), nullable=True),
        sa.Column('pds_url', sa.String(), nullable=False),
        sa.Column('authorization_server', sa.String(), nullable=False),
        sa.Column('pkce_code_verifier', sa.String(), nullable=False),
        sa.Column('dpop_private_key_pem', sa.Text(), nullable=False),
        sa.Column('dpop_authserver_nonce', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_atproto_oauth_requests_state'), 'atproto_oauth_requests', ['state'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_atproto_oauth_requests_state'), table_name='atproto_oauth_requests')
    op.drop_table('atproto_oauth_requests')
    op.drop_table('atproto_sessions')
    op.drop_index(op.f('ix_users_did'), table_name='users')
    op.drop_column('users', 'pds_url')
    op.drop_column('users', 'did')
    op.alter_column('users', 'email', existing_type=sa.String(), nullable=False)
    op.alter_column('users', 'hashed_password', existing_type=sa.String(), nullable=False)
