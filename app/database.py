import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def get_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("Переменная окружения DATABASE_URL не задана.")
    return url


class Base(DeclarativeBase):
    pass


engine = None
SessionLocal = None


def init_engine():
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(get_database_url(), pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    init_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
