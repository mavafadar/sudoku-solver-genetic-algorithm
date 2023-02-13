import tkinter as tk
from tkinter import ttk

from Sudoku import Sudoku


class UserInterface:
    def __init__(self, master):
        """
        The `__init__` method initializes the sudoku solver GUI.

        :ivar master: The main window of the GUI.
        :ivar grid: A 9x9 grid of Entry widgets representing the sudoku puzzle.
        :ivar solve_button: A button to trigger the solution of the puzzle.
        :ivar clear_button: A button to clear the puzzle.
        :ivar wait_label: A label to display waiting messages.
        """
        self.master = master
        master.title('Sudoku Solver')
        master.configure(bg='#5c6bc0')
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for column in range(9):
                entry = ttk.Entry(master, width=2, font=("Helvetica", 16), justify='center')
                entry.grid(row=row, column=column, padx=5, pady=5)
                entry.bind("<FocusOut>", lambda event, i=row, j=column: self.update_grid(event, i, j))
                self.grid[row][column] = entry
        self.solve_button = ttk.Button(master, text='Solve', style='Green.TButton', command=self.solve)
        self.solve_button.grid(row=9, column=0, columnspan=5, sticky="WE", pady=10)
        self.clear_button = ttk.Button(master, text='Clear', style='Red.TButton', command=self.clear)
        self.clear_button.grid(row=9, column=5, columnspan=4, sticky="WE", pady=10)
        self.wait_label = ttk.Label(master, text="Please wait while the puzzle is being solved...",
                                    font=("Helvetica", 14), foreground='#5c6bc0')
        self.wait_label.grid(row=10, column=0, columnspan=9, pady=10, padx=10, sticky="W")
        self.wait_label.config(text="")
        sample_grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.set_grid(sample_grid)

    def update_grid(self, event, row: int, column: int):
        """
       Update the grid with the value entered by the user.

       This function is called when the user focuses out of an entry widget in the grid.
       It checks if the entered value is a digit between 1 and 9, and if so, sets the state of
       the entry widget to "readonly" and sets its style to "Yellow.TEntry". If the entered value is
       not a digit between 1 and 9, it is cleared from the entry widget.

       :param event: The event that triggers the function call.
       :type event: tkinter event
       :param row: The row index of the grid where the entry widget is located.
       :type row: int
       :param column: The column index of the grid where the entry widget is located.
       :type column: int

       :return: None
       """
        value = event.widget.get()
        if value.isdigit() and 1 <= int(value) <= 9:
            self.grid[row][column].configure(state="readonly", style='Yellow.TEntry')
            self.grid[row][column].delete(0, tk.END)
            self.grid[row][column].insert(0, value)
        else:
            self.grid[row][column].delete(0, tk.END)

    def clear(self):
        """
        This function is used to clear all the entries in the sudoku puzzle grid.

        :return: None
        """
        for i in range(9):
            for j in range(9):
                self.grid[i][j].configure(state="normal", style='TEntry')
                self.grid[i][j].delete(0, tk.END)

    def get_grid(self) -> list:
        """
        Get the current state of the grid.

        :return: A 9x9 2D list representing the current state of the grid, where each cell
                                contains an integer from 1 to 9 or 0 if the cell is empty.
        :rtype: list[list[int]]
        """
        grid = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for column in range(9):
                value = self.grid[row][column].get()
                if value:
                    grid[row][column] = int(value)
        return grid

    def set_grid(self, grid: list):
        """
        This function sets the values of the grid.

        :param grid: A two dimensional list of integers representing the sudoku puzzle.
        :type grid: list[list[int]]

        :return: None
        """
        for row in range(9):
            for column in range(9):
                if grid[row][column] != 0:
                    self.grid[row][column].configure(style='Yellow.TEntry')
                    self.grid[row][column].delete(0, tk.END)
                    self.grid[row][column].insert(0, grid[row][column])

    def solve(self):
        """
        This method is used to solve the sudoku puzzle. It sets a label to display
        "Please wait while the puzzle is being solved..." while the puzzle is being solved and
        then updates the label with an empty string. Then it retrieves the grid using `get_grid` method,
        initializes a `Sudoku` object using the grid and solves the puzzle using the `solve_sudoku` method. Finally,
        it sets the grid using the `set_grid` method and updates the label again with an empty string.

        :return: None
        """
        self.wait_label.config(text="Please wait while the puzzle is being solved...")
        self.master.update()
        self.wait_label.config(text="")
        grid = self.get_grid()
        sudoku_solver = Sudoku(grid)
        result = sudoku_solver.solve_sudoku()
        self.set_grid(result.values)
        self.wait_label.configure(text="")
        self.master.update()
