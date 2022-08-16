"""add users

Revision ID: 54bfad871582
Revises: 177e5febe83c
Create Date: 2022-06-29 18:17:40.646904

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "54bfad871582"
down_revision = "177e5febe83c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("name", sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("comments", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "comments", "users", ["user_id"], ["id"])
    op.create_foreign_key(None, "comments", "posts", ["post_id"], ["id"])
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "posts", "users", ["user_id"], ["id"])


def downgrade():
    op.drop_constraint(None, "posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
    op.drop_constraint(None, "comments", type_="foreignkey")
    op.drop_constraint(None, "comments", type_="foreignkey")
    op.drop_column("comments", "user_id")
    op.drop_table("users")
