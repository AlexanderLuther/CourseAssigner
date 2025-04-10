import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from backend.Exception.HellException import HellException
from backend.controller.TeacherController import TeacherController
from backend.controller.TimeController import TimeController

class AddTeacherForm:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Nuevo Docente")
        self.window.geometry("400x400")
        self.teacher_controller = TeacherController()

        # Get all available time
        self.available_times = self.get_available_times()

        # Validate id method
        id_validator = (self.window.register(self.validate_id), "%P")

        # id
        tk.Label(self.window, text="Registro de Personal").pack(pady=(10, 0))
        self.id_entry = tk.Entry(self.window, validate="key", validatecommand=id_validator)
        self.id_entry.pack(pady=5)

        # Name
        tk.Label(self.window, text="Nombre del Docente").pack(pady=(10, 0))
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)

        # Entry hour
        tk.Label(self.window, text="Hora de Entrada").pack(pady=(10, 0))
        self.entry_hour_var = tk.StringVar(value="")
        self.entry_hour_menu = tk.OptionMenu(self.window, self.entry_hour_var, *self.available_times)
        self.entry_hour_menu.pack(pady=5)

        # Departure hour
        tk.Label(self.window, text="Hora de Salida").pack(pady=(10, 0))
        self.departure_hour_var = tk.StringVar(value="")
        self.departure_hour_menu = tk.OptionMenu(self.window, self.departure_hour_var, *self.available_times)
        self.departure_hour_menu.pack(pady=5)

        # Buttons
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=20)
        save_button = tk.Button(buttons_frame, text="Guardar", width=12, command=self.save_teacher)
        save_button.grid(row=0, column=0, padx=10)
        cancel_button = tk.Button(buttons_frame, text="Cancelar", width=12, command=self.window.destroy)
        cancel_button.grid(row=0, column=1, padx=10)

        # Error label
        self.error_label = tk.Label(self.window, text="", fg="red")
        self.error_label.pack()

    def get_available_times(self):
        time_controller = TimeController()
        raw_times = time_controller.get_all_times()
        time_map = {}
        for time in raw_times:
            time_str = datetime.strptime(str(time.time), "%H:%M:%S").strftime("%H:%M")
            time_map[time_str] = time.id
        return list(time_map.keys())

    def validate_id(self, new_value):
        return new_value.isdigit() and len(new_value) <= 10 or new_value == ""

    def show_error(self, message):
        self.error_label.config(text=message)
        self.window.after(3000, lambda: self.error_label.config(text=""))

    def save_teacher(self):
        name = self.name_entry.get().strip()
        id = self.id_entry.get().strip()
        start_hour = self.entry_hour_var.get()
        end_hour = self.departure_hour_var.get()

        # Verify required fields
        if not name:
            self.show_error("Nombre del Docente es obligatorio")
            return
        if not id:
            self.show_error("Registro de Personal es obligatorio")
            return
        if not start_hour:
            self.show_error("Debe seleccionar una Hora de Entrada")
            return
        if not end_hour:
            self.show_error("Debe seleccionar una Hora de Salida")
            return

        # Verify start hour is minor than departure hour
        fmt = "%H:%M"
        if datetime.strptime(start_hour, fmt) >= datetime.strptime(end_hour, fmt):
            self.show_error("La hora de entrada debe ser menor que la hora de salida")
            return

        try:
            self.teacher_controller.save_teacher(id, name, start_hour, end_hour)
            messagebox.showinfo("Éxito", f"Docente '{name}' guardado correctamente.")
            self.window.destroy()
        except HellException as e:
            self.show_error(str(e))




