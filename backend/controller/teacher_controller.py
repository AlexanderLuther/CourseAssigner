from backend.Exception.HellException import HellException
from backend.db.model.teacher_model import TeacherModel
from backend.db.query.TeacherQuery import TeacherQuery

class TeacherController:
    def __init__(self):
        self.teacher_query = TeacherQuery()

    def save_teacher(self, id, name, entry_time, departure_time):
        temp_teacher = self.teacher_query.find_teacher_by_id(id)
        if temp_teacher:
            raise HellException(f"El Docente con registro {id} ya se encuentra registrado.")
        self.teacher_query.save_teacher(
            TeacherModel(
                id=id,
                name=name,
                entry_time=entry_time,
                departure_time=departure_time
            )
        )

    def find_teacher_by_id(self, id: str):
        return self.teacher_query.find_teacher_by_id(id)

    def update_teacher(self, id, name, entry_time, departure_time):
        self.teacher_query.update_teacher(
            TeacherModel(
                id=id,
                name=name,
                entry_time=entry_time,
                departure_time=departure_time
            )
        )

    def find_all_teachers(self):
        return self.teacher_query.find_all_teachers()

    def delete_teacher(self, id: str):
        self.teacher_query.delete_teacher(id)