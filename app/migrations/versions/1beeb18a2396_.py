"""empty message

Revision ID: 1beeb18a2396
Revises: 5722c6d8d7c7
Create Date: 2023-04-13 17:19:27.724828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1beeb18a2396'
down_revision = '5722c6d8d7c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###