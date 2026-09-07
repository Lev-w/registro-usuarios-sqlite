from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.config as config
from app.modules.db.models import Base

engine = None
SessionLocal = None


def _sqlite_url(database_url):
    if database_url:
        return database_url
    return getattr(config, "DATABASE_URL", None) or f"sqlite:///{config.DATABASE_NAME}"


def configure_engine(database_url=None):
    global engine, SessionLocal

    url = _sqlite_url(database_url)
    kwargs = {}

    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
        if ":memory:" in url:
            kwargs["poolclass"] = StaticPool

    engine = create_engine(url, **kwargs)

    if url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.close()

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return engine


def get_session():
    if SessionLocal is None:
        configure_engine()
    return SessionLocal()


def init_db(database_url=None):
    configure_engine(database_url)
    Base.metadata.create_all(bind=engine)


def reset_db():
    global engine, SessionLocal

    if engine is not None:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

    engine = None
    SessionLocal = None
