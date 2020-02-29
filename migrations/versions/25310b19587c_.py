"""empty message

Revision ID: 25310b19587c
Revises: 
Create Date: 2020-02-29 11:58:20.191251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25310b19587c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('test_type', sa.Enum('HACKATON', 'GAME', 'WORKSHOP', name='test_type'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'test_type')
    # ### end Alembic commands ###