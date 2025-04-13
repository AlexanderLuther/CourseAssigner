import tkinter as tk
from tkinter import ttk

class TeacherTableFrame(tk.LabelFrame):
    def __init__(self, master, teachers):
        super().__init__(master, text="Docentes")

        # Set uncheck and check images
        self.checked_image = tk.PhotoImage(data='''
            R0lGODlhEAAQAPIAAP///wAAAMbGxv///wAAAAAAAAAAACH5BAEAAAMALAAAAAAQABAAAA
            RCKMlJq7046827/2AojmRpnmiqrmzrvnAsz3Rt33ju93gFADs=
        ''')
        self.unchecked_image = tk.PhotoImage(data='''
            R0lGODlhEAAQAKIAAP///wAAAMbGxv///wAAAAAAAAAAAAAAAAAAACH5BAEAAAEALAAAAA
            AQABAAAANRKMlJq7046827/2AoIATxTAQA7
        ''')

        self.selected_teachers = set()
        self.teacher_objects = {}

        self.tree = ttk.Treeview(
            self,
            columns=("id", "name", "entry", "departure"),
            show="tree headings"
        )

        # Table headers
        self.tree.heading("#0", text="Utilizar?")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("entry", text="Hora Entrada")
        self.tree.heading("departure", text="Hora Salida")

        # Table Columns
        self.tree.column("#0", width=30, anchor="center")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("entry", width=100, anchor="center")
        self.tree.column("departure", width=100, anchor="center")

        # Table configuration
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind Left click event
        self.tree.bind("<Button-1>", self.change_teacher_state)

        # Insert courses
        self.__insert_teachers(teachers)

    def __insert_teachers(self, teachers):
        for teacher in teachers:
            entry_str = teacher.entry_time.strftime("%H:%M") if teacher.entry_time else "-"
            departure_str = teacher.departure_time.strftime("%H:%M") if teacher.departure_time else "-"
            item = self.tree.insert(
                "", tk.END,
                text="",
                image=self.unchecked_image,
                values=(teacher.id, teacher.name, entry_str, departure_str)
            )
            self.tree.set(item, "id", teacher.id)
            self.teacher_objects[item] = teacher

    def change_teacher_state(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "tree":
            return
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        # Remove teacher
        if row_id in self.selected_teachers:
            self.selected_teachers.remove(row_id)
            self.tree.item(row_id, image=self.unchecked_image)
        # Add teacher
        else:
            self.selected_teachers.add(row_id)
            self.tree.item(row_id, image=self.checked_image)

    def get_selected_teacher_objects(self):
        return [self.teacher_objects[item_id] for item_id in self.selected_teachers]
