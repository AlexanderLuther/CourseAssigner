import tkinter as tk
from tkinter import messagebox

from backend.Exception.HellException import HellException
from backend.controller.career_controller import CareerController
from backend.controller.course_controller import CourseController  # Asegúrate de tenerlo
from backend.controller.course_type_controller import CourseTypeController
from backend.controller.section_controller import SectionController
from backend.controller.semester_controller import SemesterController


class AddCourseForm:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Nuevo Curso")
        self.window.geometry("400x550")
        self.course_controller = CourseController()
        self.section_options = self.get_sections()
        self.career_options = self.get_careers()
        self.semester_options = self.get_semesters()
        self.course_type_options = self.get_course_types()
        self.create_form()
        self.error_label = tk.Label(self.window, text="", fg="red")
        self.error_label.pack()

    def get_sections(self):
        section_controller = SectionController()
        raw_sections = section_controller.get_all_sections()
        self.section_map = {}
        for section in raw_sections:
            self.section_map[section.description] = section.id
        return list(self.section_map.keys())

    def get_careers(self):
        career_controller = CareerController()
        raw_careers = career_controller.get_all_careers()
        self.career_map = {}
        for career in raw_careers:
            self.career_map[career.description] = career.id
        return list(self.career_map.keys())

    def get_semesters(self):
        semester_controller = SemesterController()
        raw_semesters = semester_controller.get_all_semesters()
        self.semester_map = {}
        for semester in raw_semesters:
            self.semester_map[semester.description] = semester.id
        return list(self.semester_map.keys())

    def get_course_types(self):
        course_type_controller = CourseTypeController()
        raw_types = course_type_controller.get_all_course_types()
        self.type_map = {}
        for type in raw_types:
            self.type_map[type.description] = type.id
        return list(self.type_map.keys())

    def validate_id(self, new_value):
        return new_value.isdigit() and len(new_value) <= 10 or new_value == ""

    def create_form(self):
        # Validate id method
        id_validator = (self.window.register(self.validate_id), "%P")

        # Course name
        tk.Label(self.window, text="Nombre del Curso").pack(pady=(10, 0))
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)

        # Course code
        tk.Label(self.window, text="Código del Curso").pack(pady=(10, 0))
        self.code_entry = tk.Entry(self.window, validate="key", validatecommand=id_validator)
        self.code_entry.pack(pady=5)

        # Career
        tk.Label(self.window, text="Carrera").pack(pady=(10, 0))
        self.career_var = tk.StringVar(value="")
        tk.OptionMenu(self.window, self.career_var, *self.career_options).pack(pady=5)

        # Semester
        tk.Label(self.window, text="Semestre").pack(pady=(10, 0))
        self.semester_var = tk.StringVar(value="")
        tk.OptionMenu(self.window, self.semester_var, *self.semester_options).pack(pady=5)

        # Section
        tk.Label(self.window, text="Seccion").pack(pady=(10, 0))
        self.section_var = tk.StringVar(value="")
        tk.OptionMenu(self.window, self.section_var, *self.section_options).pack(pady=5)

        # Course type
        tk.Label(self.window, text="Tipo de Curso").pack(pady=(10, 0))
        self.type_var = tk.StringVar(value="")
        tk.OptionMenu(self.window, self.type_var, *self.course_type_options).pack(pady=5)

        # Buttons
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=20)
        save_button = tk.Button(buttons_frame, text="Guardar", width=12, command=self.save_course)
        save_button.grid(row=0, column=0, padx=10)
        cancel_button = tk.Button(buttons_frame, text="Cancelar", width=12, command=self.window.destroy)
        cancel_button.grid(row=0, column=1, padx=10)

    def show_error(self, message):
        self.error_label.config(text=message)
        self.window.after(3000, lambda: self.error_label.config(text=""))

    def save_course(self):
        name = self.name_entry.get().strip()
        code = self.code_entry.get().strip()
        career = self.career_var.get()
        semester = self.semester_var.get()
        section = self.section_var.get()
        course_type = self.type_var.get()

        if not name:
            self.show_error("El nombre del curso es obligatorio")
            return
        if not code:
            self.show_error("El código del curso es obligatorio")
            return
        if not career:
            self.show_error("Debe seleccionar una carrera")
            return
        if not semester:
            self.show_error("Debe seleccionar un semestre")
            return
        if not section:
            self.show_error("Debe seleccionar una seccion")
            return
        if not course_type:
            self.show_error("Debe seleccionar un tipo de curso")
            return

        try:
            self.course_controller.save_course(
                code,
                name,
                self.career_map.get(career),
                self.semester_map.get(semester),
                self.section_map.get(section),
                self.type_map.get(course_type)
            )
            messagebox.showinfo("Éxito", f"Curso '{name}' guardado.")
            self.window.destroy()
        except HellException as e:
            self.show_error(str(e))