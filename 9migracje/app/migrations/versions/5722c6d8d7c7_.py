"""empty message

Revision ID: 5722c6d8d7c7
Revises: 9de3857c0c3f
Create Date: 2023-04-12 18:25:04.092422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5722c6d8d7c7'
down_revision = '9de3857c0c3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###

