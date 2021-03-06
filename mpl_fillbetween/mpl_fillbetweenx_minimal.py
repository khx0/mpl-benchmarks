#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-05-11
# file: mpl_fillbetweenx_minimal.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
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
from scipy.stats import norm

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    outname = 'mpl_fillbetweenx_example_minimal_'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today # set datestamp

    n_points = 400
    xVals = np.linspace(-6.0, 6.0, n_points)
    yVals = norm.pdf(xVals, 0.0, 1.0)
    X = np.zeros((n_points, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals


    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'x label', fontsize = 8.0)
    ax1.set_ylabel(r'y label', fontsize = 8.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 2.0

    ######################################################################################
    # To account for the switched roles of x and y you need to properly understand
    # the syntax of the fill_betweenx command.
    # The API specifies
    # matplotlib.axes.Axes.fill_betweenx(y, x1, x2=0, where=None, step=None,
    #                                    interpolate=False, *, data = None, **kwargs)
    # [from https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.fill_betweenx.html]
    # as of 2018-08-14
    # Above the first argument is the array with the y coordinates and the second argument
    # is the array with the x coordinates.
    #
    # In the example below we first pass the x-coordinates and then the y-coordinates,
    # since we consider a normal x-y-plot turned by 90 degree and then flipped along
    # the horizontal axis. Hence, the conventional x-coordinates become the
    # new y-coordinates and vice versa, such that the first argument is basically
    # the array of new y coordinates. This might be confusing, but here it is precisely
    # the desired behavior.
    # This might differ for different applications of yours and you should
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
