import tkinter as tk
from tkinter import ttk, messagebox
from backend.controller.teacher_controller import TeacherController
from datetime import datetime
from backend.controller.time_controller import TimeController

class TeacherViewer:
    def __init__(self, parent):
        self.teacher_controller = TeacherController()
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Listado de Docentes")
        self.window.geometry("600x500")
        self.tree = None
        self.teachers = []
        self.message_label = None
        self.available_times = self.get_available_times()
        self.init_table()
        self.add_action_buttons()

    def get_available_times(self):
        time_controller = TimeController()
        raw_times = time_controller.get_all_times()
        time_map = {}
        for time in raw_times:
            time_str = datetime.strptime(str(time.time), "%H:%M:%S").strftime("%H:%M")
            time_map[time_str] = time.id
        return list(time_map.keys())

    def init_table(self):
        self.teachers = self.teacher_controller.get_all_teachers()
        if not self.teachers:
            self.show_temporal_message("No hay docentes registrados.", color="red")
            return
        self.tree = ttk.Treeview(
            self.window,
            columns=("id", "name", "entry", "departure"),
            show="headings",
            height=10
        )
        self.tree.heading("id", text="Registro Personal")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("entry", text="Hora de Entrada")
        self.tree.heading("departure", text="Hora de Salida")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("entry", width=100, anchor="center")
        self.tree.column("departure", width=100, anchor="center")
        self.tree.pack(pady=20, fill="both", expand=True)
        self._load_teachers_into_tree()

    def _load_teachers_into_tree(self):
        for teacher in self.teachers:
            self.tree.insert(
                "", "end",
                values=(
                    teacher.id,
                    teacher.name,
                    teacher.entry_time.strftime("%H:%M"),
                    teacher.departure_time.strftime("%H:%M")
                )
            )

    def add_action_buttons(self):
        frame = tk.Frame(self.window)
        frame.pack(pady=10)
        edit_button = tk.Button(frame, text="Editar", width=12, command=self.edit_action)
        edit_button.grid(row=0, column=0, padx=10)
        delete_button = tk.Button(frame, text="Borrar", width=12, command=self.delete_action)
        delete_button.grid(row=0, column=1, padx=10)

    def get_selected_teacher(self):
        if not self.tree:
            return None
        selection = self.tree.selection()
        if not selection:
            return None
        item = self.tree.item(selection)
        id = item["values"][0]
        for teacher in self.teachers:
            if teacher.id == str(id):
                return teacher
        return None

    def delete_action(self):
        teacher = self.get_selected_teacher()
        if not teacher:
            return
        self.teacher_controller.delete_teacher(teacher.id)
        self.refresh_table()
        self.show_temporal_message(f"Docente '{teacher.name}' eliminado.", color="green")

    def edit_action(self):
        teacher = self.get_selected_teacher()
        if not teacher:
            return
        self.open_edit_window(teacher)

    def open_edit_window(self, teacher):
        edit_win = tk.Toplevel(self.window)
        edit_win.title("Editar Docente")
        edit_win.geometry("400x400")

        # Name
        tk.Label(edit_win, text="Nombre del Docente").pack(pady=(10, 0))
        name_entry = tk.Entry(edit_win)
        name_entry.insert(0, teacher.name)
        name_entry.pack(pady=5)

        # Entry hour
        tk.Label(edit_win, text="Hora de Entrada").pack(pady=(10, 0))
        entry_hour_var = tk.StringVar(value=teacher.entry_time.strftime("%H:%M"))
        entry_hour_menu = tk.OptionMenu(edit_win, entry_hour_var, *self.available_times)
        entry_hour_menu.pack(pady=5)

        # Departure hour
        tk.Label(edit_win, text="Hora de Salida").pack(pady=(10, 0))
        departure_hour_var = tk.StringVar(value=teacher.departure_time.strftime("%H:%M"))
        departure_hour_menu = tk.OptionMenu(edit_win, departure_hour_var, *self.available_times)
        departure_hour_menu.pack(pady=5)

        # Error label
        error_label = tk.Label(edit_win, text="", fg="red")
        error_label.pack(pady=5)

        # Update method
        def update_teacher():
            name = name_entry.get().strip()
            start_hour = entry_hour_var.get()
            end_hour = departure_hour_var.get()
            fmt = "%H:%M"
            if not name:
                error_label.config(text="Nombre del Docente es obligatorio")
                return
            if not start_hour:
                error_label.config(text="Debe seleccionar una Hora de Entrada")
                return
            if not end_hour:
                error_label.config(text="Debe seleccionar una Hora de Salida")
                return
            if datetime.strptime(start_hour, fmt) >= datetime.strptime(end_hour, fmt):
                error_label.config(text="La hora de entrada debe ser menor que la de salida")
                return
            if teacher.name == name and teacher.entry_time.strftime(fmt) == start_hour and teacher.departure_time.strftime(fmt) == end_hour:
                self.show_temporal_message("Docente editado.", color="green")
                edit_win.destroy()
                return
            self.teacher_controller.update_teacher(
                teacher.id,
                name,
                datetime.strptime(start_hour, fmt).time(),
                datetime.strptime(end_hour, fmt).time()
            )
            self.show_temporal_message("Docente editado.", color="green")
            edit_win.destroy()
            self.refresh_table()

        # Buttons
        buttons_frame = tk.Frame(edit_win)
        buttons_frame.pack(pady=20)
        save_button = tk.Button(buttons_frame, text="Guardar", width=12, command=update_teacher)
        save_button.grid(row=0, column=0, padx=10)
        cancel_button = tk.Button(buttons_frame, text="Cancelar", width=12, command=edit_win.destroy)
        cancel_button.grid(row=0, column=1, padx=10)

    def refresh_table(self):
        if not self.tree:
            return
        self.tree.delete(*self.tree.get_children())
        self.teachers = self.teacher_controller.get_all_teachers()
        if not self.teachers:
            self.tree.pack_forget()
            self.show_temporal_message("No hay docentes registrados.", color="red")
            return
        self.tree.pack(pady=20, fill="both", expand=True)
        self._load_teachers_into_tree()

    def show_temporal_message(self, texto, color="black"):
        if self.message_label and self.message_label.winfo_exists():
            self.message_label.destroy()
        self.message_label = tk.Label(self.window, text=texto, fg=color, font=("Arial", 10))
        self.message_label.pack(pady=5)
        self.window.after(3000, lambda: self.message_label.destroy())
