"""Add last_seen in users table

Revision ID: fbba0a93bd15
Revises: b978fc03f2fc
Create Date: 2024-05-07 19:16:29.895344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbba0a93bd15'
down_revision = 'b978fc03f2fc'
branch_labels = None
depends_on = None
from datetime import datetime, timezone

def upgrade():
    # Check if the temporary table exists and drop it if it does
    op.execute('DROP TABLE IF EXISTS _alembic_tmp_likes')
    # Add default datetime to existing rows
    op.execute(
        "UPDATE likes SET created_at = '{}' WHERE created_at IS NULL".format(datetime.now(timezone.utc))
        
    )

    # Commands to upgrade the database
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.alter_column('created_at',
                              existing_type=sa.DATETIME(),
                              nullable=False,
                              server_default=sa.text('CURRENT_TIMESTAMP'))

    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.alter_column('username',
                              existing_type=sa.VARCHAR(length=100),
                              nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))


def downgrade():
    # Commands to downgrade the database
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_seen')

    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.alter_column('username',
                              existing_type=sa.VARCHAR(length=100),
                              nullable=False)

    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.alter_column('created_at',
                              existing_type=sa.DATETIME(),
                              nullable=True,
                              server_default=None)
