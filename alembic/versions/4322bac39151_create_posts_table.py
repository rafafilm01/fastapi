"""create posts table

Revision ID: 4322bac39151
Revises: 
Create Date: 2023-02-27 12:19:04.532996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4322bac39151'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title',    sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
