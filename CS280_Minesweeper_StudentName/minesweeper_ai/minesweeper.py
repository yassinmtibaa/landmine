"""
Minesweeper Game Environment
Implements the game board, mine placement, and move validation.
"""

import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        """
        Initialize game board with given dimensions and number of mines.
        
        Args:
            height: Number of rows
            width: Number of columns
            mines: Number of mines to place
        """
        # Set initial dimensions
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize empty board (all False)
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) < mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # Track cells that have been revealed
        self.mines_found = set()

    def print(self):
        """
        Print a text-based representation of the board (for debugging).
        Shows mines as 'X' and safe cells as numbers or '.'
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        """
        Check if a cell contains a mine.
        
        Args:
            cell: Tuple (i, j) representing cell coordinates
            
        Returns:
            True if cell contains a mine, False otherwise
        """
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Count the number of mines in adjacent cells (including diagonals).
        
        Args:
            cell: Tuple (i, j) representing cell coordinates
            
        Returns:
            Integer count of nearby mines (0-8)
        """
        count = 0

        # Check all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Check if cell is valid and contains a mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Check if all mines have been correctly identified.
        
        Returns:
            True if game is won, False otherwise
        """
        return self.mines_found == self.mines
