from backend.db.query.section_query import SectionQuery

class SectionController:
    def __init__(self):
        self.section_query = SectionQuery()

    def get_all_sections(self):
        return self.section_query.find_all_sections()