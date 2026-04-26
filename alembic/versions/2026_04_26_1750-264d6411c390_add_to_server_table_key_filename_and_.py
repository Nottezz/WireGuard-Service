"""add to server table key_filename and passphrase columns

Revision ID: 264d6411c390
Revises: 0e8f5bf0ef91
Create Date: 2026-04-26 17:50:01.081063

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "264d6411c390"
down_revision: Union[str, Sequence[str], None] = "0e8f5bf0ef91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("servers", sa.Column("key_filename", sa.String(), nullable=True))
    op.add_column("servers", sa.Column("passphrase", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("servers", "passphrase")
    op.drop_column("servers", "key_filename")
