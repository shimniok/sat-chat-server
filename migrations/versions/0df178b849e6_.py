"""empty message

Revision ID: 0df178b849e6
Revises: 5d3e181e80ac
Create Date: 2021-06-10 19:05:41.335218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0df178b849e6'
down_revision = '5d3e181e80ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    # ### end Alembic commands ###
