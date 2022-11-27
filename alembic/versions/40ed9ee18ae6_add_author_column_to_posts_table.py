"""add author column to posts table

Revision ID: 40ed9ee18ae6
Revises: 5bacc8f12492
Create Date: 2022-11-27 20:30:50.714262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40ed9ee18ae6'
down_revision = '5bacc8f12492'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('author', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'author')
    pass
