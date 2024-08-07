"""Add timestamps to CaptureEntry model

Revision ID: b9d32c0a835d
Revises: 4c976d2c62d2
Create Date: 2024-07-21 20:10:06.751794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9d32c0a835d'
down_revision = '4c976d2c62d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('capture_entries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('handled', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('organized', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('processed_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('capture_entries', schema=None) as batch_op:
        batch_op.drop_column('processed_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('organized')
        batch_op.drop_column('handled')

    # ### end Alembic commands ###
