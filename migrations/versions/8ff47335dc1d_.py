"""empty message

Revision ID: 8ff47335dc1d
Revises: 200fb3b4a38e
Create Date: 2020-08-02 07:48:51.027689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ff47335dc1d'
down_revision = '200fb3b4a38e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'devices', ['imei'])
    op.add_column('messages', sa.Column('device_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'messages', 'devices', ['device_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_column('messages', 'device_id')
    op.drop_constraint(None, 'devices', type_='unique')
    # ### end Alembic commands ###