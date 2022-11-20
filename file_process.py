""" $LAN=Python$ """

"""license: copyright of M103040083 李峮驊"""

# functions for file processing
from tkinter import filedialog as fd

from vd_algo import *

# 開測資
def load_dataset() -> list:

    filetypes = {("input files", "*.in"), ("all files", "*.*")}
    filename = fd.askopenfilename(title="選取檔案", initialdir="./", filetypes=filetypes)

    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()

    data = data.strip().split("\n")

    dataset = []
    i = 0
    while i < len(data):

        # empty line & comment line
        if not data[i] or data[i][0] == "#":
            i += 1
        elif data[i] == "0":
            break
        else:
            set_size = int(data[i])
            i += 1
            pi = 0
            points = []
            while pi < set_size:
                if data[i] and data[i][0] != "#":
                    x, y = map(int, data[i].split(" "))
                    p_tmp = Point(x, y)
                    points.append(p_tmp)

                pi += 1
                i += 1

            dataset.append(points)

    print("Dataset loaded.")
    for set_i, s in enumerate(dataset):
        print(f"set {set_i+1}")
        for p in s:
            print(p)
        print("---------------")
    return dataset


def open_vd_graph() -> Graph:
    filename = fd.askopenfilename(
        title="選取檔案",
        initialdir="./",
        filetypes={
            ("all files", "*.*"),
            ("voronoi diagram files", "*.vd"),
        },
    )

    with open(filename, "r") as f:
        data = f.read()

    data = data.strip().split("\n")

    points = []
    lines = []
    for line in data:
        # read points
        if line[0] == "P":
            ptmp = tuple(map(int, line[2:].split(" ")))
            points.append(ptmp)
        # read lines
        elif line[0] == "E":
            ltmp = tuple(map(int, line[2:].split(" ")))
            lines.append(ltmp)
        else:
            print("format error!")

    return Graph(points, lines)


def save_vd_graph(graph: Graph):
    print(graph)

    # ================ sorting ================ #
    graph.points.sort(key=lambda p: p.y)
    graph.points.sort(key=lambda p: p.x)

    graph.lines.sort(key=lambda l: l.p2.y)
    graph.lines.sort(key=lambda l: l.p2.x)
    graph.lines.sort(key=lambda l: l.p1.y)
    graph.lines.sort(key=lambda l: l.p1.x)
    # ========================================= #

    f = fd.asksaveasfile(
        mode="w",
        defaultextension=".vd",
        filetypes={
            ("voronoi diagram files", "*.vd"),
            ("all files", "*.*"),
        },
    )

    if f is None:
        print("file saving failed")
        return

    for p in graph.points:
        f.write(f"P {p.x:.0f} {p.y:.0f}\n")

    for l in graph.lines:
        f.write(f"E {l.p1.x:.0f} {l.p1.y:.0f} {l.p2.x:.0f} {l.p2.y:.0f}\n")

    f.close()
