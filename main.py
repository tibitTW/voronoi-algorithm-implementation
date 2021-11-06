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
sideframe = ttk.Frame(root, padding="10 10 10 10")
sideframe.grid(column=1, row=0)

fileframe = ttk.Frame(sideframe)
fileframe.grid(column=0, row=0)

file_path = StringVar()
file_name_lb = ttk.Label(fileframe, textvariable=file_path)
read_file_btn = ttk.Button(
    fileframe, width=16, text="open file", command=lambda: fp.open_file(file_path)
)
output_file_btn = ttk.Button(
    fileframe, width=16, text="save result to file", command=None
)
# TODO : command
show_graph_btn = ttk.Button(sideframe, width=16, text="show graph", command=None)
show_result_btn = ttk.Button(sideframe, width=16, text="show result", command=None)

next_step_btn = ttk.Button(sideframe, width=16, text="run next step", command=None)
clear_canvas_btn = ttk.Button(sideframe, width=16, text="clear canvas", command=None)


# sideframe layout
file_name_lb.grid(row=0)
read_file_btn.grid(row=1)
output_file_btn.grid(row=2)
show_graph_btn.grid(row=3)
show_graph_btn.grid(row=4)
show_result_btn.grid(row=5)
next_step_btn.grid(row=6)
clear_canvas_btn.grid(row=7)

root.mainloop()
