from tkinter import filedialog as fd

# 開測資
def open_file(display_lb_text=None):

    filetypes = {("input files", "*.in"), ("All files", "*.*")}
    filename = fd.askopenfilename(title="選取檔案", initialdir="./", filetypes=filetypes)
    if display_lb_text:
        display_lb_text.set("opening file: " + filename.split("/")[-1])

    with open(filename, "r") as f:
        data = f.read()

    data = data.strip().split("\n")

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
                print(line)
                if len(line) == 1:
                    print("test data size:", line[0])
                    # read EOF
                    if line[0] == "0":
                        return

                    size = int(line[0])
                    dots = []
                    for li in range(size):
                        dots.append(tuple(map(int, data[i + li + 1].split())))
                        print(data[i + li + 1])

                    for dot in dots:
                        print(dot)

                    i += size + 1

                else:
                    i += 1
            except Exception as e:
                print(e)


def save_file():
    None
