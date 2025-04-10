from backend.Exception.HellException import HellException
from backend.db.model.course_model import CourseModel
from backend.db.query.course_query import CourseQuery

class CourseController:

    def __init__(self):
        self.course_query = CourseQuery()

    def save_course(self, code, name, id_career, id_semester, id_section, id_course_type):
        temp_course = self.course_query.find_course_by_code(code)
        if temp_course:
            raise HellException(f"El curso con codigo {code} ya se encuentra registrado.")
        self.course_query.save_course(
            CourseModel(
                code=code,
                name=name,
                id_career=id_career,
                id_semester=id_semester,
                id_section=id_section,
                id_course_type=id_course_type
            )
        )

    def find_all_courses(self):
        return self.course_query.find_all_courses()

    def update_course(self, code, name, id_career, id_semester, id_section, id_course_type):
        self.course_query.update_course(
            CourseModel(
                code=code,
                name=name,
                id_career=id_career,
                id_semester=id_semester,
                id_section=id_section,
                id_course_type=id_course_type
            )
        )

    def delete_course(self, code: str):
        self.course_query.delete_course(code)