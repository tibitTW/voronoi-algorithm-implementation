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

    #################### core functions ####################
    def init_sideframe_elements(self):
        self.file_path = StringVar()
        self.file_name_lb = ttk.Label(self.sideframe, textvariable=self.file_path)
        self.read_file_btn = ttk.Button(self.sideframe, width=16, text="read file", command=self.read_dataset)
        self.next_set_btn = ttk.Button(self.sideframe, width=16, text="next set", command=self.show_next_set)
        self.step_by_step_btn = ttk.Button(self.sideframe, width=16, text="step by step", command=None)  # TODO : commands
        self.run_btn = ttk.Button(self.sideframe, width=16, text="run", command=self.do_voronoi)
        self.write_graph_file_btn = ttk.Button(self.sideframe, width=16, text="save image", command=self.save_graph)
        self.read_graph_file_btn = ttk.Button(self.sideframe, width=16, text="read image", command=self.read_graph)
        self.clear_canvas_btn = ttk.Button(self.sideframe, width=16, text="clear canvas", command=self.clean)

    def init_sideframe_layout(self):
        self.file_name_lb.grid(row=0)
        self.read_file_btn.grid(row=1)
        self.next_set_btn.grid(row=2)
        self.run_btn.grid(row=3)
        self.step_by_step_btn.grid(row=4)
        self.write_graph_file_btn.grid(row=5)
        self.read_graph_file_btn.grid(row=6)
        self.clear_canvas_btn.grid(row=7)

    def canvas_mouse_click_event(self, event):
        self.graph_contents["points"].append((event.x, event.y))
        self.print_point(event.x, event.y)

    def mainloop(self):
        self.root.mainloop()

    #################### file processing ####################
    def read_dataset(self):
        self.dataset = fp.open_in_file(self.file_path)
        self.dataset_idx = -1

    def save_graph(self):
        self.graph_contents["points"].sort()
        self.graph_contents["lines"].sort()
        fp.save_vd_file(self.graph_contents)

    def read_graph(self):
        self.clear_contents()
        self.clean_canvas()
        self.graph_contents = fp.open_vd_file()
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
        self.clean_canvas()
        self.clear_contents()

    def clear_contents(self):
        self.graph_contents = {"points": [], "lines": []}

    def show_next_set(self):
        self.dataset_idx += 1
        if self.dataset_idx < len(self.dataset):
            self.graph_contents = self.dataset[self.dataset_idx]
            self.clean_canvas()
            self.print_graph(self.graph_contents)
        else:
            self.dataset_idx = -1
            self.clean_canvas()
            self.clear_contents()

    # TODO: 寫成 divide & conquer 解法
    def do_voronoi(self):
        self.graph_contents["points"].sort()
        solutions = do_vd(self.graph_contents["points"])

        points = solutions[-1].CH_points

        self.print_point(points[0][0], points[0][1], fill="red")
        for i in range(len(points) - 1):
            self.print_line(*points[i], *points[i + 1])
        self.print_line(*points[-1], *points[0])
        for p in points:
            self.canvas.create_text(p[0], p[1], text=str(points.index(p)), anchor="nw")

        print(solutions[-1])
        lines = solutions[-1].CH_lines
        for l in lines:
            print(l.line)
            self.print_line(*l.line)


if __name__ == "__main__":
    main_sc = sc()

    main_sc.mainloop()
