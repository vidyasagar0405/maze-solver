from tkinter import Tk, BOTH, Canvas, Label


class Point:
    def __init__(self, pos_x: int, pos_y: int) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y


class Line:
    def __init__(self, point_1: Point, point_2: Point) -> None:
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(
            self.point_1.pos_x,
            self.point_1.pos_y,
            self.point_2.pos_x,
            self.point_2.pos_y,
            fill=fill_color,
            width=2,
        )


class Window:
    def __init__(self, width: int | None = None, height: int | None = None) -> None:


        self.__root: Tk = Tk(className="Maze-solver")
        self.__root.title("Maze-solver")

        if width is None:
            width = int(self.__root.winfo_screenwidth() * 0.9)

        if height is None:
            height = int(self.__root.winfo_height() * 0.9)

        # Create a label
        self.__label: Label = Label(
            self.__root, text="Maze Solver", font=("Roboto", 14), fg="black"
        )
        self.__label.pack(pady=5)

        self.__canvas: Canvas = Canvas(
            self.__root, bg="white", width=width, height=height
        )
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line: Line, fill_color: str = "black") -> None:
        line.draw(self.__canvas, fill_color)

    def close(self) -> None:
        self.__running = False
