"""empty message

Revision ID: a024a2bb43b3
Revises: b18a0c2ca2e2
Create Date: 2020-07-15 18:06:57.944897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a024a2bb43b3'
down_revision = 'b18a0c2ca2e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imei', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('devices')
    # ### end Alembic commands ###
