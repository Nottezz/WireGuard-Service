from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from wireguard_service.config import settings

engine = create_engine(
    settings.database.database_url,
    echo=settings.database.echo,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    with SessionLocal() as session:
        yield session
