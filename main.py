""" $LAN=Python """

from tkinter import *
from tkinter import ttk
from fractions import Fraction

import file_process as fp
import vd_algo
from vd_algo import Point, Graph


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

        # store all points and lines on screen
        self.current_graph = Graph(points=[], lines=[])
        # store point data read from file
        self.dataset = []
        self.dataset_idx = 0

        # store every step of doing voronoi diagram by divide and conquer methods
        self.solution_steps = []
        self.steps_idx = 0

    #################### core functions ####################
    def init_sideframe_elements(self):
        self.dataset_idx_str = StringVar()
        self.dataset_idx_lb = ttk.Label(self.sideframe, textvariable=self.dataset_idx_str)
        self.load_file_btn = ttk.Button(self.sideframe, width=16, text="load dataset", command=self.read_dataset)
        self.show_next_set_btn = ttk.Button(self.sideframe, width=16, text="next set", command=self.show_next_set)
        self.step_by_step_btn = ttk.Button(self.sideframe, width=16, text="step by step", command=self.step_by_step)
        self.run_btn = ttk.Button(self.sideframe, width=16, text="run", command=self.do_voronoi)
        self.save_graph_file_btn = ttk.Button(self.sideframe, width=16, text="save graph", command=self.save_graph)
        self.load_graph_file_btn = ttk.Button(self.sideframe, width=16, text="load graph", command=self.load_graph)
        self.clear_canvas_btn = ttk.Button(self.sideframe, width=16, text="clear canvas", command=self.clean_all)

    def init_sideframe_layout(self):
        self.dataset_idx_lb.grid(row=0)
        self.load_file_btn.grid(row=1)
        self.show_next_set_btn.grid(row=2)
        self.run_btn.grid(row=3)
        self.step_by_step_btn.grid(row=4)
        self.save_graph_file_btn.grid(row=5)
        self.load_graph_file_btn.grid(row=6)
        self.clear_canvas_btn.grid(row=7)

    def canvas_mouse_click_event(self, event):
        p_tmp = Point(event.x, event.y)
        self.print_point(p_tmp.x, p_tmp.y)
        self.current_graph.points.append(p_tmp)
        print(f"new point at: {p_tmp}")
        self.solution_steps = []
        self.steps_idx = 0

    def mainloop(self):
        self.root.mainloop()

    #################### file processing ####################
    def read_dataset(self):
        self.dataset = fp.load_dataset()
        self.dataset_idx = 0

        self.clean_all()
        self.print_graph(Graph(self.dataset[self.dataset_idx], []))
        self.dataset_idx_str.set(f"Set [{self.dataset_idx+1}/{len(self.dataset)}]")

    def save_graph(self):
        fp.save_vd_graph(self.current_graph)

    def load_graph(self):
        self.clean_all()
        self.current_graph = fp.open_vd_graph()
        self.print_graph(self.current_graph)

    ####################### graphing ######################
    def clear_canvas(self):
        self.canvas.delete("all")

    def print_point(self, x: int, y: int, r: int = 3, fill="white", outline="black"):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline=outline)

    def print_line(self, x1: int, y1: int, x2: int, y2: int, fill="black"):
        self.canvas.create_line(x1, y1, x2, y2, fill=fill)

    def print_graph(self, graph: Graph):
        for p in graph.points:
            self.print_point(p.x, p.y)

        for l in graph.lines:
            self.print_line(l.p1.x, l.p1.y, l.p2.x, l.p2.y)

    ######################## others ########################
    def clean_all(self):
        self.clear_canvas()
        self.clear_contents()
        self.solution_steps = []
        self.steps_idx = 0

    def clear_contents(self):
        self.current_graph.points = []
        self.current_graph.lines = []

    def show_next_set(self):
        self.dataset_idx += 1
        if self.dataset_idx == len(self.dataset):
            self.dataset_idx = 0

        self.current_graph = Graph(self.dataset[self.dataset_idx], [])
        self.clear_canvas()
        self.print_graph(self.current_graph)
        self.dataset_idx_str.set(f"Set [{self.dataset_idx+1}/{len(self.dataset)}]")
        self.solution_steps = []

    def do_voronoi(self):
        self.solution_steps = vd_algo.do_vd(self.dataset[self.dataset_idx])
        self.print_graph(self.solution_steps[-1])
        self.steps_idx = 0

    def step_by_step(self):
        if not self.solution_steps:
            self.solution_steps = vd_algo.get_vd_steps(self.dataset[self.dataset_idx])
            self.steps_idx = 0

        self.clear_canvas()
        self.print_graph(self.solution_steps[self.steps_idx])
        self.steps_idx += 1
        if self.steps_idx > len(self.solution_steps):
            self.steps_idx = 0


if __name__ == "__main__":
    main_sc = sc()

    main_sc.mainloop()
