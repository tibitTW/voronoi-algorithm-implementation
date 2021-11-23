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
        main_canvas = Canvas(self.mainframe, width=600, height=600, background="white")
        main_canvas.grid(column=0, row=0)

        # frame of buttons
        self.sideframe = ttk.Frame(self.root, padding="0 10 10 10")
        self.sideframe.grid(column=1, row=0)
        self._init_sideframe_elements()
        self._init_sideframe_layout()

    # initialize labels and buttons in sideframe
    def _init_sideframe_elements(self):
        self.file_path = StringVar()
        self.file_name_lb = ttk.Label(self.sideframe, textvariable=self.file_path)
        self.read_file_btn = ttk.Button(self.sideframe, width=16, text="read file", command=lambda: fp.open_file(self.file_path))
        self.show_graph_btn = ttk.Button(self.sideframe, width=16, text="next set", command=None)  # TODO : commands
        self.next_step_btn = ttk.Button(self.sideframe, width=16, text="step by step", command=None)  # TODO : commands
        self.show_result_btn = ttk.Button(self.sideframe, width=16, text="run", command=None)  # TODO : commands
        self.output_graph_file_btn = ttk.Button(self.sideframe, width=16, text="save image", command=None)  # TODO : commands
        self.read_graph_file_btn = ttk.Button(self.sideframe, width=16, text="read image", command=None)  # TODO : commands
        self.clear_canvas_btn = ttk.Button(self.sideframe, width=16, text="clear canvas", command=None)  # TODO : commands

    # initialize sideframe layout
    def _init_sideframe_layout(self):
        self.file_name_lb.grid(row=0)
        self.read_file_btn.grid(row=1)
        self.show_graph_btn.grid(row=2)
        self.next_step_btn.grid(row=3)
        self.show_result_btn.grid(row=4)
        self.output_graph_file_btn.grid(row=5)
        self.read_graph_file_btn.grid(row=6)
        self.clear_canvas_btn.grid(row=7)

    def mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    main_sc = sc()
    main_sc.mainloop()

# test
# main_canvas.create_line(10, 5, 200, 50)
# main_canvas.create_oval(30, 30, 100, 100)
