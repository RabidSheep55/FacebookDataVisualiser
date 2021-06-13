import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os, json
from seaborn import color_palette

# Consider the top N users
N = 15

# Open file
with open(os.path.join("temp", "DMsInfo.json"), 'r') as file:
    data = json.load(file)

# Sort by most messages exchanged
_temp = [[user, data[user]["sentTotal"], data[user]["receivedTotal"]] for user in data.keys()]
topUsers = np.array(sorted(_temp, key=lambda x: int(x[1])+int(x[2]), reverse=True))[:N, 0]

# Create pallete
pal = color_palette(palette='Set2', n_colors=N+2)
# rocket, viridis, Set2, Paired

# Group into all messages and compute density functions, grabbing the min and max timestamps
timestampLists = [data[user]["sentTimestamps"] + data[user]["receivedTimestamps"] for user in topUsers]
densityFuncs = []
mini, maxi = np.inf, 0
for timestamps in timestampLists:
    density = gaussian_kde(timestamps)
    density.covariance_factor = lambda : 0.12
    density._compute_covariance()
    densityFuncs += [density]

    if min(timestamps) < mini: mini = min(timestamps)
    if max(timestamps) > maxi: maxi = max(timestamps)

# Create x-space (with extra padding on the left)
x = np.linspace(mini-(maxi-mini)/7, maxi, 600)

# Compute traces and normalize
densities = []
for i in range(N):
    density = densityFuncs[i](x)
    densities += [np.array(density/max(density))]

# Convert x to datetime
x = (x/1000).astype(np.datetime64)

# Plot
plt.figure(figsize=(8, N*6/15))
for i, user in enumerate(topUsers):
    plt.fill_between(x, densities[i] - i*0.8, y2=-i*0.8, color=pal[i], label=user, zorder=i)
    plt.plot(x, densities[i] - i*0.8 + 0.025, c='w', zorder=i, linewidth=1)
    plt.text(np.min(x), -i*0.8 + 0.1, user, c=pal[i])

# Apply plot settings
plt.box(False)
plt.tick_params(axis='y', left=False, top=False, right=False, bottom=False, labelleft=False, labeltop=False, labelright=False, labelbottom=False)
plt.tick_params(axis='x', colors=pal[N-1])
plt.suptitle("Normalized Frequency for Facebook Messages sent over time", c=pal[0], fontsize=12, y=0.96)
plt.title("[Top trace has the most total messages]", c=pal[0], fontdict={'fontsize': 10}, pad=0.8)
plt.ylim(bottom=-(N-1)*0.8-0.05)
plt.tight_layout()

# Save and display
plt.savefig(os.path.join("outputs", "DM History Plot.png"), dpi=500)
plt.show()
