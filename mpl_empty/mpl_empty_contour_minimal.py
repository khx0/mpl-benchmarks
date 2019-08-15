#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-08-15
# file: mpl_empty_contour_minimal.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.1
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
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    outname = 'mpl_empty_contour_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today # set datestamp

	# create data
    nDataPoints = 500
    radius = 50.0
    angles = np.linspace(0.0, 2.0 * np.pi, nDataPoints)
    xVals = radius * np.cos(angles)
    yVals = radius * np.sin(angles)

    X = np.zeros((nDataPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    print("X.shape =", X.shape)

    pColors = ['k']

    # minimal plot
    f, ax1 = plt.subplots(1)
    f.set_size_inches(2.0, 2.0)

    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = pColors[0],
             lw = 1.0,
             clip_on = True,
             zorder = 1)

    ax1.set_xlim(-55.0, 55.0)
    ax1.set_ylim(-55.0, 55.0)

    ax1.set_xticks([])
    ax1.set_yticks([])

    plt.axis('off')

    # save plot to file
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    plt.show()

    plt.cla()
    plt.clf()
    plt.close()
