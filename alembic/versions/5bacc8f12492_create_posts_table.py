"""create posts table

Revision ID: 5bacc8f12492
Revises: 
Create Date: 2022-11-26 15:04:03.617297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bacc8f12492'
down_revision = None
branch_labels = None
depends_on = None


# Equivalente as magrations no nestjs

def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
