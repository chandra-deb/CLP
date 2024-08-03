"""add status attribute to every progress type

Revision ID: c5c280bca9b1
Revises: 0403aba375f7
Create Date: 2024-07-31 00:30:55.223175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5c280bca9b1'
down_revision = '0403aba375f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_meaning_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=64), nullable=False))
        batch_op.create_index(batch_op.f('ix_user_meaning_progress_status'), ['status'], unique=True)

    with op.batch_alter_table('user_pinyin_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=64), nullable=False))
        batch_op.create_index(batch_op.f('ix_user_pinyin_progress_status'), ['status'], unique=True)

    with op.batch_alter_table('user_recognition_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=64), nullable=False))
        batch_op.create_index(batch_op.f('ix_user_recognition_progress_status'), ['status'], unique=True)

    with op.batch_alter_table('user_writing_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=64), nullable=False))
        batch_op.create_index(batch_op.f('ix_user_writing_progress_status'), ['status'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_writing_progress', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_writing_progress_status'))
        batch_op.drop_column('status')

    with op.batch_alter_table('user_recognition_progress', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_recognition_progress_status'))
        batch_op.drop_column('status')

    with op.batch_alter_table('user_pinyin_progress', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_pinyin_progress_status'))
        batch_op.drop_column('status')

    with op.batch_alter_table('user_meaning_progress', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_meaning_progress_status'))
        batch_op.drop_column('status')

    # ### end Alembic commands ###
