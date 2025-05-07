import os
from contextlib import contextmanager

from sqlalchemy.pool import QueuePool
from sqlmodel import create_engine, Session

# Database connection configuration
DB_USER = os.getenv("DB_USER", "ngoqhuy")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1711")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "EduCenterDB")

# Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLModel engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
)


# Dependency to get DB session
def get_db():
    with Session(engine) as session:
        yield session


# Context manager for DB sessions (alternative approach)
@contextmanager
def db_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
