import tkinter as tk
from tkinter import ttk

class AssignmentViewer(tk.Toplevel):
    def __init__(self, parent, assignments: dict):
        super().__init__(parent)
        self.title("Relacion de Docentes a Cursos")
        self.geometry("700x500")

        # Treeview
        self.tree = ttk.Treeview(self, columns=("course",), show="tree headings")
        self.tree.heading("#0", text="Docente")
        self.tree.heading("course", text="Curso")

        # Columns size
        self.tree.column("#0", width=250, anchor="w")
        self.tree.column("course", width=400, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert data
        self.insert_assignments(assignments)

    def insert_assignments(self, assignment: dict):
        for teacher_id, info in assignment.items():
            teacher = info["teacher"]
            teacher_name = getattr(teacher, "name", "Sin nombre")

            #Insert teacher
            parent_id = self.tree.insert(
                "", tk.END,
                text=f"{teacher_name} -{ teacher_id}"
            )

            # Insert courses
            for course in info["courses"]:
                code = getattr(course, "code", "-")
                title = getattr(course, "name", "Sin título")
                full_course = f"{code} - {title}"

                self.tree.insert(
                    parent_id, tk.END,
                    values=(full_course,)
                )