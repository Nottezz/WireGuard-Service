"""create server table

Revision ID: 29e012bee8f8
Revises:
Create Date: 2026-02-05 16:47:06.979448

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "29e012bee8f8"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "servers",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuidv7()"), nullable=False),
        sa.Column("host", sa.String(), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("server_name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_servers")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("servers")
