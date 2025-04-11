from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.time_model import TimeModel

class TimeQuery:
    def find_all_times(self):
        with DatabaseSession.get_session() as session:
            return session.query(TimeModel).all()
