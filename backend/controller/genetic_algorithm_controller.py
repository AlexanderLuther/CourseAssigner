import random
from collections import defaultdict
from backend.controller.pdf_generator import PDFGenerator
from backend.db.model.classroom_model import ClassroomModel
from backend.db.model.course_model import CourseModel
from backend.db.model.period_model import PeriodModel
from backend.db.model.teacher_model import TeacherModel

class GeneticAlgorithmController:

    def __init__(self):
        self.pdf_generator = PDFGenerator()
        pass

    def run_genetic_algorithm(
            self,
            courses: list[CourseModel],
            teachers: list[TeacherModel],
            periods: list[PeriodModel],
            classrooms: list[ClassroomModel],
            assignment,
            population_size,
            stop_by_generation,
            max_generations,
            target_fitness,
            mutation_rate,
            tournament_size,
            no_improve_limit=10
    ):
        best_fitness_ever = float('-inf')
        best_chromosome = None
        generation = 0
        generations_without_improvement = 0
        fitness_history = []

        teachers_dict = self.__build_teachers_dict(teachers)
        courses_dict = self.__build_courses_dict(courses)
        periods_dict = self.__build_periods_dict(periods)

        population = self.generate_initial_population(courses, teachers, periods, classrooms, population_size)

        while True:
            generation += 1

            evaluated = self.evaluate_population(population, assignment, teachers_dict, courses_dict, periods_dict)
            evaluated.sort(key=lambda x: x[1], reverse=True)
            current_best_chromosome, current_best_fitness = evaluated[0]
            fitness_history.append(current_best_fitness)

            if current_best_fitness > best_fitness_ever:
                best_fitness_ever = current_best_fitness
                best_chromosome = current_best_chromosome
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1

            if stop_by_generation:
                if generation >= max_generations:
                    break
            else:
                percent = (current_best_fitness / best_fitness_ever) * 100 if best_fitness_ever > 0 else 0
                if percent >= target_fitness or generations_without_improvement >= no_improve_limit:
                    break

            selected = self.tournament_selection(
                population,
                assignment,
                teachers_dict,
                courses_dict,
                periods_dict,
                tournament_size
            )

            next_generation = []
            for i in range(0, len(selected), 2):
                parent1 = selected[i]
                parent2 = selected[i + 1] if i + 1 < len(selected) else selected[0]
                child1, child2 = self.one_point_crossover(parent1, parent2)
                next_generation.extend([child1, child2])

            population = [
                self.random_resetting_mutation(chromo, teachers, periods, classrooms, mutation_rate)
                for chromo in next_generation
            ]

        self.pdf_generator.export_schedule_to_pdf(
            filename="schedule.pdf",
            best_chromosome=best_chromosome,
            periods=periods,
            classrooms=classrooms,
            teachers=teachers_dict,
            courses=courses_dict
        )
        return best_chromosome, best_fitness_ever, generation, fitness_history

    def generate_initial_population(
            self,
            courses: list[CourseModel],
            teachers: list[TeacherModel],
            periods: list[PeriodModel],
            classrooms: list[ClassroomModel],
            population_size: int
    ):
        population = []
        for _ in range(population_size):
            chromosome = []
            for course in courses:
                teacher = random.choice(teachers)
                period = random.choice(periods)
                classroom = random.choice(classrooms)

                chromosome.append({
                    "course_id": course.code,
                    "teacher_id": teacher.id,
                    "period_id": period.id,
                    "classroom_id": classroom.id
                })

            population.append(chromosome)
        return population

    def evaluate_population(
            self,
            population,
            assignment,
            teachers: dict[str, TeacherModel],
            courses: dict[str, CourseModel],
            periods: dict[str, PeriodModel]
    ):
        evaluated = []
        for chromo in population:
            fitness = self.evaluate_fitness(
                chromo,
                assignment,
                teachers,
                courses,
                periods
            )
            evaluated.append((chromo, fitness))
        return evaluated

    def evaluate_fitness(
            self,
            chromosome,
            assignment,
            teachers: dict[str, TeacherModel],
            courses: dict[str, CourseModel],
            periods: dict[str, PeriodModel]
    ) -> int:
        base_score = len(chromosome) * 10
        fitness = 0
        penalty = 0

        teacher_schedule = defaultdict(set)
        classroom_schedule = defaultdict(set)
        required_courses = defaultdict(set)

        for gene in chromosome:
            course_id = gene["course_id"]
            teacher_id = gene["teacher_id"]
            period_id = str(gene["period_id"])
            classroom_id = str(gene["classroom_id"])

            course = courses.get(course_id)
            teacher = teachers.get(teacher_id)
            period = periods.get(period_id)

            if not course or not teacher or not period:
                penalty += 20
                continue

            can_teach = any(c.code == course_id for c in assignment.get(teacher_id, {}).get("courses", []))
            if not can_teach:
                penalty += 10

            if period.start_time < teacher.entry_time or period.end_time > teacher.departure_time:
                penalty += 5

            if period_id in teacher_schedule[teacher_id]:
                penalty += 15
            else:
                teacher_schedule[teacher_id].add(period_id)

            if period_id in classroom_schedule[classroom_id]:
                penalty += 15
            else:
                classroom_schedule[classroom_id].add(period_id)

            if course.id_course_type == 2:
                key = (course.id_career, course.id_semester)
                if period_id in required_courses[key]:
                    penalty += 10
                else:
                    required_courses[key].add(period_id)

        for (career, semester), periods_in_use in required_courses.items():
            sorted_periods = sorted(periods_in_use)
            for i in range(len(sorted_periods) - 1):
                if sorted_periods[i + 1] - sorted_periods[i] == 1:
                    fitness += 2

        return base_score + fitness - penalty

    def tournament_selection(
            self,
            population,
            assignments,
            teachers: dict[str, TeacherModel],
            courses: dict[str, CourseModel],
            periods: dict[str, PeriodModel],
            tournament_size
    ):
        selected = []
        for _ in range(len(population)):
            tournament = random.sample(population, tournament_size)
            best = max(
                tournament,
                key=lambda chromosome: self.evaluate_fitness(
                    chromosome, assignments, teachers, courses, periods
                )
            )
            selected.append(best)
        return selected

    def one_point_crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def random_resetting_mutation(self, chromosome, teachers, periods, classrooms, mutation_rate=0.1):
        mutated = []
        for gene in chromosome:
            if random.random() < mutation_rate:
                new_teacher = random.choice(teachers)
                new_period = random.choice(periods)
                new_classroom = random.choice(classrooms)

                mutated_gene = {
                    "course_id": gene["course_id"],
                    "teacher_id": new_teacher.id,
                    "period_id": new_period.id,
                    "classroom_id": new_classroom.id
                }
                mutated.append(mutated_gene)
            else:
                mutated.append(gene)
        return mutated

    def __build_teachers_dict(self, teachers: list[TeacherModel]):
        return {teacher.id: teacher for teacher in teachers}

    def __build_courses_dict(self, courses: list[CourseModel]):
        return {course.code: course for course in courses}

    def __build_periods_dict(self, periods: list[PeriodModel]):
        return {str(period.id): period for period in periods}

    def __build_classrooms_dict(self, classrooms: list[ClassroomModel]):
        return {str(classroom.id): classroom for classroom in classrooms}