from Board import Board

from random import uniform, randint
from copy import deepcopy


class CrossOver:

    def tournament_selection(self, candidates, selection_rate):
        """
        This function implements tournament selection algorithm to select a candidate from the given list of candidates.

        :param candidates: List of candidates to select from.
        :type candidates: list of objects
        :param selection_rate: Probability of selecting the fittest candidate.
        :type selection_rate: float

        :return: Selected candidate.
        :rtype: object
        """
        # Selects two random candidates
        first_candidate = candidates[randint(0, len(candidates) - 1)]
        second_candidate = candidates[randint(0, len(candidates) - 1)]
        first_fitness, second_fitness = first_candidate.fitness_score, second_candidate.fitness_score
        if first_fitness > second_fitness:
            fittest = first_candidate
            weakest = second_candidate
        else:
            fittest = second_candidate
            weakest = first_candidate
        # Returns one of them based on their fitness score and selection rate
        probability = uniform(0, 1)
        return fittest if probability < selection_rate else weakest
    
    def cross_over(self, parent_one, parent_two, cross_over_rate):
        """
        Perform a cross-over between two parents to generate two children.
        
        The function takes two parents, `parent_one` and `parent_two`, and a crossover rate, `cross_over_rate`, as input.
        Based on a random probability generated using `uniform` function, a cross-over is performed between the parents if the probability is less than `cross_over_rate`. 
        During the cross-over, two cut-off points are chosen randomly between 0 and 8, and 1 and 9. 
        The values of the children are merged based on these cut-off points using `__cross_over_rows` function for each row.
        
        :param parent_one: The first parent used in the cross-over.
        :type parent_one: Board
        :param parent_two: The second parent used in the cross-over.
        :type parent_two: Board
        :param cross_over_rate: The probability that the cross-over will occur between the two parents.
        :type cross_over_rate: float
        
        :return: The first and second children generated after cross-over.
        :rtype: tuple(Board, Board)
        """
        child_one, child_two = Board(parent_one.given_board), Board(parent_two.given_board)
        child_one.values = deepcopy(parent_one.values)
        child_two.values = deepcopy(parent_two.values)
        probability = uniform(0, 1)
        if probability < cross_over_rate:
            # Two cut off will be chosen to merge the parent between these two
            cross_over_point_one = randint(0, 8)
            cross_over_point_two = randint(1, 9)
            while cross_over_point_one == cross_over_point_two:
                cross_over_point_two = randint(1, 9)
            if cross_over_point_one > cross_over_point_two:
                cross_over_point_one, cross_over_point_two = \
                cross_over_point_two, cross_over_point_one
            # The merge will be done based on __cross_over_rows() function for each row
            for row_number in range(cross_over_point_one, cross_over_point_two):
                child_one.values[row_number], child_two.values[row_number] = \
                self.__cross_over_rows(child_one.values[row_number], child_two.values[row_number])
        return child_one, child_two
            
    def __cross_over_rows(self, row_one, row_two):
        """
        This function takes in two rows (row_one and row_two) as arguments and performs a crossover operation on these two rows to generate two child rows.
        The crossover operation uses two while loops, where each loop runs until both child_one_row and child_two_row are filled with numbers 1 to 9.

        In each iteration, the function finds the first number in the first parent row which is also in the remaining_numbers list.
        This first number is then added to the child_one_row and child_two_row based on the value of cycle_number, which is used to randomly shuffle the rows.
        If cycle_number is even, the first number from row_one is added to child_one_row and the corresponding number from row_two is added to child_two_row.
        If cycle_number is odd, the first number from row_one is added to child_two_row and the corresponding number from row_two is added to child_one_row.

        After adding the first number to the child rows, the function checks if the corresponding number in row_two is the same as the first number.
        If they are not the same, the function removes both numbers from the remaining_numbers list and repeats the process until they are the same.
        The function increments the cycle_number value after each iteration, which ensures that the crossover operation is performed randomly.

        Finally, the function returns the two child rows generated from the crossover operation.

        :param row_one: The first row used in the crossover operation
        :type row_one: list
        :param row_two: The second row used in the crossover operation
        :type row_two: list

        :return: A tuple of two child rows generated from the crossover operation
        :rtype: tuple(list, list)
        """
        child_one_row = [0 for _ in range(9)]
        child_two_row = [0 for _ in range(9)]
        remaining_numbers = [number for number in range(1, 10)]
        # This value will be used to mix two rows almost random
        cycle_number = 0
        # This while will be contined till both of childs are filled with numbers 1 to 9
        while 0 in child_one_row and 0 in child_two_row:
            # Find the first number in the first parent row which is in remaining_numbers, too
            # This means, this line find the first number which is not placed in the child list
            # Note that we use the index of this number
            index = self.__find_unused_number(row_one, remaining_numbers)
            first_number = row_one[index]
            # We want to use selected number in the child, hence, we cannot use it again.
            # So, we remove the number from remainin_numbers
            remaining_numbers.remove(first_number)
            # Based on the cycle_number value, we decide how to produce the child
            # If cycle number is even, we do the code below
            if cycle_number % 2 == 0:
                child_one_row[index], child_two_row[index] = row_one[index], row_two[index]
            # If the cycle_number is odd, we do the code below
            # Deciding based on cycle_number will help us to generate more rendom boards
            # And this can help us to solve the sudoku more quickly
            else:
                child_one_row[index], child_two_row[index] = row_two[index], row_one[index]
            # Note that we find the index of the first number which was available in the first row
            # This index in the second row does not necesserily have the same value
            # If they have the same value this means they are maybe given by the question
            # If they are not the same, we are sure that they are not the same
            # So we calculate this value in the second list, too
            next_numebr = row_two[index]
            # And while they are not the same, this means they are not given by the question
            # So, we can shuffle those. The code below, do this task
            # If they become the same as each other, the while loop will be broken
            while next_numebr != first_number:
                # Because previous numbers were not the same as each other, we have to remove
                # both numbers from remaining, and use both numbers in both children
                # Since we use first_number and next_number in just one child, we have to
                # find those numbers again, and use them once again, and after that, remove
                # the number from remaining_numbers
                index = self.__find_index(row_one, next_numebr)
                if cycle_number % 2 == 0:
                    child_one_row[index], child_two_row[index] = row_one[index], row_two[index]
                    remaining_numbers.remove(row_one[index])
                else:
                    child_one_row[index], child_two_row[index] = row_two[index], row_one[index]
                    remaining_numbers.remove(row_one[index])
                next_numebr = row_two[index]
            cycle_number += 1
        return child_one_row, child_two_row

    def __find_unused_number(self, parent_row, remaining_numbers):
        """
        Find the first unused number in `parent_row`.

        This function loops through `parent_row` and returns the index of the first number
        that is also found in the `remaining_numbers` list. If no such number is found,
        the function returns `None`.

        :param parent_row: A list of numbers representing a single row in the parent's solution.
        :type parent_row: list
        :param remaining_numbers: A list of numbers representing the remaining numbers that have not been used in the child solution yet.
        :type remaining_numbers: list
            
        :return: The index of the first unused number in `parent_row`, or `None` if no such number is found.
        :rtype: int or None            
        """
        for index, number in enumerate(parent_row):
            if number in remaining_numbers:
                return index

    def __find_index(self, parent_row, value):
        """
        Find the index of a value in a parent row.

        :param parent_row: A list containing the values in a parent row.
        :type parent_row: list
        :param value: A list containing the values in a parent row.
        :type value: int
            
        :return: A list containing the values in a parent row.
        :rtype: int or None            
        """
        for index, number in enumerate(parent_row):
            if number == value:
                return index
