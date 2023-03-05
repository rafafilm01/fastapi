"""add foregin key to post table

Revision ID: 1c0eaf849d06
Revises: 4813430c7995
Create Date: 2023-03-02 10:23:05.615934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c0eaf849d06'
down_revision = '4813430c7995'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.add_column('posts' , sa.Column('owner_id', sa.Integer(), nullable=False ))
    #create a foreign key relation 
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
