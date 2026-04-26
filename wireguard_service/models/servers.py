import uuid

from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Server(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.uuidv7(),
    )
    host: Mapped[str] = mapped_column(nullable=False)
    port: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    server_name: Mapped[str] = mapped_column(String(100), nullable=False)
    public_key: Mapped[str] = mapped_column(nullable=True)
    key_filename: Mapped[str | None] = mapped_column(nullable=True)
    passphrase: Mapped[str | None] = mapped_column(nullable=True)
