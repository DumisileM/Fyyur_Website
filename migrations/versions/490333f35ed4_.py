"""empty message

Revision ID: 490333f35ed4
Revises: c51950e313fa
Create Date: 2022-08-12 15:23:45.893618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '490333f35ed4'
down_revision = 'c51950e313fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'website_link',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'website_link',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
