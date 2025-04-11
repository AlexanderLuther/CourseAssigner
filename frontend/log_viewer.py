import tkinter as tk
from tkinter import scrolledtext
import os

class LogViewer(tk.Toplevel):
    def __init__(self, master, log_file):
        super().__init__(master)
        self.title("Errores de Importación")
        self.geometry("800x500")
        self.log_file = log_file
        self.create_widgets()
        self.load_log()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Courier", 10))
        self.text_area.pack(expand=True, fill='both')
        self.text_area.configure(state='disabled')

    def load_log(self):
        if not os.path.exists(self.log_file):
            return

        with open(self.log_file, 'r', encoding='utf-8') as f:
            contenido = f.read()

        if contenido.strip():
            self.text_area.configure(state='normal')
            self.text_area.insert(tk.END, contenido)
            self.text_area.configure(state='disabled')
