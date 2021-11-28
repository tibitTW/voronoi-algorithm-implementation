#%%
import matplotlib.pyplot as plt
from random import randint

from tools import *

# %%
p1 = P(100, 100)
p2 = P(300, 400)
p3 = P(500, 200)
plist = (p1, p2, p3)
# %%
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()
plt.xlim(0, 600)
plt.ylim(0, 600)

for p in plist:
    plt.scatter(p.x, p.y, c="g")

plt.show()

# %%
def vd(plist):
    pnum = len(plist)
    if pnum == 1:
        return
    if pnum == 2:
        line = get_bisection(plist[0], plist[1])
    vd(plist[: pnum // 2])
    vd(plist[pnum // 2 :])

    print(plist)


vd(plist)
