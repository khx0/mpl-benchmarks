#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-02-15
# file: mpl_legend_scatter_markerscale_minimal.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.4
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    # fix random seed for reproducibility
    np.random.seed(983456789)

    # create synthetic plot data
    n_datapoints = 500
    xVals = np.random.normal(0.5, 0.15, n_datapoints)
    yVals = np.random.normal(0.5, 0.2, n_datapoints)
    X = np.zeros((n_datapoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    outname = 'mpl_legend_scatter_markerscale_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    f, ax1 = plt.subplots(1)
    f.set_size_inches(3.0, 3.0)

    ax1.scatter(X[:, 0], X[:, 1],
                s = 1.5,
                marker = 'o',
                facecolors = 'C0',
                edgecolors = 'None',
                alpha = 1.0,
                linewidth = 0.0,
                zorder = 3,
                label = r'scatter label')

    ####################################################
    ####################################################
    # legend handling
    leg = ax1.legend(handlelength = 0.5,
                     markerscale = 2.5)

    '''
    If the marker symbol of scatter plot is used
    with zero linewidth, the symbol size for the
    legend can still be adjusted using the
    markerscale keyword of the legend object itself.
    '''

    leg.draw_frame(False)
    ####################################################
    ####################################################

    outname += '_' + today
    f.savefig(os.path.join(OUTDIR, outname + '.pdf'),
              dpi = 300,
              transparent = True)

    plt.cla()
    plt.clf()
    plt.close()
