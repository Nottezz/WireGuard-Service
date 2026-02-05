from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from wireguard_service.config import settings
from wireguard_service.helpers import camel_case_to_snake_case

class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.database.naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
