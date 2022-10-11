"""empty message

Revision ID: c51950e313fa
Revises: cf3362bda81d
Create Date: 2022-08-12 12:08:58.017543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c51950e313fa'
down_revision = 'cf3362bda81d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###