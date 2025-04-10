import tkinter as tk
from tkinter import ttk
from backend.controller.career_controller import CareerController
from backend.controller.course_controller import CourseController
from backend.controller.course_type_controller import CourseTypeController
from backend.controller.section_controller import SectionController
from backend.controller.semester_controller import SemesterController

class CourseViewer:
    def __init__(self, parent):
        self.course_controller = CourseController()
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Listado de Cursos")
        self.window.geometry("700x500")
        self.course_controller = CourseController()
        self.section_options = self.get_sections()
        self.career_options = self.get_careers()
        self.semester_options = self.get_semesters()
        self.course_type_options = self.get_course_types()
        self.tree = None
        self.courses = []
        self.message_label = None
        self.init_table()
        self.add_action_buttons()

    def get_sections(self):
        section_controller = SectionController()
        raw_sections = section_controller.get_all_sections()
        self.section_map = {}
        self.section_map_inverted = {}
        for section in raw_sections:
            self.section_map[section.description] = section.id
            self.section_map_inverted[section.id] = section.description
        return list(self.section_map.keys())

    def get_careers(self):
        career_controller = CareerController()
        raw_careers = career_controller.get_all_careers()
        self.career_map = {}
        self.career_map_inverted = {}
        for career in raw_careers:
            self.career_map[career.description] = career.id
            self.career_map_inverted[career.id] = career.description
        return list(self.career_map.keys())

    def get_semesters(self):
        semester_controller = SemesterController()
        raw_semesters = semester_controller.get_all_semesters()
        self.semester_map = {}
        self.semester_map_inverted = {}
        for semester in raw_semesters:
            self.semester_map[semester.description] = semester.id
            self.semester_map_inverted[semester.id] = semester.description
        return list(self.semester_map.keys())

    def get_course_types(self):
        course_type_controller = CourseTypeController()
        raw_types = course_type_controller.get_all_course_types()
        self.type_map = {}
        self.type_map_inverted = {}
        for type in raw_types:
            self.type_map[type.description] = type.id
            self.type_map_inverted[type.id] = type.description
        return list(self.type_map.keys())

    def init_table(self):
        self.courses = self.course_controller.find_all_courses()
        if not self.courses:
            self.show_temporal_message("No hay cursos registrados.", color="red")
            return

        self.tree = ttk.Treeview(
            self.window,
            columns=("code", "name", "career", "semester", "section", "type"),
            show="headings",
            height=12
        )
        self.tree.heading("code", text="Código")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("career", text="Carrera")
        self.tree.heading("semester", text="Semestre")
        self.tree.heading("section", text="Sección")
        self.tree.heading("type", text="Tipo")

        self.tree.column("code", width=80, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("career", width=120, anchor="w")
        self.tree.column("semester", width=80, anchor="center")
        self.tree.column("section", width=80, anchor="center")
        self.tree.column("type", width=120, anchor="w")

        self.tree.pack(pady=20, fill="both", expand=True)
        self._load_courses_into_tree()

    def _load_courses_into_tree(self):
        for course in self.courses:
            self.tree.insert(
                "", "end",
                values=(
                    course.code,
                    course.name,
                    self.career_map_inverted.get(course.id_career),
                    self.semester_map_inverted.get(course.id_semester),
                    self.section_map_inverted.get(course.id_section),
                    self.type_map_inverted.get(course.id_course_type)
                )
            )

    def add_action_buttons(self):
        frame = tk.Frame(self.window)
        frame.pack(pady=10)
        edit_button = tk.Button(frame, text="Editar", width=12, command=self.edit_action)
        edit_button.grid(row=0, column=0, padx=10)
        delete_button = tk.Button(frame, text="Borrar", width=12, command=self.delete_action)
        delete_button.grid(row=0, column=1, padx=10)

    def get_selected_course(self):
        if not self.tree:
            return None
        selection = self.tree.selection()
        if not selection:
            return None
        item = self.tree.item(selection)
        code = item["values"][0]
        for course in self.courses:
            if course.code == str(code):
                return course
        return None

    def delete_action(self):
        course = self.get_selected_course()
        if not course:
            return
        self.course_controller.delete_course(course.code)
        self.refresh_table()
        self.show_temporal_message(f"Curso '{course.name}' eliminado.", color="green")

    def edit_action(self):
        course = self.get_selected_course()
        if not course:
            return
        self.open_edit_form(course)

    def open_edit_form(self, course):
        edit_window = tk.Toplevel(self.window)
        edit_window.title(f"Editar Curso: {course.code}")
        edit_window.geometry("400x400")

        # Name
        tk.Label(edit_window, text="Nombre del curso").pack()
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, course.name)
        name_entry.pack()

        # Careers
        tk.Label(edit_window, text="Carrera").pack()
        career_var = tk.StringVar()
        career_combo = ttk.Combobox(edit_window, textvariable=career_var, values=self.career_options, state="readonly")
        career_combo.set(self.career_map_inverted[course.id_career])
        career_combo.pack()

        # Semesters
        tk.Label(edit_window, text="Semestre").pack()
        semester_var = tk.StringVar()
        semester_combo = ttk.Combobox(edit_window, textvariable=semester_var, values=self.semester_options,
                                      state="readonly")
        semester_combo.set(self.semester_map_inverted[course.id_semester])
        semester_combo.pack()

        # Sections
        tk.Label(edit_window, text="Sección").pack()
        section_var = tk.StringVar()
        section_combo = ttk.Combobox(edit_window, textvariable=section_var, values=self.section_options,
                                     state="readonly")
        section_combo.set(self.section_map_inverted[course.id_section])
        section_combo.pack()

        # Course Types
        tk.Label(edit_window, text="Tipo de curso").pack()
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(edit_window, textvariable=type_var, values=self.course_type_options, state="readonly")
        type_combo.set(self.type_map_inverted[course.id_course_type])
        type_combo.pack()

        # Error label
        error_label = tk.Label(edit_window, text="", fg="red")
        error_label.pack(pady=5)

        def show_local_error(message, duration=3000):
            error_label.config(text=message)
            edit_window.after(duration, lambda: error_label.config(text=""))

        def update_course():
            name = name_entry.get().strip()
            career = career_var.get()
            semester = semester_var.get()
            section = section_var.get()
            course_type = type_var.get()

            if not name:
                show_local_error("El nombre del curso es obligatorio")
                return
            if not career:
                show_local_error("Debe seleccionar una carrera")
                return
            if not semester:
                show_local_error("Debe seleccionar un semestre")
                return
            if not section:
                show_local_error("Debe seleccionar una sección")
                return
            if not course_type:
                show_local_error("Debe seleccionar un tipo de curso")
                return
            if (
                    name == course.name
                    and career == self.career_map_inverted[course.id_career]
                    and semester == self.semester_map_inverted[course.id_semester]
                    and section == self.section_map_inverted[course.id_section]
                    and course_type == self.type_map_inverted[course.id_course_type]
            ):
                self.show_temporal_message(f"Curso '{course.code}' actualizado.", color="green")
                edit_window.destroy()
                return

            self.course_controller.update_course(
                course.code,
                name,
                self.career_map[career],
                self.semester_map[semester],
                self.section_map[section],
                self.type_map[course_type]
            )
            self.refresh_table()
            self.show_temporal_message(f"Curso '{course.code}' actualizado.", color="green")
            edit_window.destroy()

        # Buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Guardar Cambios", command=update_course).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancelar", command=edit_window.destroy).pack(side="left", padx=5)

    def refresh_table(self):
        if not self.tree:
            return
        self.tree.delete(*self.tree.get_children())
        self.courses = self.course_controller.find_all_courses()
        if not self.courses:
            self.tree.pack_forget()
            self.show_temporal_message("No hay cursos registrados.", color="red")
            return
        self.tree.pack(pady=20, fill="both", expand=True)
        self._load_courses_into_tree()

    def show_temporal_message(self, texto, color="black"):
        if self.message_label and self.message_label.winfo_exists():
            self.message_label.destroy()
        self.message_label = tk.Label(self.window, text=texto, fg=color, font=("Arial", 10))
        self.message_label.pack(pady=5)
        self.window.after(3000, lambda: self.message_label.destroy())
