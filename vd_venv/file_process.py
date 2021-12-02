"""檔案處理相關 function"""

from tkinter import filedialog as fd

# 開測資
def open_in_file(display_lb_text=None) -> list:

    filetypes = {("input files", "*.in")}
    filename = fd.askopenfilename(title="選取檔案", initialdir="./", filetypes=filetypes)
    if display_lb_text:
        display_lb_text.set("using file:\n" + filename.split("/")[-1])

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
            contents = {"points": [], "lines": []}
            while pi < set_size:
                if data[i] and data[i][0] != "#":
                    x, y = map(int, data[i].split(" "))
                    contents["points"].append((x, y))

                pi += 1
                i += 1
            dataset.append(contents)

    return dataset


def open_vd_file():
    filetypes = {("voronoi diagram files", "*.vd")}
    filename = fd.askopenfilename(title="選取檔案", initialdir="./", filetypes=filetypes)

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

    return {"points": points, "lines": lines}


def save_vd_file(contents: dict):
    points = sorted(contents["points"])
    lines = sorted(contents["lines"])
    f = fd.asksaveasfile(mode="w", defaultextension=".vd", filetypes={("voronoi diagram files", "*.vd")})

    if f is None:
        print("save file failed")
        return

    for x, y in points:
        f.write(f"P {x:.0f} {y:.0f}\n")

    for x1, y1, x2, y2 in lines:
        f.write(f"E {x1:.0f} {y1:.0f} {x2:.0f} {y2:.0f}\n")

    f.close()
