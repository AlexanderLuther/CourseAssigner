import os
from datetime import datetime

import pandas as pd
from backend.Exception.HellException import HellException
from backend.controller.teacher_controller import TeacherController
import re

from backend.controller.time_controller import TimeController

LOG_FILE = 'importacion_docentes.txt'

def write_log(message: str):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

class TeacherFileController:

    def __init__(self):
        self.teacher_controller = TeacherController()

    def read_teacher_file(self, path):
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

        try:
            teachers = pd.read_csv(
                path,
                delimiter=',',
                encoding='utf-8',
                header=None,
                names=["id", "name", "entry_time", "departure_time"]
            )
            if teachers.empty:
                raise HellException("El archivo está vacío o no se pudo interpretar correctamente.")

            self.get_available_times()
            for index, row in teachers.iterrows():
                self.create_teacher(row.to_dict(), index + 1)

            return os.path.exists(LOG_FILE)

        except pd.errors.EmptyDataError:
            raise HellException("El archivo está vacío.")
        except FileNotFoundError:
            raise HellException("El archivo no fue encontrado.")
        except pd.errors.ParserError:
            raise HellException("El archivo tiene un formato incorrecto.")
        except Exception as e:
            raise HellException(f"Ocurrió un error inesperado: {str(e)}")

    def get_available_times(self):
        time_controller = TimeController()
        raw_times = time_controller.get_all_times()
        self.time_map = {}
        for time in raw_times:
            time_str = datetime.strptime(str(time.time), "%H:%M:%S").strftime("%H:%M")
            self.time_map[time_str] = time.id
        return list(self.time_map.keys())

    def create_teacher(self, teacher, line: int):
        if not self.is_teacher_complete(teacher):
            write_log(f"DESCARTADO | Línea: {line} | Docente incompleto: {teacher}")
            return
        if not self.is_valid_id(str(teacher["id"])):
            write_log(f"DESCARTADO | Línea: {line} | ID inválido: {teacher}")
            return
        if self.id_is_already_registered(teacher["id"]):
            write_log(f"DESCARTADO | Línea: {line} | ID ya registrado: {teacher}")
            return
        if not self.is_valid_time_format(teacher["entry_time"]):
            write_log(f"DESCARTADO | Línea: {line} | Formato de hora de entrada inválido: {teacher}")
            return
        if not self.is_valid_time_format(teacher["departure_time"]):
            write_log(f"DESCARTADO | Línea: {line} | Formato de hora de salida inválido: {teacher}")
            return
        if not self.is_valid_time(teacher["entry_time"]):
            write_log(f"DESCARTADO | Línea: {line} | Hora de entrada no valida: {teacher}")
            return
        if not self.is_valid_time(teacher["departure_time"]):
            write_log(f"DESCARTADO | Línea: {line} | Hora de salida no valida: {teacher}")
            return
        fmt = "%H:%M"
        if datetime.strptime(teacher["entry_time"], fmt) >= datetime.strptime(teacher["departure_time"], fmt):
            write_log(f"DESCARTADO | Línea: {line} | La hora de entrada debe ser menor que la hora de salida: {teacher}")
            return

        self.teacher_controller.save_teacher(
            teacher["id"],
            teacher["name"].strip(),
            teacher["entry_time"].strip(),
            teacher["departure_time"].strip()
        )

    def is_teacher_complete(self, teacher: dict):
        for value in teacher.values():
            if pd.isna(value) or str(value).strip() == "":
                return False
        return True

    def is_valid_id(self, code: str):
        return isinstance(code, str) and len(code.strip()) <= 10

    def id_is_already_registered(self, id):
        return bool(self.teacher_controller.find_teacher_by_id(id))

    def is_valid_time_format(self, time_str):
        return bool(re.match(r"^\d{2}:\d{2}$", str(time_str).strip()))

    def is_valid_time(self, time_str):
        return  bool(self.time_map.get(time_str.strip()))