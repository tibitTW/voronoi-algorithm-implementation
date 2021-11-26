"""檔案處理相關 function"""

from tkinter import filedialog as fd

# 開測資
def open_in_file(display_lb_text=None) -> list:

    filetypes = {("input files", "*.in")}
    filename = fd.askopenfilename(title="選取檔案", initialdir="./", filetypes=filetypes)
    if display_lb_text:
        display_lb_text.set("using file:\n" + filename.split("/")[-1])

    with open(filename, "r") as f:
        data = f.read()

    data = data.strip().split("\n")

    dataset = []
    i = 0
    while i < len(data):

        # empty line
        if len(data[i]) == 0:
            i += 1
        # read comment
        elif data[i][0] == "#":
            i += 1
        else:
            try:
                # 讀一組測試資料
                line = data[i].split(" ")
                if len(line) == 1:
                    # read EOF
                    if line[0] == "0":
                        return dataset

                    size = int(line[0])
                    contents = {"points": [], "lines": []}
                    for li in range(size):
                        contents["points"].append(tuple(map(int, data[i + li + 1].split())))

                    dataset.append(contents)
                    i += size + 1

                else:
                    i += 1
            except Exception as e:
                print(e)

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
    points = contents["points"]
    lines = contents["lines"]
    f = fd.asksaveasfile(mode="w", defaultextension=".vd", filetypes={("voronoi diagram files", "*.vd")})

    if f is None:
        print("save file failed")
        return

    for x, y in points:
        f.write(f"P {x} {y}\n")

    for x1, y1, x2, y2 in lines:
        f.write(f"E {x1} {y1} {x2} {y2}\n")

    f.close()
