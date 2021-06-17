from seaborn import color_palette, palplot
import matplotlib.pyplot as plt
import os, json
N = 10
# pal = color_palette("blend:#20ADAB,#636e72", n_colors=N)
pal = color_palette("blend:#2d3436,#00b0ac", n_colors=N)
# pal = color_palette("ch:start=.2,rot=-.3", n_colors=N)
palplot(pal)
plt.tight_layout()


with open(os.path.join("temp", "densityPalette.js"), 'w') as file:
    file.write("const densityPalette = ")
    json.dump(pal, file)

# plt.show()
