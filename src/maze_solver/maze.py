from time import sleep
from maze_solver.cell import Cell
from maze_solver.graphics import Window
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win: Window | None = None,
        seed=None,
    ) -> None:
        self._cells: list[list[Cell]] = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win: Window | None = win

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        for col in range(self._num_cols):
            col_cells = []
            for row in range(self._num_rows):
                cell = Cell(self._win)
                col_cells.append(cell)
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j) -> None:
        if self._win is None:
            return

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self, animate: bool = True) -> None:
        if self._win is None:
            return

        self._win.redraw()
        if animate:
            sleep(0.01)

    def _break_entrance_and_exit(self) -> None:
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j) -> None:
        # depth-first traversal algorithm

        # Mark the current cell as visited
        self._cells[i][j].visited = True

        # In an infinite loop:
        while True:
            # Create a new empty list to hold the i and j values you will need to visit
            adjacent_cells = []

            # Check the cells that are directly adjacent to the current cell. Keep track of any that have not been visited as "possible directions" to move to
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                adjacent_cells.append((i, j - 1))

            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                adjacent_cells.append((i + 1, j))

            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                adjacent_cells.append((i, j + 1))

            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                adjacent_cells.append((i - 1, j))

            # If there are zero directions you can go from the current cell, then draw the current cell and return to break out of the loop
            if not adjacent_cells:
                self._draw_cell(i, j)
                return

            # Otherwise, pick a random direction.
            else:
                direction = random.randrange(len(adjacent_cells))
                next_cell = adjacent_cells[direction]

            # Knock down the walls between the current cell and the chosen cell.
            # up
            if next_cell[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            # right
            if next_cell[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # down
            if next_cell[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # left
            if next_cell[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False

            # Move to the chosen cell by recursively calling _break_walls_r
            self._break_walls_r(next_cell[0], next_cell[1])

    def _reset_cells_visited(self) -> None:
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def _solve_r(self, i, j) -> bool:
        """
        uses depth-first algorithm to solve the maze
        The _solve_r method returns True if the current cell is an end cell, OR if it leads to the end cell.
        It returns False if the current cell is a loser cell.
        """

        # Call the _animate method.
        self._animate()

        # Mark the current cell as visited
        self._cells[i][j].visited = True

        # If you are at the "end" cell (the goal) then return True.
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # For each direction:
        # If there is a cell in that direction, there is no wall blocking you, and that cell hasn't been visited:
        # Draw a move between the current cell and that cell
        # Call _solve_r recursively to move to that cell. If that cell returns True, then just return True and don't worry about the other directions.
        # Otherwise, draw an "undo" move between the current cell and the next cell
        # If none of the directions worked out, return False.

        # up
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # right
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # down
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # left
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        return False

    def solve(self) -> bool:
        return self._solve_r(0, 0)
