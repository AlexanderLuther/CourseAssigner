import tkinter as tk
from tkinter import ttk, messagebox
from backend.Exception.HellException import HellException
from backend.controller.ClassroomController import ClassroomController

class ClassroomViewer:
    def __init__(self, parent):
        self.classroom_controller = ClassroomController()
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Listado de Salones")
        self.window.geometry("500x500")
        self.tree = None
        self.classrooms = []
        self.init_table()
        self.add_action_buttons()

    def init_table(self):
        self.classrooms = self.classroom_controller.get_all_classrooms()
        if not self.classrooms:
            label = tk.Label(self.window, text="No hay salones registrados.", font=("Arial", 12))
            label.pack(pady=20)
            return

        self.tree = ttk.Treeview(self.window, columns=("ID", "Descripcion"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descripcion", text="Descripción")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Descripcion", width=300, anchor="w")
        self.tree.pack(pady=20, fill="both", expand=True)
        for classroom in self.classrooms:
            self.tree.insert("", "end", values=(classroom.id, classroom.description))

    def add_action_buttons(self):
        frame = tk.Frame(self.window)
        frame.pack(pady=10)
        edit_button = tk.Button(frame, text="Editar", width=12, command=self.edit_action)
        edit_button.grid(row=0, column=0, padx=10)
        delete_button = tk.Button(frame, text="Borrar", width=12, command=self.delete_action)
        delete_button.grid(row=0, column=1, padx=10)

    def get_selected_classroom(self):
        classroom_selected = self.tree.selection()
        if not classroom_selected:
            return None
        item = self.tree.item(classroom_selected)
        id = item["values"][0]
        for classroom in self.classrooms:
            if classroom.id == id:
                return classroom
        return None

    def delete_action(self):
        classroom = self.get_selected_classroom()
        if not classroom:
            return
        self.classroom_controller.delete_classroom(classroom.id)
        self.refresh_table()
        self.show_temporal_message(f"Salón {classroom.description} eliminado correctamente.", color="green")

    def edit_action(self):
        classroom = self.get_selected_classroom()
        if not classroom:
            return
        self.open_edit_window(classroom)

    def open_edit_window(self, classroom):
        edit_win = tk.Toplevel(self.window)
        edit_win.title("Editar salón")
        edit_win.geometry("350x200")

        # Description label
        label = tk.Label(edit_win, text="Descripcion", font=("Arial", 12))
        label.pack(pady=10)

        # Error label
        self.error_label = tk.Label(self.window, text="", fg="red", font=("Arial", 10))
        self.error_label.pack()
        description_entry = tk.Entry(edit_win, width=40)
        description_entry.insert(0, classroom.description)
        description_entry.pack(pady=10)

        def save_changes():
            new_description = description_entry.get().strip()
            if not new_description:
                self.show_temporal_message("Descripcion de salon requerida.", color="red")
                return
            if new_description == classroom.description:
                edit_win.destroy()
                return
            try:
                self.classroom_controller.update_classroom(classroom.id, new_description)
                self.show_temporal_message("Salón editado correctamente.", color="green")
                edit_win.destroy()
                self.refresh_table()
            except HellException as e:
                self.show_temporal_message(str(e), color="red")

        save_button = tk.Button(edit_win, text="Guardar cambios", command=save_changes)
        save_button.pack(pady=10)

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        self.classrooms = self.classroom_controller.get_all_classrooms()
        if not self.classrooms:
            label = tk.Label(self.window, text="No hay salones registrados.", font=("Arial", 12))
            label.pack(pady=20)
            return
        for classroom in self.classrooms:
            self.tree.insert("", "end", values=(classroom.id, classroom.description))

    def show_temporal_message(self, texto, color="black"):
        if hasattr(self, "message_label") and self.message_label.winfo_exists():
            self.message_label.destroy()
        self.message_label = tk.Label(self.window, text=texto, fg=color, font=("Arial", 10))
        self.message_label.pack(pady=5)
        self.window.after(3000, self.message_label.destroy)
