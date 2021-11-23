""" $LAN=Python """

from tkinter import *
from tkinter import ttk

import file_progress as fp


class sc:
    def __init__(self) -> None:
        # main window
        self.root = Tk()
        self.root.title("Voronoi Algorithm")

        # main frame
        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0)

        # main canvas
        self.canvas = Canvas(self.mainframe, width=600, height=600, background="white")
        self.canvas.bind("<Button-1>", self.mouse_click_event)
        self.canvas.grid(column=0, row=0)

        # frame of buttons
        self.sideframe = ttk.Frame(self.root, padding="0 10 10 10")
        self.sideframe.grid(column=1, row=0)
        self._init_sideframe_elements()
        self.init_sideframe_layout()

        # record points
        self.points = []

    # initialize labels and buttons in sideframe
    def _init_sideframe_elements(self):
        self.file_path = StringVar()
        self.file_name_lb = ttk.Label(self.sideframe, textvariable=self.file_path)
        self.read_file_btn = ttk.Button(self.sideframe, width=16, text="read file", command=lambda: fp.open_in_file(self.file_path))
        self.next_set_btn = ttk.Button(self.sideframe, width=16, text="next set", command=None)  # TODO : commands
        self.step_by_step_btn = ttk.Button(self.sideframe, width=16, text="step by step", command=None)  # TODO : commands
        self.run_btn = ttk.Button(self.sideframe, width=16, text="run", command=None)  # TODO : commands
        self.write_graph_file_btn = ttk.Button(self.sideframe, width=16, text="save image", command=lambda: fp.save_vd_file())
        self.read_graph_file_btn = ttk.Button(self.sideframe, width=16, text="read image", command=lambda: fp.open_vd_file())
        self.clear_canvas_btn = ttk.Button(self.sideframe, width=16, text="clear canvas", command=self.clean_canvas)

    # initialize sideframe layout
    def init_sideframe_layout(self):
        self.file_name_lb.grid(row=0)
        self.read_file_btn.grid(row=1)
        self.next_set_btn.grid(row=2)
        self.step_by_step_btn.grid(row=3)
        self.run_btn.grid(row=4)
        self.write_graph_file_btn.grid(row=5)
        self.read_graph_file_btn.grid(row=6)
        self.clear_canvas_btn.grid(row=7)

    def mainloop(self):
        self.root.mainloop()

    def clean_canvas(self):
        self.canvas.delete("all")

    def mouse_click_event(self, event):
        self.points.append((event.x, event.y))
        self.print_point(event.x, event.y)
        print(f"click at ({event.x}, {event.y})")

    def print_point(self, x, y, r=3):
        self.canvas.create_oval(x - r, y - r, x + r, y + r)


if __name__ == "__main__":
    main_sc = sc()
    main_sc.print_point(-10, -10)
    main_sc.mainloop()


# test
# main_canvas.create_line(10, 5, 200, 50)
# main_canvas.create_oval(30, 30, 100, 100)
