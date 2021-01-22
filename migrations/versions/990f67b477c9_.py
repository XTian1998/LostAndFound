"""empty message

Revision ID: 990f67b477c9
Revises: e4258b56301f
Create Date: 2021-01-20 14:09:34.774510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '990f67b477c9'
down_revision = 'e4258b56301f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('sendId', sa.String(length=16), nullable=True),
    sa.Column('receiveId', sa.String(length=16), nullable=True),
    sa.Column('content', sa.String(length=1024), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('item_info_ibfk_3', 'item_info', type_='foreignkey')
    op.create_foreign_key(None, 'item_info', 'item_type', ['type'], ['type'], ondelete='SET DEFAULT')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'item_info', type_='foreignkey')
    op.create_foreign_key('item_info_ibfk_3', 'item_info', 'item_type', ['type'], ['type'])
    op.drop_table('message')
    # ### end Alembic commands ###
