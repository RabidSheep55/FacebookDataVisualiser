from seaborn import color_palette
import os, json
N = 10
pal = color_palette("blend:#20ADAB,#636e72", n_colors=N)

with open(os.path.join("temp", "densityPalette.js"), 'w') as file:
    file.write("const densityPalette = ")
    json.dump(pal, file)
