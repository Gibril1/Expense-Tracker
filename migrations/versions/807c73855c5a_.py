"""empty message

Revision ID: 807c73855c5a
Revises: 
Create Date: 2022-12-22 20:34:08.112405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '807c73855c5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('savings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.Date(), nullable=False))
        batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('savings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DATE(), nullable=False))
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###
