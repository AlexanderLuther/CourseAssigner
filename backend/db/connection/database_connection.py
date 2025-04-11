from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseSession:
    _engine = None
    _session_factory = None

    @classmethod
    def initialize(cls, user, password, host, db_name):
        if cls._engine is None:
            DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
            cls._engine = create_engine(
                DATABASE_URL,
                echo=True,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30
            )
            cls._session_factory = sessionmaker(bind=cls._engine)

    @classmethod
    @contextmanager
    def get_session(cls):
        if cls._session_factory is None:
            raise Exception("DatabaseSession not initialized. Call initialize() first.")
        session = cls._session_factory()
        try:
            yield session
        finally:
            session.close()
