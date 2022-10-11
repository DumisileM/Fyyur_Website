"""empty message

Revision ID: 2819548b55db
Revises: 844320d9f740
Create Date: 2022-08-13 12:17:45.334058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2819548b55db'
down_revision = '844320d9f740'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'artists', ['phone'])
    op.create_unique_constraint(None, 'venues', ['website'])
    op.create_unique_constraint(None, 'venues', ['phone'])
    op.create_unique_constraint(None, 'venues', ['address'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'venues', type_='unique')
    op.drop_constraint(None, 'venues', type_='unique')
    op.drop_constraint(None, 'venues', type_='unique')
    op.drop_constraint(None, 'artists', type_='unique')
    # ### end Alembic commands ###