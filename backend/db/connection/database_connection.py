from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SessionType

class DatabaseSession:
    _engine = None
    _session_factory = None

    @classmethod
    def initialize(cls, user, password, host, db_name):
        if cls._engine is None:
            DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
            cls._engine = create_engine(DATABASE_URL, echo=True)
            cls._session_factory = sessionmaker(bind=cls._engine)

    @classmethod
    def get_session(cls) -> SessionType:
        if cls._session_factory is None:
            raise Exception("DatabaseSession not initialized. Call initialize() first.")
        return cls._session_factory()
