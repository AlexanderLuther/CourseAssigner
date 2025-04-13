import tkinter as tk
from tkinter import ttk
from backend.controller.course_controller import CourseController
from backend.controller.genetic_algorithm_controller import GeneticAlgorithmController
from backend.controller.period_controller import PeriodController
from backend.controller.teacher_controller import TeacherController
from backend.controller.career_controller import CareerController
from backend.controller.course_type_controller import CourseTypeController
from backend.controller.section_controller import SectionController
from backend.controller.semester_controller import SemesterController
from frontend.genetic_algorithm.course_table_frame import CourseTableFrame
from frontend.genetic_algorithm.teacher_table_frame import TeacherTableFrame

class GeneticAlgorithmSetup(tk.Toplevel):
    def __init__(self, master, assignments):
        super().__init__(master)
        self.assignments = assignments
        self.title("Configuración del Algoritmo Genético")
        self.geometry("1100x800")

        # Controllers
        self.course_controller = CourseController()
        self.teacher_controller = TeacherController()
        self.period_controller = PeriodController()
        self.section_controller = SectionController()
        self.career_controller = CareerController()
        self.semester_controller = SemesterController()
        self.course_type_controller = CourseTypeController()

        # Maps
        self.section_map = self.get_section_map()
        self.career_map = self.get_career_map()
        self.semester_map = self.get_semester_map()
        self.type_map = self.get_course_type_map()

        # Main Container
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Courses Table
        self.course_table = CourseTableFrame(
            master=container,
            courses=self.course_controller.find_all_courses(),
            career_map=self.career_map,
            semester_map=self.semester_map,
            section_map=self.section_map,
            type_map=self.type_map
        )
        self.course_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))

        # Teachers Table
        self.teacher_table = TeacherTableFrame(
            master=container,
            teachers=self.teacher_controller.find_all_teachers()
        )
        self.teacher_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))

        # Population input
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Población inicial").pack(side=tk.LEFT)

        # Population input validator
        self.population_var = tk.StringVar()
        population_command = (self.register(lambda P: P.isdigit() or P == ""), "%P")
        population_entry = tk.Entry(input_frame, textvariable=self.population_var, width=10, validate="key", validatecommand=population_command)
        population_entry.pack(side=tk.LEFT, padx=5)

        # End criteria selector
        criteria_frame = tk.Frame(self)
        criteria_frame.pack(pady=10)
        tk.Label(criteria_frame, text="Criterio de Finalización").pack(side=tk.LEFT)
        self.criteria_var = tk.StringVar(value="Número de Generaciones")
        criteria_selector = ttk.Combobox(
            criteria_frame,
            textvariable=self.criteria_var,
            values=["Número de Generaciones", "Valor Óptimo de Aptitud"],
            state="readonly",
            width=30
        )
        criteria_selector.pack(side=tk.LEFT, padx=5)
        criteria_selector.bind("<<ComboboxSelected>>", self.toggle_criteria_input)

        # End criteria input
        self.criteria_value_frame = tk.Frame(self)
        self.criteria_value_frame.pack(pady=5)
        self.criteria_value_label = tk.Label(self.criteria_value_frame, text="Cantidad:")
        self.criteria_value_label.pack(side=tk.LEFT)
        self.end_criteria_value_var = tk.StringVar()
        self.end_criteria_value_entry = tk.Entry(
            self.criteria_value_frame,
            textvariable=self.end_criteria_value_var,
            width=10,
            validate="key",
            validatecommand=population_command
        )
        self.end_criteria_value_entry.pack(side=tk.LEFT, padx=5)

        # Message label
        self.message_label = tk.Label(self, text="", fg="red", font=("Arial", 10))
        self.message_label.pack(pady=(0, 5))

        # Generate Button
        generate_button = tk.Button(self, text="Generar Horario", command=self.generate)
        generate_button.pack(pady=(0, 10))

    def get_section_map(self):
        return {section.id: section.description for section in self.section_controller.get_all_sections()}

    def get_career_map(self):
        return {career.id: career.description for career in self.career_controller.get_all_careers()}

    def get_semester_map(self):
        return {semester.id: semester.description for semester in self.semester_controller.get_all_semesters()}

    def get_course_type_map(self):
        return {type.id: type.description for type in self.course_type_controller.get_all_course_types()}

    def show_temporal_message(self, text, color="black", duration=5000):
        self.message_label.config(text=text, fg=color)
        self.after(duration, lambda: self.message_label.config(text=""))

    def get_population_size(self):
        value = self.population_var.get()
        if value.isdigit() and int(value) > 10:
            return int(value)
        return None

    def get_criteria(self):
        return self.criteria_var.get()

    def get_end_criteria_value(self):
        value = self.end_criteria_value_var.get()
        if not value.isdigit():
            return None
        value = int(value)
        criteria = self.get_criteria()
        if criteria == "Número de Generaciones":
            return value if value > 10 else None
        if criteria == "Valor Óptimo de Aptitud":
            return value if 1 <= value <= 100 else None
        return None

    def toggle_criteria_input(self, event=None):
        criteria = self.get_criteria()
        if criteria == "Número de Generaciones":
            self.criteria_value_label.config(text="Cantidad:")
        else:
            self.criteria_value_label.config(text="Valor óptimo de aptitud")

    def generate(self):
        population = self.get_population_size()
        criteria = self.get_criteria()
        criteria_val = self.get_end_criteria_value()

        if not self.assignments:
            self.show_temporal_message("No se cargo ninguna relacion Docente-Curso", color="red")
            return

        if population is None:
            self.show_temporal_message("La población inicial debe ser mayor a 10", color="red")
            return

        courses = self.course_table.get_selected_course_objects()
        teachers = self.teacher_table.get_selected_teacher_objects()

        if not courses:
            self.show_temporal_message("Debes seleccionar al menos un curso", color="red")
            return

        if not teachers:
            self.show_temporal_message("Debes seleccionar al menos un docente", color="red")
            return

        if criteria == "Número de Generaciones" and criteria_val is None:
            self.show_temporal_message("La cantidad de generaciones debe ser mayor a 10", color="red")
            return

        if criteria == "Valor Óptimo de Aptitud":
            if not self.end_criteria_value_var.get().strip():
                self.show_temporal_message("Debes ingresar un valor óptimo de aptitud", color="red")
                return
            if criteria_val is None:
                self.show_temporal_message("El valor óptimo debe estar entre 1 y 100", color="red")
                return

        # Start genetic algorithm
        GeneticAlgorithmController(
            teachers,
            courses,
            self.assignments,
            self.period_controller.get_all_periods(),
            population,
            criteria == "Número de Generaciones",
            criteria_val
        )
