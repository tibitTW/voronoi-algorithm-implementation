#%%
import numpy as np
import matplotlib.pyplot as plt

from tools import *

# %%
def f(x):
    return -x + 500


#%%

# %%
p1 = P(100, 300)
p2 = P(200, 400)
p3 = (p1 + p2) / 2
print(p3)
# %%
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()
plt.xlim(0, 600)
plt.ylim(0, 600)

p1.draw()
p2.draw()
p3.draw("r")
plt.plot([0, 600], [f(0), f(600)])

plt.show()
