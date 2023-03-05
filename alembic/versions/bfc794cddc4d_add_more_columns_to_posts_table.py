"""add more columns to posts table

Revision ID: bfc794cddc4d
Revises: 4322bac39151
Create Date: 2023-02-27 12:32:09.184862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfc794cddc4d'
down_revision = '4322bac39151'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
