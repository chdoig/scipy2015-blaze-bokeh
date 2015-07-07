# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
import netCDF4
import pandas as pd

from bokeh.browserlib import view

from bokeh.plotting import figure, show, vplot, hplot, output_server, cursession
from bokeh.palettes import RdYlBu11, RdBu11
from bokeh.models.widgets import Select, Slider
from bokeh.models.actions import Callback
from bokeh.models import ColumnDataSource
from bokeh.models import Plot, Text

import world_countries_1 as wc

year = 1850
month = 1

years = [str(x) for x in np.arange(1850, 2015, 1)]

months = [str(x) for x in np.arange(1, 13, 1)]
months_str = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

month_str = months_str[month-1]

#source = ColumnDataSource(data=dict(image=[]))

data = netCDF4.Dataset('data/Land_and_Ocean_LatLong1.nc')
t = data.variables['temperature']

world_countries = wc.data.copy()
country= pd.DataFrame.from_dict(world_countries, orient='index')

def hex_to_rgb(value):
    """Given a color in hex format, return it in RGB."""

    values = value.lstrip('#')
    lv = len(values)
    rgb = list(int(values[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return rgb 
 

class RGBAColorMapper(object):
    """Maps floating point values to rgb values over a palette"""
 
    def __init__(self, low, high, palette):
        self.range = np.linspace(low, high, len(palette))
        self.r, self.g, self.b = np.array(zip(*[hex_to_rgb(i) for i in palette]))
    
    def color(self, data):
        """Maps your data values to the pallette with linear interpolation"""

        red = np.interp(data, self.range, self.r)
        blue = np.interp(data, self.range, self.b)
        green = np.interp(data, self.range, self.g)
        # Style plot to return a grey color when value is 'nan'
        red[np.isnan(red)] = 240
        blue[np.isnan(blue)] = 240
        green[np.isnan(green)] = 240
        colors = np.dstack([red.astype(np.uint8),
                          green.astype(np.uint8),
                          blue.astype(np.uint8),
                          np.full_like(data, 255, dtype=np.uint8)])
        return colors.view(dtype=np.uint32).reshape(data.shape)

colormap = RGBAColorMapper(-6, 6, RdBu11)


def get_slice(t, year, month):
    i = (year - 1850)*12 + month - 1
    time = data.variables.get('time')
    return colormap.color(t[i, :, :])


output_server("earth")

plot = figure(
        plot_height=540,
        plot_width=1080,
        toolbar_location=None,
        x_axis_type=None, y_axis_type=None,
        x_range=(-180, 180),
        y_range=(-89, 89))

image = get_slice(t, 1891, 1)

plot.image_rgba(
    image=[image],
    x=[-180], y=[-89],
    dw=[360], dh=[178], name="im"
)

plot.text(x=10, y=-88, text=[month_str], text_font_size='25pt', text_color='black', name="mo")
plot.text(x=-22, y=-88, text=[str(year)], text_font_size='25pt', text_color='black', name="ye")

plot.patches(xs=country['lons'], ys=country['lats'], fill_color="white", fill_alpha=0,
    line_color="black", line_width=0.5)


# Legend

from bokeh.models.glyphs import Text, Rect
from bokeh.models import Plot, Range1d
from bokeh.palettes import RdBu11
from bokeh.plotting import output_notebook, show

xdr = Range1d(0, 100)
ydr = Range1d(0, 600)

legend_plot = Plot(
    x_range=xdr,
    y_range=ydr,
    title="",
    plot_width=100,
    plot_height=500,
    min_border=0,
    toolbar_location=None,
    outline_line_color="#FFFFFF",
    title_text_align='left',
    title_text_baseline='top',
)

minimum = Text(x=40, y=-2, text=['-6 ºC'])
legend_plot.add_glyph(minimum)
maximum = Text(x=40, y=460, text=['6 ºC'])
legend_plot.add_glyph(maximum)

palette = RdBu11
width = 40
for i, color in enumerate(palette):
    rect = Rect(
        x=40, y=(width * (i + 1)),
        width=width, height=40,
        fill_color=color, line_color='black'
    )
    legend_plot.add_glyph(rect)


# 

import math
import numpy as np

from bokeh.models import DatetimeTickFormatter, LinearAxis, ColumnDataSource, HoverTool
from collections import OrderedDict

df = pd.read_csv('data/Land_Ocean_Monthly_Anomaly_Average.csv', index_col=0)
df['date'] = pd.to_datetime(df['time'])
df['moving_average'] = pd.rolling_mean(df['anomaly'], 12)
df = df.fillna(0)

TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"

source = ColumnDataSource(df)

p = figure(x_axis_type = "datetime", width=1000, height=200,tools=TOOLS, toolbar_location=None)

dates = np.array(df['date'], dtype=np.datetime64)
anomaly = np.array(df['anomaly'])

p.line(dates, anomaly, color='lightgrey', legend='anom')
p.line('date', 'moving_average', color='red', legend='avg', source=source, name="mva")

p.grid.grid_line_alpha=0.2
p.yaxis.axis_label = 'Anomaly(ºC)'
p.xaxis.major_label_orientation = math.pi/4
p.legend.orientation = "bottom_right"

xformatter = DatetimeTickFormatter(formats=dict(months=["%b %Y"], years=["%Y"]))
#xaxis = DatetimeAxis(formatter=xformatter)

p.xaxis[0].formatter = xformatter


hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ("anomaly", "@anomaly"),
    ("time", "@time"),
])

hover.renderers = p.select("mva")


# Layout

layout = hplot(plot, legend_plot)
bottom = vplot(layout, p)

show(bottom)

renderer = plot.select(dict(name="im"))
ds = renderer[0].data_source

month_renderer = plot.select(dict(name="mo"))
month_ds = month_renderer[0].data_source

year_renderer = plot.select(dict(name="ye"))
year_ds = year_renderer[0].data_source

import time

while True:
    for year_index in np.arange(1950, 2015, 1):
        year_ds.data["text"] = [str(year_index)]
        #cursession().store_objects(year_ds)
        for month_index in np.arange(1, 13, 1):
            month_ds.data["text"] = [months_str[month_index-1]]
            image = get_slice(t, year_index, month_index)
            #print(image)
            ds.data["image"] = [image]
            cursession().store_objects(ds, month_ds, year_ds)
        #cursession().store_objects(ds, year_ds)
            time.sleep(0.2)



