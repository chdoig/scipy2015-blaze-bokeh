# -*- coding: utf-8 -*-

# **Exercise: Animate the timeseries plot**

# In[1]:

# Imports
from threading import Thread
import datetime
import logging
import time

import numpy as np
import netCDF4
import pandas as pd

from bokeh.plotting import vplot, hplot, cursession, curdoc, output_server, show
from bokeh.models.widgets import Button, Icon

from viz import climate_map, timeseries, legend, get_slice  


# In[2]:

# Data
data = netCDF4.Dataset('data/Land_and_Ocean_LatLong1.nc')
t = data.variables['temperature']
df = pd.read_csv('data/Land_Ocean_Monthly_Anomaly_Average.csv', parse_dates=[0])


# In[3]:

# Output option
output_server("climate")


# In[4]:

from bokeh.plotting import figure

# Data 
year = 1850
month = 1

years = [str(x) for x in np.arange(1850, 2015, 1)]

months = [str(x) for x in np.arange(1, 13, 1)]
months_str = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

month_str = months_str[month-1]

date = datetime.date(year, month, 1)
df['moving_average'] = pd.rolling_mean(df['anomaly'], 12)
df = df.fillna(0)

# New text Plot
title = figure(width=1200, height=100, x_range=(0, 1200), y_range=(0, 100), toolbar_location=None,
        x_axis_type=None, y_axis_type=None, outline_line_color="#FFFFFF", tools="", min_border=0)

title.text(x=500, y=5, text=[month_str], text_font_size='36pt', text_color='black', name="month", text_font="Georgia")
title.text(x=350, y=5, text=[str(year)], text_font_size='36pt', text_color='black', name="year",text_font="Georgia")


# In[5]:

# Plots
climate_map = climate_map()
timeseries = timeseries()
legend = legend()


# ADD WIDGETS
play = True

def play_handler():
    print("button_handler: start click")
    global play 
    play = True

def stop_handler():
    print("button_handler: stop click")
    global play 
    play = False

button_start = Button(label="Start", type="success")
button_start.on_click(play_handler)

button_stop = Button(label="Stop", type="danger")
button_stop.on_click(stop_handler)


controls = hplot(button_start, button_stop)

# In[6]:

# New circle in timeseries plot
timeseries.circle(x=[date], y=[df[df.datetime == date].moving_average], size=8, name="circle")


# In[7]:

# Create layout
map_legend = hplot(climate_map, legend)
layout = vplot(controls, title, map_legend, timeseries)


# In[8]:

# Show
show(layout)


# In[9]:

# Select data source for climate_map and month and year
renderer = climate_map.select(dict(name="image"))
ds = renderer[0].data_source

month_renderer = title.select(dict(name="month"))
month_ds = month_renderer[0].data_source

year_renderer = title.select(dict(name="year"))
year_ds = year_renderer[0].data_source

# Select data source for timeseries data
timeseries_renderer = timeseries.select(dict(name="circle"))
timeseries_ds = timeseries_renderer[0].data_source


def should_play():
    """
    Return true if we should play animation, otherwise block
    """
    global play
    while True:
        if play:
            return True
        else:
            time.sleep(0.05)


def background_thread(ds, year_ds, month_ds, timeseries_ds):
    """Plot animation, update data if play is True, otherwise stop"""
    try:
        while True:
            for year_index in np.arange(2000, 2015, 1):
                    year_ds.data["text"] = [str(year_index)]
                    for month_index in np.arange(1, 13, 1):
                        if should_play():  
                            month_ds.data["text"] = [months_str[month_index-1]]
                            image = get_slice(t, year_index, month_index)
                            date = datetime.date(year_index, month_index, 1)
                            timeseries_ds.data["x"] = [date]
                            timeseries_ds.data["y"] = [df[df.datetime == date].moving_average]
                            ds.data["image"] = [image]
                            cursession().store_objects(ds, year_ds, month_ds, timeseries_ds)
                            time.sleep(0.5)
                        time.sleep(0.5)
    except:
        logger.exception("An error occurred")
        raise


# spin up a background thread 
Thread(target=background_thread, args=(ds, year_ds, month_ds, timeseries_ds)).start()

# endlessly poll
cursession().poll_document(curdoc(), 0.04)

