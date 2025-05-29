from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from app.core.config import settings
from typing import Generator


DATABASE_URL = settings.DATABASE_URL
print("Using DB URL:", DATABASE_URL)

engine = create_engine(str(settings.DATABASE_URL), echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
