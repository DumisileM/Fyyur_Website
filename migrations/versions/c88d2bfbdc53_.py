"""empty message

Revision ID: c88d2bfbdc53
Revises: b7e8fb51ba44
Create Date: 2022-08-12 10:25:14.284042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c88d2bfbdc53'
down_revision = 'b7e8fb51ba44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'seeking_description',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'seeking_description',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    # ### end Alembic commands ###
