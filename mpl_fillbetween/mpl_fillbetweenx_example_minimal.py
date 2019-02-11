#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-11
# file: mpl_fillbetweenx_example_minimal.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.2  in conjunction with mpl version 3.0.2
##########################################################################################

'''
Minimal example to illustrate the use of matplotlib's fillbetweenx function.
This requires the same functionality as the fillbetween function, 
but with exchanged roles for x and y. For this purpose matplotlib's
fillbetweenx function is the ideal choice.
'''

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend
from scipy.stats import norm

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "{}-{}-{}".format(str(now.year), str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(OUTDIR)

if __name__ == '__main__':

    outname = 'mpl_fillbetweenx_example_minimal_'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + now # set datestamp
    
    nPoints = 400
    xVals = np.linspace(-6.0, 6.0, nPoints)
    yVals = norm.pdf(xVals, 0.0, 1.0)
    X = np.zeros((nPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'x label', fontsize = 8.0)
    ax1.set_ylabel(r'y label', fontsize = 8.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 2.0  
    
    ######################################################################################
    # Here it is important to understand the syntax of the fill_betweenx command.
    # The API specifies 
    # matplotlib.axes.Axes.fill_betweenx(y, x1, x2=0, where=None, step=None, 
    #                                    interpolate=False, *, data = None, **kwargs)
    # [from https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.fill_betweenx.html]
    # as of 2018-08-14
    # Above the first argument is the array with the y coordinates and the second argument 
    # is the array with the x coordinates.
    # However, below I first pass the x-coordinates and then the y-coordinates, since
    # I consider a normal x-y-plot turned by 90 degree and then flipped along 
    # the horizontal axis. Hence the conventional x-coordinates become the
    # new y-coordinates and vice versa, such that the first argument are basically 
    # the new y coordinates. This might be confusing, but it is here precisely what I want.
    # This might be different for different applications of yours and you should 
    # in all cases make sure to clearly understand the API and think about what you want.
    # As always.
    ######################################################################################
    
    ax1.fill_betweenx(X[:, 0], X[:, 1], 0.0,
                      color = 'C0',
                      alpha = 0.5,
                      lw = 0.0)
    
    ax1.plot(X[:, 1], X[:, 0], 
             color = 'C0',
             alpha = 1.0,
             lw = 1.5,
             zorder = 3,
             label = r'legend')

    leg = ax1.legend(handlelength = 1.5, 
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)
    plt.gca().add_artist(leg)

    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    
    plt.cla()
    plt.clf()
    plt.close()
