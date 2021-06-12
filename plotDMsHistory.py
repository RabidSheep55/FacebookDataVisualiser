import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os, json
from seaborn import color_palette

# Open file
with open(os.path.join("temp", "DMsInfo.json"), 'r') as file:
    data = json.load(file)

# Consider the top N users
N = 15
_temp = [[user, data[user]["sentTotal"], data[user]["receivedTotal"]] for user in data.keys()]
topUsers = np.array(sorted(_temp, key=lambda x: int(x[1])+int(x[2]), reverse=True))[:N, 0]

# Create pallete
pal = color_palette(palette='pastel', n_colors=N)

# Group into all messages and compute density functions, grabbing the min and max timestamps
timestampLists = [data[user]["sentTimestamps"] + data[user]["receivedTimestamps"] for user in topUsers]
densityFuncs = []
mini, maxi = np.inf, 0
for timestamps in timestampLists:
    density = gaussian_kde(timestamps)
    density.covariance_factor = lambda : 0.20
    density._compute_covariance()
    densityFuncs += [density]

    if min(timestamps) < mini: mini = min(timestamps)
    if max(timestamps) > maxi: maxi = max(timestamps)

x = np.linspace(mini, maxi, 200)

# Compute traces and normalize
densities = []
for i in range(N):
    density = densityFuncs[i](x)
    densities += [np.array(density/max(density))]

x = (x/1000).astype(np.datetime64)

for i, user in enumerate(topUsers):

    plt.fill_between(x, densities[i] - i*0.8, y2=-i*0.8, color=pal[i], label=user, zorder=i)
    plt.plot(x, densities[i] - i*0.8, c='w', zorder=i, linewidth=1)
    plt.text(np.min(x), -i*0.8 + 0.12, user, c=pal[i])

plt.yticks([])
plt.axis('off')

plt.show()
