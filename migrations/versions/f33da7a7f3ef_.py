"""empty message

Revision ID: f33da7a7f3ef
Revises: eb032c5f759d
Create Date: 2020-07-07 10:24:54.911301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f33da7a7f3ef'
down_revision = 'eb032c5f759d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
