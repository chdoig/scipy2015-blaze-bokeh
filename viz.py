# -*- coding: utf-8 -*-
import math
from collections import OrderedDict

import pandas as pd
import netCDF4

from bokeh.plotting import figure, show, output_notebook
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, HoverTool, Plot, Range1d
from bokeh.palettes import RdBu11
from bokeh.models.glyphs import Text, Rect

import utils.world_countries as wc
from utils.colormap import RGBAColorMapper

colormap = RGBAColorMapper(-6, 6, RdBu11)

def get_slice(t, year, month):
    i = (year - 1850)*12 + month - 1
    return colormap.color(t[i, :, :])

def climate_map():
    data = netCDF4.Dataset('data/Land_and_Ocean_LatLong1.nc')
    t = data.variables['temperature']
    image = get_slice(t, 1950, 1)

    world_countries = wc.data.copy()

    worldmap = pd.DataFrame.from_dict(world_countries, orient='index')

    # Create your plot
    p =  figure(width=900, height=500, x_axis_type=None, y_axis_type=None,
            x_range=[-180,180], y_range=[-90,90], toolbar_location="left")

    p.image_rgba(
        image=[image],
        x=[-180], y=[-90],
        dw=[360], dh=[180], name='image'
    )

    p.patches(xs=worldmap['lons'], ys=worldmap['lats'], fill_color="white", fill_alpha=0,
        line_color="black", line_width=0.5)

    return p


def legend():
    # Set ranges
    xdr = Range1d(0, 100)
    ydr = Range1d(0, 500)
    # Create plot
    plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=100,
        plot_height=500,
        min_border=0,
        toolbar_location=None,
        outline_line_color="#FFFFFF",
    )

    # For each color in your palette, add a Rect glyph to the plot with the appropriate properties
    palette = RdBu11
    width = 40
    for i, color in enumerate(palette):
        rect = Rect(
            x=40, y=(width * (i + 1)),
            width=width, height=40,
            fill_color=color, line_color='black'
        )
        plot.add_glyph(rect)

    # Add text labels and add them to the plot
    minimum = Text(x=50, y=0, text=['-6 ºC'])
    plot.add_glyph(minimum)
    maximum = Text(x=50, y=460, text=['6 ºC'])
    plot.add_glyph(maximum)

    return plot

def timeseries():
    # Get data
    df = pd.read_csv('data/Land_Ocean_Monthly_Anomaly_Average.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df[['anomaly','datetime']]
    df['moving_average'] = pd.rolling_mean(df['anomaly'], 12)
    df = df.fillna(0)
    
    # List all the tools that you want in your plot separated by comas, all in one string.
    TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"

    # New figure
    t = figure(x_axis_type = "datetime", width=1000, height=200,tools=TOOLS)

    # Data processing
    # The hover tools doesn't render datetime appropriately. We'll need a string. 
    # We just want dates, remove time
    f = lambda x: str(x)[:7]
    df["datetime_s"]=df[["datetime"]].applymap(f)
    source = ColumnDataSource(df)

    # Create plot
    t.line('datetime', 'anomaly', color='lightgrey', legend='anom', source=source)
    t.line('datetime', 'moving_average', color='red', legend='avg', source=source, name="mva")

    # Style
    xformatter = DatetimeTickFormatter(formats=dict(months=["%b %Y"], years=["%Y"]))
    t.xaxis[0].formatter = xformatter
    t.xaxis.major_label_orientation = math.pi/4
    t.yaxis.axis_label = 'Anomaly(ºC)'
    t.legend.orientation = "bottom_right"
    t.grid.grid_line_alpha=0.2
    t.toolbar_location=None

    # Style hover tool
    hover = t.select(dict(type=HoverTool))
    hover.tooltips = """
        <div>
            <span style="font-size: 15px;">Anomaly</span>
            <span style="font-size: 17px;  color: red;">@anomaly</span>
        </div>
        <div>
            <span style="font-size: 15px;">Month</span>
            <span style="font-size: 10px; color: grey;">@datetime_s</span>
        </div>
        """
    hover.renderers = t.select("mva")

    # Show plot
    #show(t)
    return t