from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.TimeModel import TimeModel

class TimeQuery:
    def __init__(self):
        self.db_session = DatabaseSession.get_session()

    def find_all_times(self):
        return (
            self.db_session
                .query(TimeModel)
                .all()
        )