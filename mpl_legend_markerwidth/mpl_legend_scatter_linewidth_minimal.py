#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-05-30
# file: mpl_legend_scatter_linewidth_minimal.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.0
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend

now = datetime.datetime.now()
now = "{}-{}-{}".format(str(now.year), str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    # fix random seed for reproducibility
    np.random.seed(123456789)

    # create synthetic plot data
    nDatapoints = 500
    xVals = np.random.normal(0.5, 0.15, nDatapoints)
    yVals = np.random.normal(0.5, 0.2, nDatapoints)
    X = np.zeros((nDatapoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    outname = 'mpl_legend_scatter_linewidth_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    f, ax1 = plt.subplots(1)
    f.set_size_inches(3.0, 3.0)

    ax1.scatter(X[:, 0], X[:, 1],
                s = 3.0,
                marker = 'o',
                facecolors = 'None',
                edgecolors = 'C0',
                alpha = 1.0,
                linewidth = 0.2,
                zorder = 3,
                label = r'scatter label')

    ####################################################
    ####################################################
    # legend handling
    leg = ax1.legend(handlelength = 0.1,
                     markerscale = 3.5)

    '''
    The linewidth of the legend object can be manually
    adjusted by the two code lines below, using the
    legobj.set_linewidth(WIDTH)
    function call.
    Here this is used to adjust the linewidth of the
    scatter symbols.
    '''

    # set the linewidth of the legend object
    for legobj in leg.legendHandles:
        legobj.set_linewidth(1.0)

    leg.draw_frame(False)
    ####################################################
    ####################################################

    outname += '_' + now
    f.savefig(os.path.join(OUTDIR, outname + '.pdf'),
              dpi = 300,
              transparent = True)

    plt.cla()
    plt.clf()
    plt.close()
