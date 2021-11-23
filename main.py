""" $LAN=Python """

from tkinter import *
from tkinter import ttk

import file_process as fp


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

    # initialize labels and buttons in sideframe
    def init_sideframe_elements(self):
        self.file_path = StringVar()
        self.file_name_lb = ttk.Label(self.sideframe, textvariable=self.file_path)
        self.read_file_btn = ttk.Button(self.sideframe, width=16, text="read file", command=self.read_dataset)
        self.next_set_btn = ttk.Button(self.sideframe, width=16, text="next set", command=self.show_next_set)
        self.step_by_step_btn = ttk.Button(self.sideframe, width=16, text="step by step", command=None)  # TODO : commands
        self.run_btn = ttk.Button(self.sideframe, width=16, text="run", command=None)  # TODO : commands
        self.write_graph_file_btn = ttk.Button(self.sideframe, width=16, text="save image", command=self.save_graph)
        self.read_graph_file_btn = ttk.Button(self.sideframe, width=16, text="read image", command=self.read_graph)
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

    def canvas_mouse_click_event(self, event):
        self.graph_contents["points"].append((event.x, event.y))
        self.print_point(event.x, event.y)

    def mainloop(self):
        self.root.mainloop()

    def read_dataset(self):
        self.dataset = fp.open_in_file(self.file_path)

    def show_next_set(self):
        self.dataset_idx += 1
        if self.dataset_idx < len(self.dataset):
            self.graph_contents = self.dataset[self.dataset_idx]
            self.clean_canvas()
            self.print_graph(self.graph_contents)
        else:
            self.dataset_idx = -1
            self.clean_canvas()
            self.graph_contents = {"points": [], "lines": []}

    def read_graph(self):
        # read file
        graph_content = fp.open_vd_file()
        self.graph_contents["points"] = graph_content["points"]
        self.graph_contents["lines"] = graph_content["lines"]
        self.print_graph(graph_content)

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

    def save_graph(self):
        self.graph_contents["points"].sort()
        self.graph_contents["lines"].sort()
        fp.save_vd_file(self.graph_contents)


if __name__ == "__main__":
    main_sc = sc()

    main_sc.mainloop()
