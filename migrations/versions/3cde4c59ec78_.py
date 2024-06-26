"""empty message

Revision ID: 3cde4c59ec78
Revises: 68801a8c35eb
Create Date: 2024-04-06 21:10:08.809195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cde4c59ec78'
down_revision = '68801a8c35eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###
