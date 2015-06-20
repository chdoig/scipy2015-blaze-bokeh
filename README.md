# Blaze and Bokeh tutorial, SciPy 2015
Building Python Data Applications with Blaze and Bokeh Tutorial, SciPy 2015

# Setup

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


Make sure you have the right environment setup by running the following script:

```
python check_env.py
```

