from random import uniform, randint, shuffle
from copy import deepcopy

class Board:

    def __init__(self, values: list):
        """
        Initialize a new instance of the class.

        :param values: A list of values representing the sudoku board.
        :type values: list
        :ivar values: A deep copy of the `values` input parameter.
        :ivar given_board: A reference to the original `values` input parameter.
        :ivar fitness_score: The fitness score of the sudoku board, initially set to None.
        """
        self.values = deepcopy(values)
        self.given_board = values
        self.fitness_score = None

    def __str__(self) -> str:
        """
        Return a string representation of the sudoku board.

        :return: A string representation of the sudoku board, with each row separated by horizontal lines and each cell separated by vertical lines.
        :rtype: str
        """
        final_message = str()
        for _ in range(9):
            final_message += ' ---'
        final_message += '\n'
        for row in self.values:
            final_message += '|'
            for number in row:
                final_message += f' {number} |'
            final_message += '\n'
            for _ in range(9):
                final_message += ' ---'
            final_message += '\n'
        return final_message

    def check_duplication_for_generation(self, row: int, column: int, value: int) -> bool:
        """
        Check if a given value is a valid entry for a given position on the sudoku board.

        :param row: The row index of the position to be checked.
        :type row: int
        :param column: The column index of the position to be checked.
        :type column: int
        :param value: The value to be checked for validity.
        :type value: int
        :return: True if the value is a valid entry for the given position, False otherwise.
        :rtype: bool
        """
        if self.given_board[row][column] != 0:
            return False
        if self.check_column_duplication(column, value) is True:
            return False
        if self.check_row_duplication(row, value) is True:
            return False
        if self.check_subgrid_duplicatoin(row, column, value) is True:
            return False
        return True

    def fill_board(self) -> None:
        """
        Fill the sudoku board with valid values.

        This function first generates a helper board with possible answers for each cell of the sudoku board.
        It then uses the `check_duplication_for_generation` function to validate the answers and fill the sudoku board.
        If a cell has already been given a value in the question, it will not be changed.
        Otherwise, the cell will be filled with a random valid value from the helper board.
        The function checks if the filled row has duplicate values, and if so, refills the row with new values.
        """
        # This list has possible answers for each cell of the sudoku
        helper_board = Board([[list() for _ in range(9)] for _ in range(9)])
        # This piece of code, generate possible numbers for each cell
        for row in range(9):
            for column in range(9):
                for value in range(1, 10):
                    if self.check_duplication_for_generation(row, column, value):
                        helper_board.values[row][column].append(value)
                    elif self.given_board[row][column] != 0:
                        helper_board.values[row][column].append(self.given_board[row][column])
                        break
        # This piece of code fills the sudoku table
        for row in range(9):
            this_row = [0 for _ in range(9)]
            for column in range(9):
                # This means this cell is filled by the question
                if self.given_board[row][column] != 0:
                    this_row[column] = self.given_board[row][column]
                # This means this cell has to be filled randomly
                elif self.given_board[row][column] == 0:
                    this_row[column] = \
                    helper_board.values[row][column][randint(0, len(helper_board.values[row][column]) - 1)]
            # This means this row has duplicat numebrs      
            while len(set(this_row)) != 9:
                for column in range(9):
                    # We change the numbers those are not given by the question, since we have an acceptable answer
                    if self.given_board[row][column] == 0:
                        this_row[column] = \
                        helper_board.values[row][column][randint(0, len(helper_board.values[row][column]) - 1)]
            self.values[row] = this_row

    def check_row_duplication(self, row: int, value: int) -> bool:
        """
        Check if a `value` is already present in a `row` of the board.

        :param row: Check if a `value` is already present in a `row` of the board.
        :type row: int
        :param value: Check if a `value` is already present in a `row` of the board.
        :type value: int
        :return: True if the `value` is already present in the `row`, False otherwise.
        :rtype: bool
        """
        return True if value in self.given_board[row] else False

    def check_column_duplication(self, column: int, value: int) -> bool:
        """
        Check if a `value` is already present in a `column` of the board.

        :param column: Check if a `value` is already present in a `column` of the board.
        :type row: int
        :param value: Check if a `value` is already present in a `column` of the board.
        :type value: int
        :return: True if the `value` is already present in the `column`, False otherwise.
        :rtype: bool
        """
        return True if value in [self.given_board[row][column] for row in range(9)] else False

    def check_subgrid_duplicatoin(self, row: int, column: int, value: int) -> bool:
        """
        This function checks if the value being checked is already present in the subgrid in which the current cell belongs.

        :param row: Row number of the cell.
        :type row: int
        :param column: Column number of the cell.
        :type column: int
        :param value: Value to be checked for duplication.
        :type value: int
        :return: Returns `True` if the value is already present in the subgrid, otherwise `False`.
        :rtype: bool
        """
        subgrid_row, subgrid_column = row // 3 * 3, column // 3 * 3
        subgrid_values = [self.given_board[subgrid_row + row][subgrid_column + column] for row in range(3) for column in range(3)]
        return True if value in subgrid_values else False

    def __calculate_column_fitness_score(self) -> float:
        """
        Calculate the fitness score for columns of the sudoku grid.

        :return: Calculate the fitness score for columns of the sudoku grid.
        :rtype: float
        """
        column_sum = 0
        for column in range(9):
            column_count = [0 for _ in range(9)]
            for row in range(9):
                column_count[self.values[row][column] - 1] += 1
            column_sum += (1.0 / len(set(column_count))) / 9
        return column_sum

    def __calculate_subgrid_fitness_score(self) -> float:
        """
        This function calculates the fitness score of the subgrid in the sudoku board.
    
        :return: The fitness score of the subgrid.
        :rtype: float
        """
        subgrid_sum = 0
        for subgrid in range(9):
            subgrid_count = [0 for _ in range(9)]
            for row in range(3):
                for column in range(3):
                    subgrid_count[self.values[subgrid // 3 * 3 + row][subgrid % 3 * 3 + column] - 1] += 1
            subgrid_sum += (1.0 / len(set(subgrid_count))) / 9
        return subgrid_sum
            
    def update_fitness_score(self) -> None:
        """
        This function updates the fitness score of the sudoku board.
        The fitness score is calculated as the product of column fitness score and subgrid fitness score.
        If either the column fitness score or subgrid fitness score is 1, the fitness score is set to 1,
        indicating that the board is a valid solution.
        """
        column_fitness_score = self.__calculate_column_fitness_score()
        subgrid_fitness_score = self.__calculate_subgrid_fitness_score()
        if int(column_fitness_score) == 1 and int(subgrid_fitness_score) == 1:
            self.fitness_score = 1
        else:
            self.fitness_score = column_fitness_score * subgrid_fitness_score

    def __check_duplication_for_mutation(self, row: int, from_column: int, to_column: int) -> bool:
        """
        Check duplication of values before mutation.

        This function checks if there are any duplicates in the specified row,
        in both the column where the value is being moved from and the column
        where the value is being moved to. It also checks for duplicates in the
        subgrid that contains the row and columns being checked.

        :param row: The row of the value being checked.
        :type row: int
        :param from_column: The column where the value is being moved from.
        :type from_column: int
        :param to_column: The column where the value is being moved to.
        :type to_column: int
        :return:
        :rtype: bool
        """
        if self.check_column_duplication(from_column, self.values[row][to_column]) is True:
            return False
        if self.check_column_duplication(to_column, self.values[row][to_column]) is True:
            return False
        if self.check_subgrid_duplicatoin(row, from_column, self.values[row][from_column]) is True:
            return False
        if self.check_subgrid_duplicatoin(row, to_column, self.values[row][to_column]) is True:
            return False
        return True

    def mutate(self, mutation_rate: float) -> None:
        """
        Mutates the sudoku board.

        :param mutation_rate: The mutation rate, a float value between 0 and 1, which determines the probability of mutation happening.
        :type mutation_rate: float
        :return: None
        """
        probablity = uniform(0, 1)
        was_it_successful = False
        if probablity < mutation_rate:
            # Generate random numbers till a mutation happens
            while not was_it_successful:
                selected_row, from_column, to_column = randint(0, 8), randint(0, 8), randint(0, 8)
                while from_column == to_column:
                    to_column = randint(0, 8)
                # This if checks whether this cell has been given or not
                if self.given_board[selected_row][from_column] == 0 and self.given_board[selected_row][to_column] == 0:
                    # This if checks after mutation, whether duplication will be caused
                    if self.__check_duplication_for_mutation(selected_row, from_column, to_column):
                        self.values[selected_row][to_column], self.values[selected_row][from_column] = \
                        self.values[selected_row][from_column], self.values[selected_row][to_column]
                        was_it_successful = True
