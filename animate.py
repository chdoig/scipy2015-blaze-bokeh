import numpy as np
import netCDF4

from bokeh.plotting import vplot, hplot, cursession, output_server, show

from viz import climate_map, timeseries, legend, get_slice  

# Data
data = netCDF4.Dataset('data/Land_and_Ocean_LatLong1.nc')
t = data.variables['temperature']

# Output option
output_server("climate")

# Plots
climate_map = climate_map()
timeseries = timeseries()
legend = legend()

# Create layout
map_legend = hplot(climate_map, legend)
layout = vplot(map_legend, timeseries)

# Show
show(layout)

# Select data source for climate_map
renderer = climate_map.select(dict(name="image"))
ds = renderer[0].data_source

# Create an infite loop to update image data
import time

while True:
   for year_index in np.arange(2000, 2015, 1):
        for month_index in np.arange(1, 13, 1):
            image = get_slice(t, year_index, month_index)
            ds.data["image"] = [image]
            cursession().store_objects(ds)
            time.sleep(0.2)
