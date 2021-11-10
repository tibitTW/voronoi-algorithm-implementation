#%%
import numpy as np
import matplotlib.pyplot as plt

# %%
p1 = (300, 300)
p2 = (400, 400)

#%%
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()
plt.xlim(0, 600)
plt.ylim(0, 600)
plt.scatter([300, 400], [300, 400])
plt.plot([300, 400], [300, 400])
plt.show()
