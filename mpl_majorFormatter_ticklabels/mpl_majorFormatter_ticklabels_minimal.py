#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-02-23
# file: mpl_majorFormatter_ticklabels_minimal.py
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

    # create synthetic data
    n_vispoints = 800
    xVals = np.linspace(0.0, 1.0, n_vispoints)
    yVals = np.sin(2.0 * np.pi * xVals)

    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    # file i/o
    outname = 'mpl_majorFormatter_ticklabels_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    # plot
    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})

    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'x label')
    ax1.set_ylabel(r'y label')

    ax1.plot(X[:, 0], X[:, 1],
             color = 'C0',
             alpha = 1.0)

    # tick label formatting
    from matplotlib.ticker import FormatStrFormatter
    majorFormatter = FormatStrFormatter('%g')
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax1.yaxis.set_major_formatter(majorFormatter)

    # save to file
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf', dpi = 300, transparent = True)
    f.savefig(os.path.join(OUTDIR, outname) + '.png', dpi = 600, transparent = True)

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
