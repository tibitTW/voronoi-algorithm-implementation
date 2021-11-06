from tkinter import filedialog as fd


def open_file(display_lb_text=None):
    filetypes = {("input files", "*.in"), ("All files", "*.*")}

    filename = fd.askopenfilename(title="選取檔案", initialdir="./", filetypes=filetypes)
    if display_lb_text:
        display_lb_text.set("file name: " + filename.split("/")[-1])

    with open(filename, "r") as f:
        data = f.read()

    data = data.strip().split()
    for d in data:
        print(d)
