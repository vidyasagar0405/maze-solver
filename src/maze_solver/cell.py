from typing import Self
from maze_solver.graphics import Point, Window, Line


class Cell:
    def __init__(self, win: Window) -> None:
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self._x1: int | None = None
        self._x2: int | None = None
        self._y1: int | None = None
        self._y2: int | None = None
        self._win: Window = win
        self.visited: bool = False

    def draw(self, x1: int, y1: int, x2: int, y2: int) -> None:
        if self._win is None:
            return

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        if self.has_left_wall:
            self._win.draw_line(
                Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            )
        else:
            self._win.draw_line(
                Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
                fill_color="white",
            )
        if self.has_right_wall:
            self._win.draw_line(
                Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            )
        else:
            self._win.draw_line(
                Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
                fill_color="white",
            )
        if self.has_top_wall:
            self._win.draw_line(
                Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            )
        else:
            self._win.draw_line(
                Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
                fill_color="white",
            )
        if self.has_bottom_wall:
            self._win.draw_line(
                Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            )
        else:
            self._win.draw_line(
                Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
                fill_color="white",
            )

    def draw_move(self, to_cell: Self, undo: bool = False):
        fill_color = "green"
        if undo:
            fill_color = "red"

        # Get mid point
        assert self._x1 and self._y1 and self._x2 and self._y2 is not None, (
            "Value cannot be None"
        )
        self_half: int = abs((self._x2 - self._x1) // 2)
        self_x_center: int = self_half + self._x1
        self_y_center: int = self_half + self._y1

        assert (
            to_cell._x1 and to_cell._y1 and to_cell._x2 and to_cell._y2 is not None
        ), "Value cannot be None"

        to_half: int = abs((to_cell._x2 - to_cell._x1) // 2)
        to_x_center: int = to_half + to_cell._x1
        to_y_center: int = to_half + to_cell._y1

        self_mid_point = Point(self_x_center, self_y_center)
        to_mid_point = Point(to_x_center, to_y_center)

        line = Line(self_mid_point, to_mid_point)

        self._win.draw_line(line, fill_color=fill_color)
