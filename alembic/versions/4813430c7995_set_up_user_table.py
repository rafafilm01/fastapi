"""set up user table

Revision ID: 4813430c7995
Revises: bfc794cddc4d
Create Date: 2023-02-27 12:39:48.097687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4813430c7995'
down_revision = 'bfc794cddc4d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')
    pass
