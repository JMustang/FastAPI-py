"""add foreign-key to posts table

Revision ID: 9f906814ec34
Revises: 84e78d4d7ec4
Create Date: 2022-12-03 19:27:38.105718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f906814ec34'
down_revision = '84e78d4d7ec4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'owner_id', sa.Integer(), nullable=False)),
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE'),
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
