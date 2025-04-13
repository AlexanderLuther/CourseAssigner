from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.period_model import PeriodModel

class PeriodQuery:
    def find_all_periods(self):
        with DatabaseSession.get_session() as session:
            return session.query(PeriodModel).all()
