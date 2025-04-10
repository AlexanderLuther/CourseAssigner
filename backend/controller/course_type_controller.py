from backend.db.query.course_type_query import CourseTypeQuery

class CourseTypeController:
    def __init__(self):
        self.course_type_query = CourseTypeQuery()

    def get_all_course_types(self):
        return self.course_type_query.find_all_course_types()
