from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4c976d2c62d2'
down_revision = 'e9df5b695ced'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('project_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_task_project', 'project', ['project_id'], ['id'])

def downgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_constraint('fk_task_project', type_='foreignkey')
        batch_op.drop_column('project_id')
