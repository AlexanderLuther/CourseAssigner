from datetime import datetime
import random
from reportlab.lib.pagesizes import landscape, A3, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from backend.controller.career_controller import CareerController
from backend.controller.section_controller import SectionController
from backend.controller.semester_controller import SemesterController
from backend.db.model.classroom_model import ClassroomModel
from backend.db.model.course_model import CourseModel
from backend.db.model.period_model import PeriodModel
from backend.db.model.teacher_model import TeacherModel

class PDFGenerator:

    def __init__(self):
        career_controller = CareerController()
        semester_controller = SemesterController()
        section_controller = SectionController()
        self.careers_dict = {c.id: c.description for c in career_controller.get_all_careers()}
        self.sections_dict = {s.id: s.description for s in section_controller.get_all_sections()}
        self.semesters_dict = {s.id: s.description for s in semester_controller.get_all_semesters()}

    def export_schedule_to_pdf(
        self,
        best_chromosome: list[dict],
        periods: list[PeriodModel],
        classrooms: list[ClassroomModel],
        teachers: dict[str, TeacherModel],
        courses: dict[str, CourseModel],
        filename="schedule.pdf",
    ):
        # Order periods and classrooms
        sorted_periods = sorted(periods, key=lambda p: p.start_time)
        sorted_classrooms = sorted(classrooms, key=lambda c: c.id)

        # Create PDF document with the provided data.
        doc = SimpleDocTemplate(
            filename,
            pagesize=landscape(A3),
            leftMargin=0.2 * cm,
            rightMargin=0.2 * cm,
            topMargin=0.2 * cm,
            bottomMargin=0.2 * cm
        )
        usable_width = doc.width

        # Style
        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        normal_style.fontSize = 5
        normal_style.leading = 8
        normal_style.spaceAfter = 0
        normal_style.spaceBefore = 0

        # Set a color per career
        career_ids = list({course.id_career for course in courses.values()})
        career_colors = dict(zip(career_ids, self.__generate_colors(len(career_ids))))

        # Create color table
        color_table = self.__create_color_table(career_ids, career_colors)
        elements = [color_table, Spacer(1, 0.2 * cm)]

        # Schedule headers
        table_data = [["Periodo / Aula"] + [classroom.description for classroom in sorted_classrooms]]
        cell_backgrounds = []

        # Period per row
        for period in sorted_periods:
            row = [f"{period.start_time.strftime('%H:%M')} - {period.end_time.strftime('%H:%M')}"]

            # Add an empty cell per classroom in row
            for classroom in sorted_classrooms:
                cell = ""
                bg_color = None
                for gene in best_chromosome:

                    #Add data to cell if a course is assigned to the classroom
                    if gene["period_id"] == period.id and gene["classroom_id"] == classroom.id:
                        course = courses.get(gene["course_id"])
                        teacher = teachers.get(gene["teacher_id"])
                        if course and teacher:
                            type = "Obligatorio" if course.id_course_type == 2 else "Optativo"
                            section = self.sections_dict.get(course.id_section, f"Sección {course.id_section}")
                            semester = self.semesters_dict.get(course.id_semester, f"Semestre {course.id_semester}")
                            cell = (
                                f"{course.name}<br/>"
                                f"{section}<br/>"
                                f"{type}<br/>"
                                f"{semester}<br/>"
                                f"{teacher.name}"
                            )
                            bg_color = career_colors.get(course.id_career, colors.white)
                        break
                row.append(Paragraph(cell, normal_style))
                if bg_color:
                    col_idx = len(row) - 1
                    row_idx = len(table_data)
                    cell_backgrounds.append(("BACKGROUND", (col_idx, row_idx), (col_idx, row_idx), bg_color))

            table_data.append(row)

        # Width of each column
        first_col_width = 3 * cm
        remaining_width = usable_width - first_col_width
        num_classrooms = len(sorted_classrooms)
        classroom_col_width = max(1.5 * cm, remaining_width / num_classrooms)
        col_widths = [first_col_width] + [classroom_col_width] * num_classrooms

        # Create schedule
        table = Table(table_data, repeatRows=1, colWidths=col_widths)

        #Schedule style
        table_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (0, -1), colors.lightgrey),
            ("TEXTCOLOR", (0, 1), (0, -1), colors.black),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ])

        # Apply color in each cell
        for bg in cell_backgrounds:
            table_style.add(*bg)

        # Apply schedule style
        table.setStyle(table_style)

        # Add schedule to PDF
        elements.append(table)

        #Build PDF
        doc.build(elements, onFirstPage=self.__add_page_number, onLaterPages=self.__add_page_number)

    def __create_color_table(self, career_ids, career_colors):
        legend_data = [["Color", "Carrera"]]
        for cid in career_ids:
            legend_data.append(["", self.careers_dict.get(cid, f"Carrera {cid}")])
        table = Table(legend_data, colWidths=[1.2 * cm, 7 * cm])
        legend_style = TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 3.5),
        ])
        for i, cid in enumerate(career_ids):
            legend_style.add("BACKGROUND", (0, i + 1), (0, i + 1), career_colors[cid])
        table.setStyle(legend_style)
        return table

    def __generate_colors(self, n):
        base_colors = [
            colors.lightblue, colors.lightgreen, colors.lightcoral, colors.khaki,
            colors.orange, colors.violet, colors.cadetblue, colors.beige,
            colors.paleturquoise, colors.plum, colors.wheat
        ]
        if n <= len(base_colors):
            return base_colors[:n]
        else:
            return [colors.HexColor(f"#{random.randint(0x444444, 0xAAAAAA):06X}") for _ in range(n)]


    def __add_page_number(self, canvas: Canvas, doc):
        canvas.setFont("Helvetica", 4)
        canvas.drawRightString(1600, 10, f"Página {doc.page}")

    def export_execution_summary(
            self,
            execution_time: float,
            total_generations: int,
            base_fitness: int,
            best_fitness: int,
            total_memory: float,
            conflicts_history: list[int],
            filename="execution_summary.pdf"
    ):
        # Create PDF
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        # PDF Styles
        styles = getSampleStyleSheet()
        normal = styles["Normal"]
        title = styles["Title"]

        elements = [
            Paragraph("Resumen de Ejecución del Algoritmo Genético", title),
            Spacer(1, 1 * cm),
            Paragraph(f"<b>Fecha de ejecución:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", normal),
            Paragraph(f"<b>Tiempo total:</b> {execution_time:.2f} segundos", normal),
            Paragraph(f"<b>Total de memoria utilizada:</b> {total_memory / 1024:.2f} KB", normal),
            Paragraph(f"<b>Total de generaciones:</b> {total_generations}", normal),
            Paragraph(f"<b>Valor de aptitud base:</b> {base_fitness}", normal),
            Paragraph(f"<b>Mejor valor de aptitud:</b> {best_fitness}", normal)
        ]

        # Create and add table of conflicts
        conflict_table = self.create_conflitcs_table(conflicts_history)
        elements.append(Spacer(1, 1 * cm))
        elements.append(Paragraph("Conflictos por generación", title))
        elements.append(conflict_table)


        # Build PDF
        doc.build(elements)

    def create_conflitcs_table(self, conflicts_history):
        # Table Headers
        conflict_table_data = [["Generación", "Conflictos"]]

        # Fill data per generation
        for i, conflicts in enumerate(conflicts_history, 1):
            conflict_table_data.append([str(i), str(conflicts)])

        # Create table
        conflict_table = Table(conflict_table_data, colWidths=[4 * cm, 4 * cm])
        conflict_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        return conflict_table

