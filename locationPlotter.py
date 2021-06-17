print("[loc] Starting location plotting")
import os
import pandas as pd
import folium
from folium.plugins import HeatMap
from datetime import datetime as dt

# Load location history data
file_loc = os.path.join("unzipped3", "location", "location_history.json")
df = pd.read_json(file_loc, orient='records', convert_axes=True)["location_history_v2"]
df = pd.json_normalize(df)
print(f"[loc] Loaded {df.shape[0]} entries")

# Plot
m = folium.Map(
    # tiles="Stamen Toner",
    zoom_control=False,
    attributionControl=0
)

heatmap_settings = {
    "radius": 15,
    # "gradient": {
    #     0.4: "#fab1a0",
    #     0.6: "#e17055"
    # }
}

heatmap = HeatMap(df[["coordinate.latitude", "coordinate.longitude"]], **heatmap_settings)

# Get south west and north east most points for setting bounds
sw = df[["coordinate.latitude", "coordinate.longitude"]].min().values.tolist()
ne = df[["coordinate.latitude", "coordinate.longitude"]].max().values.tolist()
m.fit_bounds([sw, ne])

m.add_child(heatmap)
m.save(os.path.join("temp", "map.html"))

# For debug/output
import webbrowser
print("[loc] Opening index.html in browser")
webbrowser.open("file://" + os.path.join(os.getcwd(), "temp", 'map.html'))
