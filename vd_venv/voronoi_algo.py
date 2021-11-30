#%%
import matplotlib.pyplot as plt
from random import randint

from tools import *


def get_vd(vd: VD):
    pass
    # pnum = len(vd.points)
    # if pnum == 1:
    #     return
    # if pnum == 2:
    #     p1, p2 = vd.points
    #     line = get_bisection(p1, p2)
    #     vd.lines.append(line)
    # get_vd(plist[: pnum // 2])
    # get_vd(plist[pnum // 2 :])

    # print(plist)


def display_vd(vd: VD):
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes()
    plt.xlim(0, 600)
    plt.ylim(0, 600)

    for x, y in vd.points:
        plt.scatter(x, y, c="g")
    for x1, y1, x2, y2 in vd.lines:
        plt.plot((x1, x2), (y1, y2), c="b")

    plt.show()


# %%
vd1 = VD()
for _ in range(4):
    p = (randint(100, 500), randint(100, 500))
    vd1.points.append(p)

vd1.points.sort()
# %%
display_vd(vd1)

# %%
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()
plt.xlim(0, 600)
plt.ylim(0, 600)

for x, y in plist:
    plt.scatter(x, y, c="g")
vd(plist)

plt.show()

# %%
