""" $LAN=Python """

from tkinter import *
from tkinter import ttk
from fractions import Fraction

import file_process as fp
from tools import *


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
        self.canvas.bind("<Button-1>", self.canvas_mouse_click_event)
        self.canvas.grid(column=0, row=0)

        # frame including buttons
        self.sideframe = ttk.Frame(self.root, padding="0 10 10 10")
        self.sideframe.grid(column=1, row=0)
        self.init_sideframe_elements()
        self.init_sideframe_layout()

        # store all points and lines to show
        self.graph_contents = {"points": [], "lines": []}
        # store point data read from file
        self.dataset = []
        self.dataset_idx = -1

        self.steps = -1
        self.solutions = []
        self.step_status = 0  # 0: CH, 1: merge CH, 2: 中垂線, 3: merge 中垂線

    #################### core functions ####################
    def init_sideframe_elements(self):
        self.file_path = StringVar()
        self.file_name_lb = ttk.Label(self.sideframe, textvariable=self.file_path)
        self.load_file_btn = ttk.Button(self.sideframe, width=16, text="load file", command=self.read_dataset)
        self.show_next_set_btn = ttk.Button(self.sideframe, width=16, text="next set", command=self.show_next_set)
        self.step_by_step_btn = ttk.Button(self.sideframe, width=16, text="step by step", command=self.step_by_step)  # TODO : commands
        self.run_btn = ttk.Button(self.sideframe, width=16, text="run", command=self.do_voronoi)
        self.save_graph_file_btn = ttk.Button(self.sideframe, width=16, text="save image", command=self.save_graph)
        self.load_graph_file_btn = ttk.Button(self.sideframe, width=16, text="load image", command=self.load_graph)
        self.clear_canvas_btn = ttk.Button(self.sideframe, width=16, text="clear canvas", command=self.clean)

    def init_sideframe_layout(self):
        self.file_name_lb.grid(row=0)
        self.load_file_btn.grid(row=1)
        self.show_next_set_btn.grid(row=2)
        self.run_btn.grid(row=3)
        self.step_by_step_btn.grid(row=4)
        self.save_graph_file_btn.grid(row=5)
        self.load_graph_file_btn.grid(row=6)
        self.clear_canvas_btn.grid(row=7)

    def canvas_mouse_click_event(self, event):
        self.steps = -1
        self.graph_contents["points"].append((event.x, event.y))
        self.print_point(event.x, event.y)

    def mainloop(self):
        self.root.mainloop()

    #################### file processing ####################
    def read_dataset(self):
        self.dataset = fp.load_dataset(self.file_path)
        self.dataset_idx = -1

    def save_graph(self):
        self.graph_contents["points"].sort()
        self.graph_contents["lines"].sort()
        fp.save_vd_graph(self.graph_contents)

    def load_graph(self):
        self.clear_contents()
        self.clean_canvas()
        self.graph_contents = fp.open_vd_graph()
        self.print_graph(self.graph_contents)

    ####################### draw graph ######################
    def clean_canvas(self):
        self.canvas.delete("all")

    def print_point(self, x: int, y: int, r: int = 3, fill="white", outline="black"):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline=outline)

    def print_line(self, x1: int, y1: int, x2: int, y2: int, fill="black"):
        self.canvas.create_line(x1, y1, x2, y2, fill=fill)

    def print_graph(self, content: dict):

        points = content["points"]
        lines = content["lines"]

        for x, y in points:
            self.print_point(x, y)

        for x1, y1, x2, y2 in lines:
            self.print_line(x1, y1, x2, y2)

    ######################## others ########################
    def clean(self):
        self.steps = -1
        self.clean_canvas()
        self.clear_contents()

    def clear_contents(self):
        self.graph_contents = {"points": [], "lines": []}

    def show_next_set(self):
        self.steps = -1
        self.dataset_idx += 1
        if self.dataset_idx < len(self.dataset):
            self.graph_contents = self.dataset[self.dataset_idx]
            self.clean_canvas()
            self.print_graph(self.graph_contents)
        else:
            self.dataset_idx = -1
            self.clean_canvas()
            self.clear_contents()

    def do_voronoi(self):
        pass

    def step_by_step(self):
        pass


if __name__ == "__main__":
    main_sc = sc()

    main_sc.mainloop()
