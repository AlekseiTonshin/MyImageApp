"""first migration

Revision ID: 9daf351eea4d
Revises: 
Create Date: 2020-08-24 11:15:06.312257

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '9daf351eea4d'
down_revision = '1975ea83b712'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'img_test',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('old_image', sa.LargeBinary())
        sa.Column('new_image', sa.LargeBinary())
    )


def downgrade():
    op.drop_table('img_test')
