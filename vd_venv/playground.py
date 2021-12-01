#%%
import matplotlib.pyplot as plt
from random import randint

from tools import *


def convex_hull(points):
    num_points = len(points)
    if num_points <= 3:
        return points

    else:
        leftCH = convex_hull(points[: num_points // 2])
        rightCH = convex_hull(points[num_points // 2 :])
        return mergeCH(leftCH, rightCH)


def mergeCH(leftCH, rightCH):
    pL = leftCH[-1]
    pR = rightCH[0]

    return 0


# %%

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
