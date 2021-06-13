import numpy as np
from seaborn import color_palette
from scipy.stats import gaussian_kde
import os, json

# Consider the top N users
N = 15

# Open file
with open(os.path.join("temp", "DMsInfo.json"), 'r') as file:
    data = json.load(file)

# Sort by most messages exchanged
_temp = [[user, data[user]["sentTotal"], data[user]["receivedTotal"]] for user in data.keys()]
topUsers = np.array(sorted(_temp, key=lambda x: int(x[1])+int(x[2]), reverse=True))[:N, 0]

# Create pallete
pal = color_palette(palette='rocket', n_colors=N+2)
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
    densities += [list(density/max(density))]

# Save to file
output = {
    "labels": list(topUsers),
    "densities": densities,
    "palette": pal,
    "x": list(x)
}

with open(os.path.join("temp", "DMsDensityInfo.json"), "w") as file:
    json.dump(output, file)
