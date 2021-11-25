#%%
import matplotlib.pyplot as plt

from tools import *

# %%
def line_cross(line1p1, line1p2, line2p3, line2p4):

    if line1p2[0] == line1p1[0]:

        k1 = (line2p4[1] - line2p3[1]) * 1.0 / (line2p4[0] - line2p3[0])
        b1 = line2p3[1] * 1.0 - line2p3[0] * k1 * 1.0

        if (line1p2[0] - line1p1[0]) == 0:
            k2 = None
            b2 = 0
        else:
            k2 = (line1p2[1] - line1p1[1]) * 1.0 / (line1p2[0] - line1p1[0])
            b2 = line1p1[1] * 1.0 - line1p1[0] * k2 * 1.0

        if k2 == None:
            x = line1p1[0]
        elif k1 == k2:
            return -1, -1
        else:
            x = (b2 - b1) * 1.0 / (k1 - k2)

        y = k1 * x * 1.0 + b1 * 1.0

        return x, y

    else:

        k1 = (line1p2[1] - line1p1[1]) * 1.0 / (line1p2[0] - line1p1[0])
        b1 = line1p1[1] * 1.0 - line1p1[0] * k1 * 1.0

        if (line2p4[0] - line2p3[0]) == 0:
            k2 = None
            b2 = 0
        else:
            k2 = (line2p4[1] - line2p3[1]) * 1.0 / (line2p4[0] - line2p3[0])
            b2 = line2p3[1] * 1.0 - line2p3[0] * k2 * 1.0

        if k2 == None:
            x = line2p3[0]
        elif k1 == k2:
            return -1, -1
        else:
            x = (b2 - b1) * 1.0 / (k1 - k2)

        y = k1 * x * 1.0 + b1 * 1.0

        return x, y


def line_cross2(line1, line2):

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return -878787, -878787

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x, y


# %%
line1 = ((0, 0), (600, 600))
line2 = ((600, 0), (0, 600))
d = line_cross2(line1, line2)
print(d)
# %%
line1 = (0, 0, 600, 600)
line2 = (0, 600, 600, 0)
d = line_cross(line1[:2], line1[2:], line2[:2], line2[2:])
print(d)
# %%
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()
plt.xlim(0, 600)
plt.ylim(0, 600)


plt.show()
