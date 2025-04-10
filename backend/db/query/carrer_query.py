from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.career_model import CareerModel

class CareerQuery:
    def __init__(self):
        self.db_session = DatabaseSession.get_session()

    def find_all_careers(self):
        return (
            self.db_session
                .query(CareerModel)
                .all()
        )