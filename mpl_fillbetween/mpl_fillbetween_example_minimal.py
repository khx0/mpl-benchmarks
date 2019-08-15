#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-08-15
# file: mpl_fillbetween_example_minimal.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.1
##########################################################################################

'''
Minimal example to illustrate the use of matplotlib's fillbetween function.
Here illustrated by filling the area under a normal distribution.
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

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    nPoints = 400
    xVals = np.linspace(-6.0, 6.0, nPoints)
    yVals = norm.pdf(xVals, 0.0, 1.0)
    X = np.zeros((nPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    outname = 'mpl_fillbetween_example_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today # set datestamp

    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'x label', fontsize = 8.0)
    ax1.set_ylabel(r'y label', fontsize = 8.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 2.0

    ax1.fill_between(X[:, 0], 0, X[:, 1],
                     color = 'C0',
                     alpha = 0.5,
                     lw = 0.0)

    ax1.plot(X[:, 0], X[:, 1],
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
