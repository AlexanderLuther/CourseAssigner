from backend.db.connection.database_connection import DatabaseSession
from backend.db.model.section_model import SectionModel

class SectionQuery:
    def __init__(self):
        self.db_session = DatabaseSession.get_session()

    def find_all_sections(self):
        return (
            self.db_session
                .query(SectionModel)
                .all()
        )