"""empty message

Revision ID: 3227ab508a21
Revises: b50687863e9a
Create Date: 2020-07-18 15:27:50.035725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3227ab508a21'
down_revision = 'b50687863e9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_role_user',
    sa.Column('cmsrole_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cmsrole_id'], ['cmsrole.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('cmsrole_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_role_user')
    # ### end Alembic commands ###
