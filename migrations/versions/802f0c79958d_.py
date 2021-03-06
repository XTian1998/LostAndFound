"""empty message

Revision ID: 802f0c79958d
Revises: 3056e7f4a8b4
Create Date: 2021-01-17 19:59:37.821890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '802f0c79958d'
down_revision = '3056e7f4a8b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'item_info', 'item_type', ['type'], ['type'], ondelete='SET DEFAULT')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'item_info', type_='foreignkey')
    # ### end Alembic commands ###
