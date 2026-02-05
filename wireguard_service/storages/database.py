from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from wireguard_service.config import settings

engine = create_engine(
    settings.database.database_url_asyncpg,
    echo=settings.database.echo,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    with SessionLocal() as session:
        yield session
