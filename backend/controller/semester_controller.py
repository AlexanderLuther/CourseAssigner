from backend.db.query.semester_query import SemesterQuery

class SemesterController:
    def __init__(self):
        self.semester_query = SemesterQuery()

    def get_all_semesters(self):
        return self.semester_query.find_all_semesters()
