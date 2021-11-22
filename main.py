""" $LAN=Python """

from tkinter import *
from tkinter import ttk

import file_progress as fp


root = Tk()
root.title("Voronoi")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0)

# 畫圖區域
main_canvas = Canvas(mainframe, width=600, height=600, background="black")
main_canvas.grid(column=0, row=0)

# 放按鈕的容器
sideframe = ttk.Frame(root, padding="0 10 10 10")
sideframe.grid(column=1, row=0)

file_path = StringVar()

file_name_lb = ttk.Label(sideframe, textvariable=file_path)
read_file_btn = ttk.Button(sideframe, width=16, text="read file", command=lambda: fp.open_file(file_path))
show_graph_btn = ttk.Button(sideframe, width=16, text="next set", command=None)  # TODO : commands
next_step_btn = ttk.Button(sideframe, width=16, text="step by step", command=None)  # TODO : commands
show_result_btn = ttk.Button(sideframe, width=16, text="run", command=None)  # TODO : commands
output_graph_file_btn = ttk.Button(sideframe, width=16, text="save image", command=None)  # TODO : commands
read_graph_file_btn = ttk.Button(sideframe, width=16, text="read image", command=None)  # TODO : commands
clear_canvas_btn = ttk.Button(sideframe, width=16, text="clear canvas", command=None)  # TODO : commands

# sideframe layout
file_name_lb.grid(row=0)
read_file_btn.grid(row=1)
show_graph_btn.grid(row=2)
next_step_btn.grid(row=3)
show_result_btn.grid(row=4)
output_graph_file_btn.grid(row=5)
read_graph_file_btn.grid(row=6)
clear_canvas_btn.grid(row=7)

root.mainloop()
