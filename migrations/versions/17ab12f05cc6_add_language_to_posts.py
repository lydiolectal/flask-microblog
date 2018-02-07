"""add language to posts

Revision ID: 17ab12f05cc6
Revises: 1dd7b4879f61
Create Date: 2018-02-05 16:59:09.346540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17ab12f05cc6'
down_revision = '1dd7b4879f61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###