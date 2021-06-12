import matplotlib.pyplot as plt
import numpy as np
import os, json

# Open file
with open(os.path.join("temp", "DMsInfo.json"), 'r') as file:
    data = json.load(file)

# Format data
formattedData = [[user, data[user]["sentTotal"], data[user]["receivedTotal"]] for user in data.keys()]

# Sort data
formattedData = np.array(sorted(formattedData, key=lambda x: int(x[1])+int(x[2]), reverse=True))

# Plot only n first points
N = 20
fig, ax = plt.subplots()
ax.bar(formattedData[:N, 0], formattedData[:N, 1].astype(int), 0.6, label="Sent")
ax.bar(formattedData[:N, 0], formattedData[:N, 2].astype(int), 0.6, bottom=formattedData[:N, 1].astype(int), label="Received")

ax.set_ylabel('Facebook Messages Exchanged')
ax.legend()

plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
