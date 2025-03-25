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
        seed = None,
    ) -> None:
        self._cells: list[list[Cell]] = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win: Window | None = win

        self.seed = seed
        if self.seed is None:
            self.seed = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()

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
        self._animate(False)

    def _animate(self, animate: bool = True) -> None:
        if self._win is None:
            return

        self._win.redraw()
        if animate:
            sleep(0.05)

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

        # Create a new empty list to hold the i and j values you will need to visit
        cells_to_be_visited = []

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                cells_to_be_visited.append([i, j])

                if not self._cells[i][j].visited:
                    ...


        # Check the cells that are directly adjacent to the current cell. Keep track of any that have not been visited as "possible directions" to move to
        # If there are zero directions you can go from the current cell, then draw the current cell and return to break out of the loop
        # Otherwise, pick a random direction.
        # Knock down the walls between the current cell and the chosen cell.
        # Move to the chosen cell by recursively calling _break_walls_r
