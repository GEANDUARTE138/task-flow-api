"""
This module provides a MySQLConnector class to manage MySQL database connections
using SQLAlchemy. It includes methods for creating and disposing of the engine, 
and managing session scope for transactions.
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from core.config import settings

class MySQLConnector:
    """
    A connector class for managing MySQL database connections and sessions
    using SQLAlchemy.
    """
    
    path = "mysql+pymysql://{}:{}@{}:{}/{}".format(
        settings.DB_USER,
        settings.DB_PASSWORD,
        settings.DB_HOST,
        settings.DB_PORT,
        settings.DB_NAME,
    )
    engine: Engine
    Session: scoped_session

    @classmethod
    def create_engine(cls):
        """
        Create the SQLAlchemy engine and session factory for the MySQL database.

        This method sets up the database engine and a scoped session factory,
        with a connection pool for managing multiple concurrent connections.
        """
        cls.engine = create_engine(
            cls.path,
            echo=False,
            pool_size=int(settings.DB_POOL_SIZE),
            max_overflow=int(settings.DB_MAX_OVERFLOW_SIZE),
            pool_recycle=int(settings.DB_POOL_RECYCLE_TIME),
            poolclass=QueuePool,
        )
        cls.Session = scoped_session(sessionmaker(bind=cls.engine))

    @classmethod
    def dispose_engine(cls):
        """
        Dispose of the current SQLAlchemy engine.

        This method closes the engine and releases all connections in the pool.
        """
        cls.engine.dispose()

    @classmethod
    @contextmanager
    def session_scope(cls):
        """
        Provide a transactional scope around a series of operations.

        This method creates a new database session, handles commit and rollback
        as necessary, and ensures the session is closed after use.
        """
        session = cls.Session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
