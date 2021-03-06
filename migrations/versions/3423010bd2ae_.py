"""empty message

Revision ID: 3423010bd2ae
Revises: 2ab08482a16f
Create Date: 2021-01-10 16:55:22.009667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3423010bd2ae'
down_revision = '2ab08482a16f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(length=16), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('phone', sa.String(length=16), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
