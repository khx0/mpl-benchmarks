#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-06-05
# file: mpl_margins_minimal.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
##########################################################################################

##########################################################################################
# Matplolib's pyplot.margins command:
#
# Syntax used in this script: plt.margins(x = xMargin, y = yMargin)
#
# The margin command will add padding to each axis according to the simple rule:
# additional axis padding = margin * dataInterval
# Hence the axis limits using the plt.margins command are the following:
# dataRangeX = xMax - xMin
# dataRangeY = yMax - yMin
# xPadding = xMargin * dataRangeX
# yPadding = yMargin * dataRangeY
# limits x: [xMin - xPadding, xMax + xPadding]
# limits y: [yMin - yPadding, yMax + yPadding]
# By default the padding is symmetrical in both directions of a given axis.
#
# The plt.margins(*) command is superseded by the ax1.set_xlim(*) and ax1.set_ylim(*)
# commands (regardless of the order of occurrence if both are present in a plot script).
# This makes sense since it is part of matplotlib's autoscaling tools, whereas the
# set_xlim and set_ylim commands are explicit absolute commands to set the axis limits.
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    xMargin, yMargin = 0.073, 0.073
    outname = f'mpl_margins_D_xMargin_{xMargin}_yMargin_{yMargin}_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    # create synthetic data
    n_vispoints = 300
    xVals = np.linspace(0.0, 1.0, n_vispoints)
    yVals = np.array([x for x in xVals])
    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    # minimal plot
    f, ax1 = plt.subplots(1)

    # labeling
    ax1.set_xlabel(r'x label')
    ax1.set_ylabel(r'y label')

    # plotting
    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = 'C0',
             lw = 1.0,
             label = 'data',
             clip_on = True,
             zorder = 1)

    # annotation
    label_str = f'x margin: {xMargin}\ny margin: {yMargin}'

    ax1.annotate(label_str,
                 xy = (0.0, 1.03),
                 xycoords = 'axes fraction',
                 horizontalalignment = 'left',
                 zorder = 8)

    # legend
    leg = ax1.legend(handlelength = 1.35,
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)

    # set axes limits
    # use plt.margins instead of absolute set_xlim and set_ylim axis limit specifications.
    plt.margins(x = xMargin, y = yMargin)

    # save plot to file
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
