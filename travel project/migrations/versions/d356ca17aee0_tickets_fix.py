"""tickets fix

Revision ID: d356ca17aee0
Revises: 580947e11125
Create Date: 2020-05-26 16:25:43.140399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd356ca17aee0'
down_revision = '580947e11125'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticket', sa.Column('flight_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ticket', 'flight', ['flight_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ticket', type_='foreignkey')
    op.drop_column('ticket', 'flight_id')
    # ### end Alembic commands ###