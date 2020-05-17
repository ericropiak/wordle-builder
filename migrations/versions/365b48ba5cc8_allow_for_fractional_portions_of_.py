"""allow for fractional portions of currency

Revision ID: 365b48ba5cc8
Revises: 7e74338591c0
Create Date: 2020-04-26 20:16:05.776972

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '365b48ba5cc8'
down_revision = '7e74338591c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('banker_currency', sa.Column('amount', sa.Float(), nullable=False))
    op.drop_column('banker_currency', 'amount_temp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('banker_currency', sa.Column('amount_temp', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('banker_currency', 'amount')
    # ### end Alembic commands ###
