"""empty message

Revision ID: 869b2ebe4a84
Revises: 490333f35ed4
Create Date: 2022-08-12 15:24:30.055167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '869b2ebe4a84'
down_revision = '490333f35ed4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'website_link',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'website_link',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###