import os
import unicodedata
import pandas as pd
from backend.controller.course_type_controller import CourseTypeController
from backend.controller.section_controller import SectionController
from backend.controller.career_controller import CareerController
from backend.controller.course_controller import CourseController
from backend.Exception.HellException import HellException

LOG_FILE = 'importacion_cursos.txt'

def write_log(message: str):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

class CourseFileController:

    def __init__(self):
        self.course_controller = CourseController()

    def read_course_file(self, path):
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

        try:
            courses = pd.read_csv(
                path,
                delimiter=',',
                encoding='utf-8',
                header=None,
                names=["name", "code", "career", "semester", "section", "type"]
            )
            if courses.empty:
                raise HellException("El archivo está vacío o no se pudo interpretar correctamente.")

            self.get_sections()
            self.get_careers()
            self.get_course_types()

            for index, row in courses.iterrows():
                self.create_course(row.to_dict(), index + 1)

            return os.path.exists(LOG_FILE)
        except pd.errors.EmptyDataError:
            raise HellException("El archivo está vacío.")
        except FileNotFoundError:
            raise HellException("El archivo no fue encontrado.")
        except pd.errors.ParserError:
            raise HellException("El archivo tiene un formato incorrecto.")
        except Exception as e:
            raise HellException(f"Ocurrió un error inesperado: {str(e)}")

    def get_sections(self):
        section_controller = SectionController()
        raw_sections = section_controller.get_all_sections()
        self.section_map = {section.description: section.id for section in raw_sections}

    def get_careers(self):
        career_controller = CareerController()
        raw_careers = career_controller.get_all_careers()
        self.career_map = {career.description: career.id for career in raw_careers}
        return list(self.career_map.keys())

    def get_course_types(self):
        course_type_controller = CourseTypeController()
        raw_types = course_type_controller.get_all_course_types()
        self.type_map = {type.description: type.id for type in raw_types}
        return list(self.type_map.keys())

    def create_course(self, course, line: int):
        if not self.is_course_complete(course):
            write_log(f"DESCARTADO | Línea: {line} | Curso incompleto: {course}")
            return
        if not self.is_valid_course_type(course["type"]):
            write_log(f"DESCARTADO | Línea: {line} | Tipo de curso incorrecto: {course}")
            return
        if not self.is_valid_semester(course["semester"]):
            write_log(f"DESCARTADO | Línea: {line} | Semestre incorrecto: {course}")
            return
        if not self.is_valid_section(course["section"]):
            write_log(f"DESCARTADO | Línea: {line} | Sección incorrecta: {course}")
            return
        if not self.is_valid_code(str(course["code"])):
            write_log(f"DESCARTADO | Línea: {line} | Código incorrecto: {course}")
            return
        if self.code_is_already_registered(course["code"]):
            write_log(f"DESCARTADO | Línea: {line} | Código ya registrado: {course}")
            return
        if not self.is_valid_career(course["career"]):
            write_log(f"DESCARTADO | Línea: {line} | Carrera incorrecta: {course}")
            return

        id_section = self.section_map.get(course["section"].upper().strip())
        if not id_section:
            write_log(f"DESCARTADO | Línea: {line} | No se obtuvo ID de sección: {course}")
            return

        id_type = self.type_map.get(course["type"].strip().capitalize())
        if not id_type:
            write_log(f"DESCARTADO | Línea: {line} | No se obtuvo ID del tipo de curso: {course}")
            return

        id_career = self.career_map.get(course["career"].strip().title())
        if not id_career:
            write_log(f"DESCARTADO | Línea: {line} | No se obtuvo ID de la carrera: {course}")
            return

        self.course_controller.save_course(
            course["code"],
            course["name"],
            id_career,
            course["semester"],
            id_section,
            id_type
        )

    def is_course_complete(self, course: dict):
        for value in course.values():
            if value is None:
                return False
            if isinstance(value, float) and pd.isna(value):
                return False
            if isinstance(value, str) and value.strip() == "":
                return False
        return True

    def is_valid_course_type(self, type: str):
        return type.strip().lower() in ["obligatorio", "optativo"]

    def is_valid_semester(self, semester: int):
        return 1 <= semester <= 10

    def is_valid_section(self, section: str):
        if not isinstance(section, str) or len(section.strip()) != 1:
            return False
        section = section.strip().upper()
        return 'A' <= section <= 'L'

    def is_valid_code(self, code: str):
        return isinstance(code, str) and len(code.strip()) <= 10

    def code_is_already_registered(self, code: str):
        course = self.course_controller.find_course_by_code(code)
        return bool(course)

    def is_valid_career(self, career: str):
        normalized_career = unicodedata.normalize('NFD', career)
        normalized_career = ''.join(
            c for c in normalized_career if unicodedata.category(c) != 'Mn'
        )
        return normalized_career.strip().lower() in [
            "industrial",
            "mecanica",
            "civil",
            "mecanica industrial",
            "sistemas"
        ]
