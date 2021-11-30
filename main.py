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

        # frame of buttons
        self.sideframe = ttk.Frame(self.root, padding="0 10 10 10")
        self.sideframe.grid(column=1, row=0)
        self.init_sideframe_elements()
        self.init_sideframe_layout()

        # record points and lines
        self.graph_contents = {"points": [], "lines": []}
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
        self.step_by_step_btn.grid(row=3)
        self.run_btn.grid(row=4)
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

    def save_graph(self):
        self.graph_contents["points"].sort()
        self.graph_contents["lines"].sort()
        fp.save_vd_file(self.graph_contents)

    def read_graph(self):
        # read file
        graph_content = fp.open_vd_file()
        self.graph_contents["points"] = graph_content["points"]
        self.graph_contents["lines"] = graph_content["lines"]
        self.print_graph(graph_content)

    ####################### draw graph ######################
    def clean_canvas(self):
        self.canvas.delete("all")

    def print_point(self, x: int, y: int, r: int = 3, fill="black", outline="black"):
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
        if len(self.graph_contents["points"]) <= 1:
            return
        elif len(self.graph_contents["points"]) == 2:
            p1, p2 = self.graph_contents["points"]
            if p1 == p2:  # 共點
                return

            x1, y1, x2, y2 = get_bisection(p1, p2)
            self.print_line(x1, y1, x2, y2)

        elif len(self.graph_contents["points"]) == 3:
            self.graph_contents["points"].sort()
            p1, p2, p3 = self.graph_contents["points"]

            # 1. 找ab中垂線
            line1 = a1x, a1y, a2x, a2y = get_bisection(p1, p2)
            a1, a2 = (a1x, a1y), (a2x, a2y)
            # 2. 找bc中垂線
            line2 = b1x, b1y, b2x, b2y = get_bisection(p2, p3)
            b1, b2 = (b1x, b1y), (b2x, b2y)
            # 3. 找中垂線交點
            if intersect(a1, a2, b1, b2):  # 兩線有交點
                # a. 找交點位置
                x, y = intersection(a1, a2, b1, b2)
                if p2[1] > p1[1]:
                    top_point = p1
                    btn_point = p2
                else:
                    top_point = p2
                    btn_point = p1

                hyperplane = []
                hpx1, hpy1, hpx2, hpy2 = get_bisection(top_point, p3)
                if hpy1 < hpy2:
                    pass
                    hyperplane.append((hpx1, hpy1, x, y))
                else:
                    hyperplane.append((hpx2, hpy2, x, y))

                if a1x - x < 0:
                    line1 = (a1x, a1y, x, y)
                else:
                    line1 = (x, y, a2x, a2y)

                c1x, c1y, c2x, c2y = get_bisection(btn_point, p3)

                if c1y > y:
                    hyperplane.append((x, y, c1x, c1y))
                else:
                    hyperplane.append((x, y, c2x, c2y))

                self.print_line(*line1, "red")
                self.print_line(*hyperplane[0], "blue")
                self.print_line(*hyperplane[1], "green")

                for l in (line1, hyperplane[0], hyperplane[1]):
                    x1, y1, x2, y2 = l
                    if x1 < x2:
                        self.graph_contents["lines"].append(l)
                    elif x1 == x2:
                        if y1 < y2:
                            self.graph_contents["lines"].append(l)
                        else:
                            self.graph_contents["lines"].append((x2, y2, x1, y1))
                    else:
                        self.graph_contents["lines"].append((x2, y2, x1, y1))

            else:  # 兩線無交點
                self.print_line(*line1)
                self.print_line(*line2)
        else:
            # TODO
            print("TODO: solve problems using more than 3 points.")


if __name__ == "__main__":
    main_sc = sc()

    main_sc.mainloop()
