"""
Database engine and session management for LandslideNER.
Configured for Supabase PostgreSQL + PostGIS using Supavisor Session Mode (Port 5432)
to support IPv4 connectivity and SQLAlchemy QueuePool / prepared statements.
"""

import os
from functools import lru_cache
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load backend/.env if present (never committed to Git)
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(_BACKEND_DIR, ".env"))


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Add your Supabase Supavisor Session Mode URI to backend/.env"
        )
    return url


@lru_cache(maxsize=1)
def get_engine():
    url = get_database_url()
    return create_engine(
        url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )


def get_session_local():
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> tuple[bool, str]:
    """Verify PostgreSQL connectivity and PostGIS availability without exposing credentials."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            postgis_ver = conn.execute(text("SELECT extensions.PostGIS_Version();")).scalar()
            return True, f"Connected (PostGIS {postgis_ver})"
    except Exception as exc:
        return False, f"Database unavailable: {type(exc).__name__}"
