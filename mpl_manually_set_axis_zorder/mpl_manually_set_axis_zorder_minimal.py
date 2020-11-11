#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-11
# file: mpl_manually_set_axis_zorder_minimal.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.2
##########################################################################################

import os
import datetime
import platform
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    outname = 'mpl_manually_set_axis_zorder_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # create synthetic data
    n_vispoints = 500

    xVals = np.linspace(-0.5, 1.5, n_vispoints)
    yVals1 = np.sin(xVals)
    yVals2 = np.sin(2.0 * xVals) - 0.1
    X = np.zeros((n_vispoints, 3))
    X[:, 0] = xVals
    X[:, 1] = yVals1
    X[:, 2] = yVals2

    # minimal plot
    f, ax1 = plt.subplots(1)

    '''
    Using the zorder keyword we plot the first line below the
    axis, whereas we put the second line above it.
    Comapare the corresponding zorder values:
    zorder = 1 and 11 for the two lines
    and zorder = 10 for the axis, as manually set below.
    The value of zoder = 10 for the axis should be adjusted
    for your individual needs.
    '''

    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = 'C0',
             lw = 1.0,
             label = 'data 1',
             clip_on = False,
             zorder = 1)

    ax1.plot(X[:, 0], X[:, 2],
             alpha = 1.0,
             color = 'C1',
             lw = 1.0,
             label = 'data 2',
             clip_on = False,
             zorder = 11)

    ######################################################################################
    ######################################################################################
    # manually set the axis zorder here
    ax1.set_axisbelow(False)

    for spine in ax1.spines.values(): # ax1.spines is a dictionary
        spine.set_zorder(10)
    ######################################################################################
    ######################################################################################

    leg = ax1.legend(handlelength = 1.35,
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)

    ######################################################################################
    # set plot range and scale
    ax1.set_xlim(-0.05, 1.05)

    outname += '_' + today
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    plt.show()

    plt.cla()
    plt.clf()
    plt.close()
