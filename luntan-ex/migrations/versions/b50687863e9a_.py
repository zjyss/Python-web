"""empty message

Revision ID: b50687863e9a
Revises: 8c590e917d22
Create Date: 2020-07-18 15:01:40.575884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b50687863e9a'
down_revision = '8c590e917d22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cmsrole',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('desc', sa.String(length=30), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cmsrole')
    # ### end Alembic commands ###
