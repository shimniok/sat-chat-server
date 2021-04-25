"""empty message

Revision ID: 1609de0d4c1e
Revises: 8ff47335dc1d
Create Date: 2021-04-19 09:39:11.883640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1609de0d4c1e'
down_revision = '8ff47335dc1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try: 
        op.drop_table('conversations')
        op.drop_table('contacts')
        op.drop_table('roles')
    except psycopg2.errors.UndefinedTable:
        pass
    except Exception as e:
        print("Error dropping tables: "+e)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    sa.UniqueConstraint('name', name='roles_name_key')
    )
    op.create_table('contacts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('device_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='contacts_device_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='contacts_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='contacts_pkey')
    )
    op.create_table('conversations',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('device_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='conversations_device_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='conversations_user_id_fkey')
    )
    # ### end Alembic commands ###
