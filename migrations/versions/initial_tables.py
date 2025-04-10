"""initial tables

Revision ID: initial_tables
Create Date: 2023-09-20 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'initial_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create urls table
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('short_code', sa.String(), nullable=False),
        sa.Column('original_url', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('clicks', sa.Integer(), server_default='0'),
        sa.Column('is_custom', sa.Boolean(), server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('short_code')
    )
    op.create_index('idx_short_code', 'urls', ['short_code'])
    op.create_index('idx_expires_at', 'urls', ['expires_at'])

    # Create settings table
    op.create_table(
        'settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('setting_name', sa.String(), nullable=False),
        sa.Column('setting_value', sa.String(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('setting_name')
    )

    # Insert default settings
    op.execute(
        "INSERT INTO settings (setting_name, setting_value) VALUES "
        "('default_expiry_days', '30'), "
        "('short_code_length', '6'), "
        "('allow_custom_urls', 'true')"
    )

def downgrade() -> None:
    op.drop_table('settings')
    op.drop_index('idx_expires_at')
    op.drop_index('idx_short_code')
    op.drop_table('urls')