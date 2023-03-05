"""adding last set of columns

Revision ID: cf0a70abd172
Revises: 1c0eaf849d06
Create Date: 2023-03-02 10:34:46.206728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf0a70abd172'
down_revision = '1c0eaf849d06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    #add published and created_at to posts 
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE' ),) 
    op.add_column('posts', sa.Column ('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),)
    
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')
    pass
