"""add user table

Revision ID: 84e78d4d7ec4
Revises: 40ed9ee18ae6
Create Date: 2022-11-30 20:42:04.802180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84e78d4d7ec4'
down_revision = '40ed9ee18ae6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
