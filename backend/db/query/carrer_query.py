from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.career_model import CareerModel

class CareerQuery:
    def find_all_careers(self):
        with DatabaseSession.get_session() as session:
            return session.query(CareerModel).all()
