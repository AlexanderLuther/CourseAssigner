import tkinter as tk
from frontend.course_assigner import CourseAssigner
from backend.db.connection.database_connection import DatabaseSession

if __name__ == "__main__":
    # Database
    DatabaseSession.initialize(
        user='root',
        password='********.',
        host='localhost',
        db_name='COURSE_ASSIGNER'
    )

    # UI
    root = tk.Tk()
    app = CourseAssigner(root)
