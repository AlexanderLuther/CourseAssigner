import tkinter as tk
from frontend.classroom.add_classroom_form import AddClassroomForm
from frontend.classroom.classroom_viewer import ClassroomViewer
from frontend.course.add_course_form import AddCourseForm
from frontend.teacher.TeacherViewer import TeacherViewer
from frontend.teacher.add_teacher_form import AddTeacherForm

class CourseAssigner:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Asignador de Cursos")
        self.parent.geometry("600x600")
        self.create_menu()
        self.parent.mainloop()

    def create_menu(self):
        menu_bar = tk.Menu(self.parent)
        self.parent.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Importar Docentes", command=lambda: self.nueva_ventana("Cursos"))
        file_menu.add_command(label="Importar Cursos", command=lambda: self.nueva_ventana("Cursos"))
        file_menu.add_command(label="Importar Relacion Docente-Curso", command=lambda: self.nueva_ventana("Cursos"))
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        # Courses Menu
        courses_menu = tk.Menu(menu_bar, tearoff=0)
        courses_menu.add_command(label="Nuevo Curso", command=lambda: AddCourseForm(self.parent))
        courses_menu.add_command(label="Ver Cursos", command=lambda: self.nueva_ventana("Cursos"))
        menu_bar.add_cascade(label="Cursos", menu=courses_menu)

        # Teacher Menu
        teacher_menu = tk.Menu(menu_bar, tearoff=0)
        teacher_menu.add_command(label="Nuevo Docente", command=lambda: AddTeacherForm(self.parent))
        teacher_menu.add_command(label="Ver Docentes", command=lambda: TeacherViewer(self.parent))
        menu_bar.add_cascade(label="Docentes", menu=teacher_menu)

        # Classroom Menu
        classroom_menu = tk.Menu(menu_bar, tearoff=0)
        classroom_menu.add_command(label="Nuevo Salon", command=lambda: AddClassroomForm(self.parent))
        classroom_menu.add_command(label="Ver Salones", command=lambda: ClassroomViewer(self.parent))
        menu_bar.add_cascade(label="Salones", menu=classroom_menu)