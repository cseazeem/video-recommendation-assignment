from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=64), nullable=False, unique=True),
        sa.Column('display_name', sa.String(length=128), nullable=False, server_default=""),
        sa.Column('mood', sa.String(length=32), nullable=False, server_default="general"),
        sa.Column('profile', sa.JSON(), nullable=False, server_default=sa.text("'{}'"))
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)

    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('slug', sa.String(length=128), nullable=False, unique=True),
        sa.Column('title', sa.String(length=512), nullable=False, server_default=""),
        sa.Column('project_code', sa.String(length=64), nullable=False, server_default=""),
        sa.Column('category_name', sa.String(length=128), nullable=False, server_default=""),
        sa.Column('topic_name', sa.String(length=128), nullable=False, server_default=""),
        sa.Column('tags', sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column('is_available_in_public_feed', sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column('is_locked', sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column('stats', sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column('media', sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column('owner', sa.JSON(), nullable=False, server_default=sa.text("'{}'"))
    )
    op.create_index('ix_posts_slug', 'posts', ['slug'], unique=True)

    op.create_table(
        'interactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=16), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=False, server_default="1"),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('ix_interactions_username', 'interactions', ['username'])

def downgrade() -> None:
    op.drop_index('ix_interactions_username', table_name='interactions')
    op.drop_table('interactions')
    op.drop_index('ix_posts_slug', table_name='posts')
    op.drop_table('posts')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
