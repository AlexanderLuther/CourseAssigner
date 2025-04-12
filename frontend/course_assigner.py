import tkinter as tk
from tkinter import filedialog, messagebox

from backend.Exception.HellException import HellException
from backend.controller.course_file_controller import CourseFileController
from backend.controller.teacher_file_controller import TeacherFileController
from frontend.classroom.add_classroom_form import AddClassroomForm
from frontend.classroom.classroom_viewer import ClassroomViewer
from frontend.course.add_course_form import AddCourseForm
from frontend.course.course_viewer import CourseViewer
from frontend.log_viewer import LogViewer
from frontend.teacher.teacher_viewer import TeacherViewer
from frontend.teacher.add_teacher_form import AddTeacherForm

class CourseAssigner:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Asignador de Cursos")
        self.parent.geometry("700x600")
        self.file_course_controller = CourseFileController()
        self.file_teacher_controller = TeacherFileController()
        self.create_menu()
        self.parent.mainloop()

    def create_menu(self):
        menu_bar = tk.Menu(self.parent)
        self.parent.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Importar Docentes", command=self.import_teachers)
        file_menu.add_command(label="Importar Cursos", command=self.import_courses)
        file_menu.add_command(label="Importar Relacion Docente-Curso", command=lambda: self.nueva_ventana("Cursos"))
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        # Courses Menu
        courses_menu = tk.Menu(menu_bar, tearoff=0)
        courses_menu.add_command(label="Nuevo Curso", command=lambda: AddCourseForm(self.parent))
        courses_menu.add_command(label="Ver Cursos", command=lambda: CourseViewer(self.parent))
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

    def get_file_path(self):
        file = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv")],
            defaultextension=".csv"
        )
        if file:
            return file
        return None

    def import_courses(self):
        try:
            file_path = self.get_file_path()
            if file_path:
                has_errors = self.file_course_controller.read_course_file(file_path)
                if has_errors:
                    LogViewer(self.parent, 'importacion_cursos.txt')
                else:
                    messagebox.showinfo("Cursos importados correctamente", "Los cursos se han importado correctamente.")
        except HellException as e:
            messagebox.showerror("Error al importar cursos", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    def import_teachers(self):
        try:
            file_path = self.get_file_path()
            if file_path:
                has_errors = self.file_teacher_controller.read_teacher_file(file_path)
                if has_errors:
                    LogViewer(self.parent, 'importacion_docentes.txt')
                else:
                    messagebox.showinfo("Docentes importados correctamente", "Los docentes se han importado correctamente.")
        except HellException as e:
            messagebox.showerror("Error al importar docentes", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

