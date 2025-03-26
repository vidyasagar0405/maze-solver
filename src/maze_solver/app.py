from time import perf_counter
from maze_solver.graphics import Window
from maze_solver.maze import Maze
import sys


def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    sys.setrecursionlimit(10000)

    win = Window(screen_x, screen_y)
    # win = Window()
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    print("maze created")
    start = perf_counter()
    is_solvable = maze.solve()
    end = perf_counter()
    if not is_solvable:
        print("Maze can not be solved!")
    else:
        print(f"Maze solved! in {end - start} seconds")
    win.wait_for_close()


if __name__ == "__main__":
    main()
