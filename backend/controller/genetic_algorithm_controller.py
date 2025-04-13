import random
from collections import defaultdict
from backend.db.model.course_model import CourseModel
from backend.db.model.period_model import PeriodModel
from backend.db.model.teacher_model import TeacherModel

class GeneticAlgorithmController:

    def __init__(
            self,
            teachers: list[TeacherModel],
            courses: list[CourseModel],
            assignments,
            periods: list[PeriodModel],
            population: int,
            limited_by_generation: bool,
            limit: int
    ):
        population = self.generate_initial_population(courses, teachers, periods, population)
        for chromosome in population:
            fitness = self.evaluate_fitness(chromosome, assignments, self.__build_teachers_dict(teachers), self.__build_courses_dict(courses), self.__build_periods_dict(periods))
            print({"fitness": fitness})


    def generate_initial_population(
            self,
            courses: list[CourseModel],
            teachers: list[TeacherModel],
            periods: list[PeriodModel],
            population_size: int
    ):
        """
        Generates an initial population of chromosomes for a genetic algorithm. Each chromosome
        represents a possible scheduling configuration where each course is assigned a randomly
        selected teacher and a period. This function is foundational for initializing the genetic
        algorithm to solve scheduling-related optimization problems.

        :param courses: A list of course objects included in the scheduling problem.
        :param teachers: A list of teacher objects available for assignment.
        :param periods: A list of available periods for scheduling.
        :param population_size: The number of chromosomes to include in the initial population.
        :return: Returns a list of chromosomes, where each chromosome is a list of dictionaries.
            Each dictionary represents a course-to-teacher-to-period assignment, containing keys
            for `course_id`, `teacher_id`, and `period_id`.
        """
        population = []
        for _ in range(population_size):
            chromosome = []
            # Generate one gen per course
            for course in courses:
                teacher = random.choice(teachers)
                period = random.choice(periods)
                chromosome.append({
                    "course_id": course.code,
                    "teacher_id": teacher.id,
                    "period_id": period.id
                })
            population.append(chromosome)
        return population

    def evaluate_fitness(
            self,
            chromosome,
            assignment,
            teachers: dict[str, TeacherModel],
            courses: dict[str, CourseModel],
            periods: dict[str, PeriodModel]
    ):
        """
        Evaluates the fitness of a given chromosome for a scheduling problem by applying penalties and bonuses
        based on constraints and requirements.

        :param chromosome: The chromosome to evaluate, represented as a list of genes, where each gene
           contains `course_id`, `teacher_id`, and `period_id`.
        :param assignment: The assignment of courses to teachers, structured as a dictionary where keys
           are teacher IDs and values are dictionaries containing assigned courses.
        :param teachers: A dictionary of teacher models where the keys are teacher IDs and the values
           are `TeacherModel` instances containing teacher information.
        :param courses: A dictionary of course models where the keys are course IDs and the values are
           `CourseModel` instances containing course data.
        :param periods: A dictionary of period models where the keys are period IDs and the values
           are `PeriodModel` instances representing scheduling periods.
        :return: The fitness score of the chromosome, calculated as the base score reduced by any
           penalties incurred for violating constraints.
        """
        fitness = 0
        penalty = 0
        teacher_schedule = defaultdict(set)
        required_courses = defaultdict(set)

        # Apply Penalties
        for gene in chromosome:
            # Get ids from gene
            course_id = gene["course_id"]
            teacher_id = gene["teacher_id"]
            period_id = gene["period_id"]

            # Get objects from dicts
            course = courses.get(course_id)
            teacher = teachers.get(teacher_id)
            period = periods.get(period_id)

            # INCOMPLETE GEN PENALIZATION
            if not course or not teacher or not period:
                penalty += 20
                continue

            # TEACHER CANT TEACH THE COURSE PENALIZATION
            can_teach = any(c.code == course_id for c in assignment.get(teacher_id, {}).get("courses", []))
            if not can_teach:
                penalty += 10

            # OUTSIDE OF TEACHER'S SCHEDULE PENALIZATION
            if period.start_time < teacher.entry_time or period.end_time > teacher.departure_time:
                penalty += 5

            # OVERLAPPING COURSES OF THE SAME TEACHER PENALIZATION
            if period_id in teacher_schedule[teacher_id]:
                penalty += 15
            else:
                teacher_schedule[teacher_id].add(period_id)

            # OVERLAP BETWEEN REQUIRED COURSES OF THE SAME SEMESTER AND CAREER
            if course.id_course_type == 2:
                key = (course.id_career, course.id_semester)
                if period_id in required_courses[key]:
                    penalty += 10
                else:
                    required_courses[key].add(period_id)

        # Apply Semester continuity bonus
        for (career, semester), periods_in_use in required_courses.items():
            sorted_periods = sorted(periods_in_use)
            for i in range(len(sorted_periods) - 1):
                if sorted_periods[i + 1] - sorted_periods[i] == 1:
                    fitness += 2

        return fitness - penalty




    def __build_teachers_dict(self, teachers: list[TeacherModel]):
        return {teacher.id: teacher for teacher in teachers}

    def __build_courses_dict(self, courses: list[CourseModel]):
        return {course.code: course for course in courses}

    def __build_periods_dict(self, periods: list[PeriodModel]):
        return {period.id: period for period in periods}
