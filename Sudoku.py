from random import choice
from copy import deepcopy
from time import time


class Board:
    def __init__(self):
        self.board = [[0 for col in range(9)] for row in range(9)]
        self.progress_board = deepcopy(self.board)
        self.progress_coords = list()

    def check_position(self, board, row, col, n):
        """Returns True if n is not present in the current board's row, col and 3x3 square."""

        def check_row():
            return False if n in board[row] else True

        def check_column():
            return False if n in [board[i][col] for i in range(9)] else True

        def check_square():
            row_range = row - row % 3
            col_range = col - col % 3

            for i in range(3):
                for j in range(3):
                    if n == board[i + row_range][j + col_range]:
                        return False
            return True

        return check_row() and check_column() and check_square()

    def get_free_position(self):
        """Returns the next free position on the board."""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return False

    def generate_coords(self, n=15):
        numbers = set()

        while len(numbers) < n:
            numbers.add(choice(range(81)))

        return [(x // 9, x % 9) for x in numbers]

    def fill_coords(self, coords):
        """Fills coords with random numbers(1-9) with check_position() == True."""
        for coord in coords:
            row, col = coord

            num = choice(range(1, 10))

            while not self.check_position(self.board, row, col, num):
                num = choice(range(1, 10))

            self.board[row][col] = num

    def solution(self, endtime):
        """Backtracking algorithm which solves a Sudoku board.
        Checks for a free position.
        Checks that position for numbers (1-9).
        Calls another recursive call for each number which suits that position.
        When it reaches a point, where there is no suitable number for that position,
        resets it to 0 and all other positions used so far in the recursive call.
        If there are no free positions left the solution is successful.
        """

        # Timeout for the recursive call.
        if time() > endtime:
            # If the endtime is passed, the board is nulled and the generation is reset.
            self.board = deepcopy(self.progress_board)
            self.generate_board()

        if self.get_free_position() == False:
            # If there is no free position left, the function returns True
            return True

        row, col = self.get_free_position()

        for i in range(1, 10):
            if self.check_position(self.board, row, col, i) == True:
                self.board[row][col] = i

                if self.solution(endtime):
                    return True
                # Resets the coord used in the recursive process if there is a False return.
                self.board[row][col] = 0

        return False

    def generate_board(self):
        """Generates board with 15 random coords with numbers on them.
        Fires a solution on that board with a timeout of 5 seconds.
        """

        coords = self.generate_coords()
        self.fill_coords(coords)
        self.solution(time() + 5)
        print("done")


board = Board()
board.generate_board()
