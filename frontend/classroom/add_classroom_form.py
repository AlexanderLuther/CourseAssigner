import tkinter as tk
from tkinter import messagebox

from backend.Exception.HellException import HellException
from backend.controller.ClassroomController import ClassroomController

class AddClassroomForm:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(self.parent)
        self.window.title("Nuevo Salon")
        self.window.geometry("400x200")
        self.classroom_controller = ClassroomController()
        self.init()

    def init(self):
        # Name label
        label = tk.Label(self.window, text="Descripcion", font=("Arial", 12))
        label.pack(pady=(20, 5))

        # Name input
        self.entry_description = tk.Entry(self.window, width=40)
        self.entry_description.pack(pady=5)
        self.entry_description.focus()

        # Error label
        self.error_label = tk.Label(self.window, text="", fg="red", font=("Arial", 10))
        self.error_label.pack()

        # Buttons
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=20)
        save_button = tk.Button(buttons_frame, text="Guardar", width=12, command=self.save_classroom)
        save_button.grid(row=0, column=0, padx=10)
        cancel_button = tk.Button(buttons_frame, text="Cancelar", width=12, command=self.window.destroy)
        cancel_button.grid(row=0, column=1, padx=10)

    def save_classroom(self):
        description = self.entry_description.get().strip()
        if not description:
            self.error_label.config(text="Descripcion de salon requerida.")
            return
        try:
            self.classroom_controller.save_classroom(description)
            messagebox.showinfo("Salón guardado", f"Salón {description} guardado correctamente.")
            self.window.destroy()
        except HellException as e:
            self.error_label.config(text=str(e))
