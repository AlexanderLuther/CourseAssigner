import os
import pandas as pd
from backend.Exception.HellException import HellException
from backend.controller.teacher_controller import TeacherController
from backend.controller.course_controller import CourseController

LOG_FILE = 'importacion_docente_curso.txt'

def write_log(message: str):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

class TeacherCourseFileController:

    def __init__(self):
        self.teacher_controller = TeacherController()
        self.course_controller = CourseController()
        self.assignments = {}

    def read_teacher_course_file(self, path):
        self.assignments = {}
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

        try:
            data = pd.read_csv(
                path,
                delimiter=',',
                encoding='utf-8',
                header=None,
                names=["teacher_id", "course_code"]
            )

            if data.empty:
                raise HellException("El archivo está vacío o no se pudo interpretar correctamente.")

            teachers = {str(t.id): t for t in self.teacher_controller.find_all_teachers()}
            courses = {str(c.code): c for c in self.course_controller.find_all_courses()}

            for index, row in data.iterrows():
                self.validate_assignment(row.to_dict(), index + 1, teachers, courses)

            return os.path.exists(LOG_FILE)

        except pd.errors.EmptyDataError:
            raise HellException("El archivo está vacío.")
        except FileNotFoundError:
            raise HellException("El archivo no fue encontrado.")
        except pd.errors.ParserError:
            raise HellException("El archivo tiene un formato incorrecto.")
        except Exception as e:
            raise HellException(f"Ocurrió un error inesperado: {str(e)}")

    def validate_assignment(self, assignment: dict, line: int, teachers: dict, courses: dict):
        teacher_id = str(assignment["teacher_id"]).strip()
        course_code = str(assignment["course_code"]).strip()
        if not self.is_assignment_complete(assignment):
            write_log(f"DESCARTADO | Línea: {line} | Assignacion incomplet: {assignment}")
            return

        if len(teacher_id) > 10:
            write_log(f"DESCARTADO | Línea: {line} | ID de docente demasiado largo: {assignment}")
            return

        if len(course_code) > 10:
            write_log(f"DESCARTADO | Línea: {line} | Código de curso demasiado largo: {assignment}")
            return

        teacher = teachers.get(teacher_id)
        course = courses.get(course_code)

        if not teacher:
            write_log(f"DESCARTADO | Línea: {line} | Docente no encontrado: {assignment}")
            return

        if not course:
            write_log(f"DESCARTADO | Línea: {line} | Curso no encontrado: {assignment}")
            return

        if teacher_id not in self.assignments:
            self.assignments[teacher_id] = {
                "teacher": teacher,
                "courses": []
            }

        self.assignments[teacher_id]["courses"].append(course)

    def is_assignment_complete(self, assignment: dict):
        for value in assignment.values():
            if pd.isna(value) or str(value).strip() == "":
                return False
        return True

    def get_assignments(self):
        return self.assignments
