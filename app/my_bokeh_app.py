# -*- coding: utf-8 -*-
import math
from collections import OrderedDict

import flask

import pandas as pd
import netCDF4
import numpy as np

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8

from bokeh.models import DatetimeTickFormatter, ColumnDataSource, HoverTool, Plot, Range1d
from bokeh.palettes import RdBu11
from bokeh.models.glyphs import Text, Rect
from bokeh.plotting import figure, show, output_notebook, hplot, vplot

import utils.world_countries as wc
from utils.colormap import RGBAColorMapper

from viz2 import climate_map, timeseries, legend, title, get_slice 

app = flask.Flask(__name__)

colormap = RGBAColorMapper(-6, 6, RdBu11)


@app.route("/")
def index():
    # Create layout
    c_map = climate_map()
    ts = timeseries()
    l = legend()
    t = title()

    map_legend = hplot(c_map, l)
    layout = vplot(t, map_legend, ts)

    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw,
        css_raw=INLINE.css_raw,
        js_files=INLINE.js_files,
        css_files=INLINE.css_files,
    )
    script, div = components(layout, INLINE)
    html = flask.render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        plot_resources=plot_resources,
    )
    return encode_utf8(html)


if __name__ == "__main__":
    app.run(debug=True)