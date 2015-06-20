"""check_env.py for Blaze - Bokeh tutorial at SciPy 2015"""

try:
    import blaze
    print blaze.__version__
    assert(blaze.__version__ == '0.8.0')
except ImportError:
    print("You need Blaze installed, please run: conda install blaze=0.8")

try:
    import bokeh
    print bokeh.__version__
    assert(bokeh.__version__ == '0.9.0')
except ImportError:
    print("You need Bokeh installed, please run: conda install bokeh=0.9")

try:
    import IPython
    print IPython.__version__
    assert(IPython.__version__ == '3.1.0')
except ImportError:
    print("You need IPython installed, please run: conda install ipython=3.1")


print("You are good to go :)")