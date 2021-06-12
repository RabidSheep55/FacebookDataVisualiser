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
m = folium.Map()

heatmap_settings = {
    "radius": 15
}

heatmap = HeatMap(df[["coordinate.latitude", "coordinate.longitude"]], **heatmap_settings)

m.add_child(heatmap)
m.save(os.path.join("outputs", "index.html"))

# For debug/output
import webbrowser
print("[loc] Opening index.html in browser")
webbrowser.open("file://" + os.path.join(os.getcwd(), "outputs", 'index.html'))
