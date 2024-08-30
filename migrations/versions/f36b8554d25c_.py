"""empty message

Revision ID: f36b8554d25c
Revises: 
Create Date: 2024-08-28 17:47:27.236570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f36b8554d25c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chinese_character', schema=None) as batch_op:
        batch_op.drop_index('ix_chinese_character_character')
        batch_op.create_index(batch_op.f('ix_chinese_character_character'), ['character'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chinese_character', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_chinese_character_character'))
        batch_op.create_index('ix_chinese_character_character', ['character'], unique=1)

    # ### end Alembic commands ###
