"""add public_key to server table

Revision ID: 0e8f5bf0ef91
Revises: 29e012bee8f8
Create Date: 2026-02-06 15:26:38.961245

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e8f5bf0ef91"
down_revision: Union[str, Sequence[str], None] = "29e012bee8f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("servers", sa.Column("public_key", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("servers", "public_key")
