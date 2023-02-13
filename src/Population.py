from Board import Board


class Population:

    def __init__(self, size_of_population: int, given_board: list):
        """
        Initialize a Population object and generates number of randomly filled boards
        and calculates their fitness scores.

        :param size_of_population: Number of Board objects in this population.
        :type size_of_population: int
        :param given_board: A 2-dimensional list that represents the initial state of the board.
        :type given_board: list of list of int
        :return: None
        :rtype: None
        """

        self.size_of_population = size_of_population
        self.candidates = list()

        print(f'Start generatinig population with size {self.size_of_population}')
        print('This may take a while, please be patient...')
        percentage = 1
        for counter in range(self.size_of_population):
            if counter == percentage * self.size_of_population // 10:
                print(f'{percentage * 10}% of all candidates are generated...')
                percentage += 1
            this_candidate = Board(given_board)
            this_candidate.fill_board()
            self.candidates.append(this_candidate)
        self.update_fitnesses()
        print(f'{self.size_of_population} boards were generated successfully')

    def update_fitnesses(self) -> None:
        """
        Update fitness scores for all candidates in the population.

        This function updates the fitness score of all candidates stored in the `self.candidates` list.
        The fitness score of each candidate is updated by calling the `update_fitness_score` method of the 
        `Board` class.
        """
        for candidate in self.candidates:
            candidate.update_fitness_score()

    def sort_based_on_fitness_score(self) -> None:
        """
        This method sorts the candidate boards based on their fitness scores in descending order.

        The boards with the highest fitness scores will be at the beginning of the list.
        """
        self.candidates = sorted(self.candidates, key=lambda item: item.fitness_score, reverse=True)
