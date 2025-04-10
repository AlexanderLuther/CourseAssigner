from backend.Exception.HellException import HellException
from backend.db.model.classroom_model import ClassroomModel
from backend.db.query.classroom_query import ClassroomQuery

class ClassroomController:
    def __init__(self):
        self.classroom_query = ClassroomQuery()

    def save_classroom(self, description: str):
        classroom = self.classroom_query.find_classroom_by_description(description)
        if classroom:
            raise HellException(f"El salon {description} ya se encuentra registrado.")
        self.classroom_query.save_classroom(ClassroomModel(description=description))

    def update_classroom(self, id: int, description: str):
        classroom = self.classroom_query.find_classroom_by_description(description)
        if classroom and classroom.id != id:
            raise HellException(f"Ya existe un salon con la descripcion {description}.")
        self.classroom_query.update_classroom(ClassroomModel(id=id, description=description))

    def get_all_classrooms(self):
        return self.classroom_query.find_all_classrooms()

    def delete_classroom(self, id: int):
        self.classroom_query.delete_classroom(id)
