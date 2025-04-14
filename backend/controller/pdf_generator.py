from reportlab.lib.pagesizes import landscape, A3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
import random

from backend.db.model.classroom_model import ClassroomModel
from backend.db.model.course_model import CourseModel
from backend.db.model.period_model import PeriodModel
from backend.db.model.teacher_model import TeacherModel


class PDFGenerator:
    pass

    def export_schedule_to_pdf(
        self,
        filename: str,
        best_chromosome: list[dict],
        periods: list[PeriodModel],
        classrooms: list[ClassroomModel],
        teachers: dict[str, TeacherModel],
        courses: dict[str, CourseModel],
        careers: dict[int, str],
        sections: dict[int, str],
        semesters: dict[int, str]
    ):
        sorted_periods = sorted(periods, key=lambda p: p.start_time)
        sorted_classrooms = sorted(classrooms, key=lambda c: c.id)

        # Documento en A2 apaisado
        doc = SimpleDocTemplate(
            filename,
            pagesize=landscape(A3),
            leftMargin=0.2 * cm,
            rightMargin=0.2 * cm,
            topMargin=0.2 * cm,
            bottomMargin=0.2 * cm
        )
        usable_width = doc.width

        # Estilo extra compacto
        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        normal_style.fontSize = 5
        normal_style.leading = 8
        normal_style.spaceAfter = 0
        normal_style.spaceBefore = 0

        # Colores únicos por carrera
        def generate_color_palette(n):
            base_colors = [
                colors.lightblue, colors.lightgreen, colors.lightcoral, colors.khaki,
                colors.orange, colors.violet, colors.cadetblue, colors.beige,
                colors.paleturquoise, colors.plum, colors.wheat
            ]
            if n <= len(base_colors):
                return base_colors[:n]
            else:
                return [colors.HexColor(f"#{random.randint(0x444444, 0xAAAAAA):06X}") for _ in range(n)]

        career_ids = list({course.id_career for course in courses.values()})
        career_colors = dict(zip(career_ids, generate_color_palette(len(career_ids))))

        # Leyenda de colores
        legend_data = [["Color", "Carrera"]]
        for cid in career_ids:
            legend_data.append(["", careers.get(cid, f"Carrera {cid}")])
        legend_table = Table(legend_data, colWidths=[1.2 * cm, 7 * cm])
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
        legend_table.setStyle(legend_style)

        elements = [Paragraph("<b>Leyenda de colores por carrera</b>", styles["Heading4"]),
                    legend_table, Spacer(1, 0.2 * cm)]

        # Tabla principal
        table_data = [["Periodo / Aula"] + [c.description for c in sorted_classrooms]]
        cell_backgrounds = []

        for period in sorted_periods:
            row = [f"{period.start_time.strftime('%H:%M')} - {period.end_time.strftime('%H:%M')}"]

            for classroom in sorted_classrooms:
                cell = ""
                bg_color = None
                for gene in best_chromosome:
                    if gene["period_id"] == period.id and gene["classroom_id"] == classroom.id:
                        course = courses.get(gene["course_id"])
                        teacher = teachers.get(gene["teacher_id"])
                        if course and teacher:
                            tipo = "Obligatorio" if course.id_course_type == 1 else "Optativo"
                            carrera = careers.get(course.id_career, f"Carrera {course.id_career}")
                            seccion = sections.get(course.id_section, f"Sección {course.id_section}")
                            semestre = semesters.get(course.id_semester, f"Semestre {course.id_semester}")

                            cell = (
                                f"{course.name}<br/>"
                                f"{seccion}<br/>"
                                f"{tipo}<br/>"
                                f"{semestre}<br/>"
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

        # Cálculo de anchos de columna
        first_col_width = 3 * cm
        remaining_width = usable_width - first_col_width
        num_classrooms = len(sorted_classrooms)
        classroom_col_width = max(1.5 * cm, remaining_width / num_classrooms)
        col_widths = [first_col_width] + [classroom_col_width] * num_classrooms

        table = Table(table_data, repeatRows=1, colWidths=col_widths)

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

        for bg in cell_backgrounds:
            table_style.add(*bg)

        table.setStyle(table_style)
        elements.append(table)

        doc.build(elements, onFirstPage=self.__add_page_number, onLaterPages=self.__add_page_number)

    def __add_page_number(self, canvas: Canvas, doc):
        canvas.setFont("Helvetica", 4)
        canvas.drawRightString(1600, 10, f"Página {doc.page}")

