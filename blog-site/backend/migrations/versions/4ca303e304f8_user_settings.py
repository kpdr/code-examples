"""user settings

Revision ID: 4ca303e304f8
Revises: 54bfad871582
Create Date: 2022-07-01 16:41:52.534369

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4ca303e304f8"
down_revision = "54bfad871582"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_settings",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_display", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )


def downgrade():
    op.drop_table("user_settings")
