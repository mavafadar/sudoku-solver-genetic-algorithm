from Population import Population
from CrossOver import CrossOver


class Sudoku:

    def __init__(self, given_board: list):
        """
        Initialize the Genetic Algorithm.

        :param given_board: A NxN 2D list representing the Sudoku problem.
        :type given_board: list
        """
        self.given_board = given_board
        self.population = None
        self.cross_over = CrossOver()

    def solve_sudokue(self):
        """
        This function solves the sudoku puzzle using a genetic algorithm.

        :param self: an instance of the class that the function is defined in
        :return: the candidate solution that has the best fitness score, if a solution is found, or None if no solution is found
        """
        number_of_candidates = 1000
        number_of_generations = 1000
        mutation_rate = 0.06
        selection_rate = 0.85
        cross_over_rate = 0.85
        # Generate a population of candidate answers
        self.population = Population(number_of_candidates, self.given_board)
        for generation_number in range(number_of_generations):
            print(f'Generation #{generation_number} is started...')
            # Here we find the best fitness score of current population
            # and fitness score 1 means that we have found the answer so we return it
            best_fitness_score = 0.0
            for candidate in self.population.candidates:
                if best_fitness_score < candidate.fitness_score:
                    best_fitness_score = candidate.fitness_score
                if best_fitness_score == 1:
                    print(f'Solution is found..')
                    return candidate
            print(f'Best fitness score now is {best_fitness_score}...')
            # If we pass previous code, means that we did not find the answer
            # So we are going to generate next generation
            new_generation = list()
            # Firstly, we are going to do the cross over to generate new offsprings and complete the population
            # And after that mutation each of which
            for _ in range(0, number_of_candidates, 2):
                # Here, two offsprings will be generated
                parent_one = self.cross_over.tournament_selection(self.population.candidates, selection_rate)
                parent_two = self.cross_over.tournament_selection(self.population.candidates, selection_rate)
                child_one, child_two = self.cross_over.cross_over(parent_one, parent_two, cross_over_rate)
                # Here, they will be mutated
                child_one.mutate(mutation_rate)
                child_two.mutate(mutation_rate)
                # And finally they will be added to the next generation
                new_generation.append(child_one)
                new_generation.append(child_two)
            # Finalize new population
            self.population.candidates = new_generation
            self.population.update_fitnesses()
        
        print('Unfortunately, no solution found...')
