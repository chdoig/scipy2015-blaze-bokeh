# Blaze and Bokeh tutorial, SciPy 2015

Building Python Data Applications with Blaze and Bokeh Tutorial, SciPy 2015

# Setup

```
git clone https://github.com/chdoig/scipy2015-blaze-bokeh.git
cd scipy2015-blaze-bokeh
```

- **Option A: Anaconda**

If you don't have Anaconda installed, you can install it from [here](https://store.continuum.io/cshop/anaconda/).
After following the instructions, you should be ready to go. Check it with:

```
python check_env.py
```

If you already have Anaconda installed, make sure to update both conda and anaconda 
to the latest versions, by running:

```
conda update conda
conda update anaconda
```

- **Option B: Miniconda**

If you want a lightweight alternative to Anaconda, you can install Miniconda from 
[here](http://conda.pydata.org/miniconda.html).

After cloning this repository, run the following commands:

```
cd scipy2015-blaze-bokeh
conda env create
```

If you are running Linux or OS X run:

```
source activate scipy-tutorial
```

If you are running Windows, run:

```
activate scipy-tutorial
```

# Testing

Make sure you have the right environment setup by running the following script:

```
python check_env.py
```

Also, try to run the testing notebook (0 - Test Notebook.ipynb):

```
ipython notebook
```

and run all the cells.

# Data

This tutorial will use the following datasets:

- [Berkeley Earth](http://www.berkeleyearth.org) ~400MB
- [Sean Lahman Baseball](http://www.seanlahman.com/baseball-archive/statistics/) ~50MB

Download the datasets *before* attending the tutorial from:

- https://s3.amazonaws.com/scipy-blaze-bokeh/Land_and_Ocean_LatLong1.nc
- https://s3.amazonaws.com/scipy-blaze-bokeh/lahman2013.sqlite

Move those datasets to the folder ``~/scipy2015-blaze-bokeh/data``

# Resources

- [Slides](http://chdoig.github.com/scipy2015-blaze-bokeh)

- Docs:

    + [Bokeh](http://bokeh.pydata.org/en/latest/)
    + [Blaze](http://blaze.pydata.org/en/latest/)
    + [Odo](http://odo.readthedocs.org/en/latest/)










