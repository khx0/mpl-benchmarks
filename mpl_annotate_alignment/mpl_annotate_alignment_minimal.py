#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-05-09
# file: mpl_annotate_alignment_minimal.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
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

    outname = 'mpl_annotate_alignment_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    # create synthetic data
    n_vispoints = 500
    xVals = np.linspace(0.0, 1.0, n_vispoints)
    yVals = np.array([np.sin(x) ** 3 for x in xVals])
    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    # minimal plot
    f, ax1 = plt.subplots(1)
    f.subplots_adjust(right = 0.70)

    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = 'C0',
             lw = 1.0,
             label = 'data',
             clip_on = False,
             zorder = 1)

    leg = ax1.legend(handlelength = 1.5,
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)

    # annotations
    '''
    This example uses relative coordinates for the placement of annotations.
    This is realized by setting xycoords = 'axes fraction'. 
    Then the specified xy position is set relative to the axis canvas, 
    where both the x and y position is specified by their fractional value between [0, 1].
    Additionally this example demonstrates the use of alignment specifications,
    using the "horizontalalignment" and "verticalalignment" keywords.
    For the horizontal alignment keyword use 'left', 'right' or 'center' and
    for the vertical alignment keyword use 'top', 'center' or 'bottom', respectively.
    '''

    ax1.annotate('upper right label',
                 xy = (1.0, 1.03),
                 xycoords = 'axes fraction',
                 horizontalalignment = 'right',
                 zorder = 8)

    ax1.annotate('upper left label',
                 xy = (0.0, 1.03),
                 xycoords = 'axes fraction',
                 horizontalalignment = 'left',
                 zorder = 8)

    ax1.annotate('center label',
                 xy = (0.5, 0.5),
                 xycoords = 'axes fraction',
                 horizontalalignment = 'center',
                 verticalalignment = 'center',
                 zorder = 8)

    ax1.annotate('right margin top label',
                 xy = (1.02, 1.0),
                 xycoords = 'axes fraction',
                 horizontalalignment = 'left',
                 verticalalignment = 'top',
                 zorder = 8)

    ax1.annotate('right margin bottom label',
                 xy = (1.02, 0.0),
                 xycoords = 'axes fraction',
                 horizontalalignment = 'left',
                 verticalalignment = 'bottom',
                 zorder = 8)

    # set plot range and scale
    ax1.set_xlim(-0.05, 1.05)

    # save plot to file
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
