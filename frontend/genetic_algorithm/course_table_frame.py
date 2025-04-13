import tkinter as tk
from tkinter import ttk

class CourseTableFrame(tk.LabelFrame):
    def __init__(self, master, courses, career_map, semester_map, section_map, type_map):
        super().__init__(master, text="Cursos")

        # Set uncheck and check images
        self.checked_image = tk.PhotoImage(data='''
            R0lGODlhEAAQAPIAAP///wAAAMbGxv///wAAAAAAAAAAACH5BAEAAAMALAAAAAAQABAAAA
            RCKMlJq7046827/2AojmRpnmiqrmzrvnAsz3Rt33ju93gFADs=
        ''')
        self.unchecked_image = tk.PhotoImage(data='''
            R0lGODlhEAAQAKIAAP///wAAAMbGxv///wAAAAAAAAAAAAAAAAAAACH5BAEAAAEALAAAAA
            AQABAAAANRKMlJq7046827/2AoIATxTAQA7
        ''')

        self.selected_courses = set()
        self.course_objects = {}

        self.tree = ttk.Treeview(
            self,
            columns=("code", "name", "career", "semester", "section", "type"),
            show="tree headings"
        )

        # Table headers
        self.tree.heading("#0", text="Utilizar?")
        self.tree.heading("code", text="Código")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("career", text="Carrera")
        self.tree.heading("semester", text="Semestre")
        self.tree.heading("section", text="Sección")
        self.tree.heading("type", text="Tipo")

        # Table Columns
        self.tree.column("#0", width=30, anchor="center")
        self.tree.column("code", width=80, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("career", width=120, anchor="w")
        self.tree.column("semester", width=80, anchor="center")
        self.tree.column("section", width=80, anchor="center")
        self.tree.column("type", width=120, anchor="w")

        # Table configuration
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind Left click event
        self.tree.bind("<Button-1>", self.change_course_state)

        # Insert courses
        self.__insert_courses(courses, career_map, semester_map, section_map, type_map)

    def __insert_courses(self, courses, career_map, semester_map, section_map, type_map):
        for course in courses:
            item_id = self.tree.insert(
                "",
                tk.END,
                text="",
                image=self.unchecked_image,
                values=(
                    getattr(course, "code", "-"),
                    getattr(course, "name", "Sin nombre"),
                    career_map.get(course.id_career, "-"),
                    semester_map.get(course.id_semester, "-"),
                    section_map.get(course.id_section, "-"),
                    type_map.get(course.id_course_type, "-"),
                )
            )
            self.course_objects[item_id] = course
            self.tree.set(item_id, "code", course.code)

    def change_course_state(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "tree":
            return
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        if row_id in self.selected_courses:
            self.selected_courses.remove(row_id)
            self.tree.item(row_id, image=self.unchecked_image)
        else:
            self.selected_courses.add(row_id)
            self.tree.item(row_id, image=self.checked_image)

    def get_selected_course_objects(self):
        return [self.course_objects[item_id] for item_id in self.selected_courses]
