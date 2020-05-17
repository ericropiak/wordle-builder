"""adding tables needed for ctconomy

Revision ID: b3ec0752cee9
Revises: a3c9ef98c3b0
Create Date: 2020-04-26 19:45:46.809702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3ec0752cee9'
down_revision = 'a3c9ef98c3b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('currency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('regulator_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['regulator_id'], ['banker.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('banker_currency',
    sa.Column('banker_id', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['banker_id'], ['banker.id'], ),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.PrimaryKeyConstraint('banker_id', 'currency_id')
    )
    op.create_table('currency_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('currency_history')
    op.drop_table('banker_currency')
    op.drop_table('currency')
    op.drop_table('banker')
    # ### end Alembic commands ###
