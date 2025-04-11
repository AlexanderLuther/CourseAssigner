from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.section_model import SectionModel

class SectionQuery:
    def find_all_sections(self):
        with DatabaseSession.get_session() as session:
            return session.query(SectionModel).all()
