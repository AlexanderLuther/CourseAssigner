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
            no_improve_limit=1000
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
        """
        Generates the initial population of chromosomes for a genetic algorithm
        based on the given courses, teachers, periods, and classrooms.

        Each chromosome within the population represents a potential schedule
        solution. A chromosome is constructed by iterating through all the courses
        and randomly assigning a teacher, period, and classroom for each course.
        This process is repeated for the specified population size to generate
        the entire population.

        :param courses: List of courses to be scheduled.
        :type courses: list[CourseModel]
        :param teachers: List of teachers available for scheduling.
        :type teachers: list[TeacherModel]
        :param periods: List of periods available for scheduling.
        :type periods: list[PeriodModel]
        :param classrooms: List of classrooms available for scheduling.
        :type classrooms: list[ClassroomModel]
        :param population_size: Number of chromosomes to generate in the initial
            population.
        :type population_size: int
        :return: Initial population containing a list of chromosomes, where each
            chromosome is a list of course-teacher-period-classroom assignments.
        :rtype: list[list[dict]]
        """
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
        """
        Evaluates the given population by calculating fitness for each chromosome
        based on the provided assignment, teachers, courses, and periods.

        A list of tuples is returned, where each tuple contains a chromosome from the
        population and its associated fitness value.

        :param population: A list of chromosomes representing the population to be
            evaluated.
        :param assignment: Data defining the assignment structure used for fitness
            evaluation.
        :param teachers: A dictionary mapping teacher identifiers to corresponding
            TeacherModel instances.
        :param courses: A dictionary mapping course identifiers to corresponding
            CourseModel instances.
        :param periods: A dictionary mapping period identifiers to corresponding
            PeriodModel instances.
        :return: A list of tuples, where each tuple consists of a chromosome and its
            calculated fitness value.
        """
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
        """
        Evaluates the fitness of a given chromosome based on specific assignment, teacher, course, and period data.

        The function calculates a base score and adjusts it by evaluating constraints and penalties. These constraints
        include compatibility of teachers with courses, scheduling conflicts, and adherence to required teaching periods
        and classrooms. The final score reflects the chromosome's suitability while minimizing penalties.

        :param chromosome:
            List of genes where each gene represents an assignment of a course to a teacher, period, and classroom.

        :param assignment:
            Dictionary mapping teacher IDs to their assignments, detailing which courses they are allowed to teach.

        :param teachers:
            Dictionary with teacher IDs as keys and `TeacherModel` instances as values, which include teacher
            availability and other properties.

        :param courses:
            Dictionary with course IDs as keys and `CourseModel` instances as values, defining course-related
            attributes such as type, semester, or career.

        :param periods:
            Dictionary with period IDs as keys and `PeriodModel` instances as values providing data such as
            start time, end time, and other scheduling details.

        :return:
            The calculated fitness score as an integer, representing the suitability of the given chromosome
            based on the constraints and penalties applied.
        """
        base_score = len(chromosome) * 10
        fitness = 0
        penalty = 0

        teacher_schedule = defaultdict(set)
        classroom_schedule = defaultdict(set)
        required_courses = defaultdict(set)

        for gene in chromosome:
            course_id = gene["course_id"]
            teacher_id = gene["teacher_id"]
            period_id = int(gene["period_id"])
            classroom_id = int(gene["classroom_id"])

            course = courses.get(course_id)
            teacher = teachers.get(teacher_id)
            period = periods.get(str(period_id))

            if not course or not teacher or not period:
                penalty += 20
                continue

            # Teacher cant give the course
            can_teach = any(c.code == course_id for c in assignment.get(teacher_id, {}).get("courses", []))
            if not can_teach:
                penalty += 10

            # Teacher schedule is out of period
            if period.start_time < teacher.entry_time or period.end_time > teacher.departure_time:
                penalty += 5

            # Teacher is already in the period
            if period_id in teacher_schedule[teacher_id]:
                penalty += 15
            else:
                teacher_schedule[teacher_id].add(period_id)

            # Classroom is already in the period
            if period_id in classroom_schedule[classroom_id]:
                penalty += 15
            else:
                classroom_schedule[classroom_id].add(period_id)

            # Required course of the same semester and career is already in the period
            if course.id_course_type == 2:
                key = (course.id_career, course.id_semester)
                if period_id in required_courses[key]:
                    penalty += 10
                else:
                    required_courses[key].add(period_id)

        # Courses of the same career and semester are subsequent
        for (career, semester), periods_in_use in required_courses.items():
            sorted_periods = sorted(periods_in_use)
            for i in range(len(sorted_periods) - 1):
                if sorted_periods[i + 1] - sorted_periods[i] == 1:
                    fitness += 20

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
        """
        Selects individuals from a population using the tournament selection method, which
        chooses the best individual among randomly selected subsets of the population. The
        selection process emphasizes fitter individuals according to a fitness evaluation function.

        :param population: A list of individuals (chromosomes) representing potential solutions
            in the genetic algorithm's population.
        :param assignments: Data or mappings representing specific gene values or their assigned
            configurations in the genetic representation.
        :param teachers: A dictionary mapping teacher identifiers (keys) to corresponding
            TeacherModel instances (values).
        :param courses: A dictionary mapping course identifiers (keys) to corresponding
            CourseModel instances (values).
        :param periods: A dictionary mapping period identifiers (keys) to corresponding
            PeriodModel instances (values).
        :param tournament_size: Number of individuals randomly selected from the population for
            each tournament, from which the fittest individual is chosen.
        :return: A list containing the selected individuals (chromosomes) after applying the
            tournament selection strategy.
        """
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
        """
        Performs a one-point crossover operation on the given parent sequences to produce
        two offspring.

        A single crossover point is randomly selected, dividing each parent into two
        segments. The offspring are created by combining segments from each parent.

        :param parent1: The first parent sequence to participate in the one-point crossover.
        :param parent2: The second parent sequence to participate in the one-point crossover.
        :return: A tuple containing two offspring sequences resulting from the crossover
            operation.
        """
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def random_resetting_mutation(self, chromosome, teachers, periods, classrooms, mutation_rate=0.1):
        """
        Performs a random resetting mutation on a given chromosome. This method randomly
        selects genes in the chromosome based on the mutation rate and modifies their
        attributes to new random selections from the provided teachers, periods, and
        classrooms. This is useful in evolutionary algorithms for introducing variation
        into the population.

        :param chromosome: The chromosome to be mutated. A list of dictionaries where each
            dictionary represents a gene containing keys such as "course_id", "teacher_id",
            "period_id", and "classroom_id".
        :type chromosome: list[dict]

        :param teachers: A collection of teacher objects. Each teacher object should
            contain an `id` attribute that represents the teacher's identifier.
        :type teachers: list[object]

        :param periods: A collection of period objects to choose from for mutation. Each
            period object should represent a distinct scheduling period.
        :type periods: list[object]

        :param classrooms: A collection of classroom objects to choose from for mutation.
            Each classroom object should represent a distinct physical or virtual classroom.
        :type classrooms: list[object]

        :param mutation_rate: A float value representing the probability of mutating each
            gene in the chromosome. Default value is 0.1.
        :type mutation_rate: float, optional

        :return: A new mutated chromosome, structured as a list of dictionaries. Each
            dictionary represents a gene, potentially altered during the mutation process.
        :rtype: list[dict]
        """
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