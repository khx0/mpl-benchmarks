#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-07-15
# file: mpl_logscale_minor_ticks_minimal.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.1
##########################################################################################

"""
(Minimal) Benchmark matplotlib script illustrating how to set a lower and upper limit
for the minor tick locations in logarithmic axis scaling independent of the axis limits.
This script shows how to do this for a logarithmic x-axis.
Version A uses the default behavior from the ticker.LogLocator class
whereas version B manually crops the minor ticks, such that the newly chosen minor tick
locations become independent from the ax1.set_xlim(xmin, xmax) satement.
For aesthetic reasons I often prefer not to have minor tick marks towards
both the left and right margin of a chosen log-axis.
In general, I typically want to control the range for ticks indepedent of the view range,
which is straight forward in matplotlibs normal view, but a little more challenging
when using logarithmic axis scaling.
"""

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import LogFormatter

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

now = datetime.datetime.now()
now = "{}-{}-{}".format(str(now.year), str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def plot_minimal_version_A(X, filename):

    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'x label', fontsize = 10.0)
    ax1.set_ylabel(r'y label', fontsize = 10.0)
    ax1.xaxis.labelpad = 4.0
    ax1.yaxis.labelpad = 4.0

    ax1.plot(X[:, 0], X[:, 1],
             color = 'C0',
             alpha = 1.0,
             lw = 1.0)

    # set plot range and scale

    ax1.set_xscale('log')

    ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 10))

    ax1.xaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 10,
                                subs = np.arange(2, 10) * 0.1))

    ax1.set_xlim(5.0e-13, 2.5e-6)

    ax1.set_ylim(-0.02, 1.05)
    major_y_ticks = np.arange(0.0, 1.1, 0.5)
    minor_y_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    ax1.set_yticklabels([0, 0.5, 1])

    ax1.set_axisbelow(False)

    filename += '_' + now
    f.savefig(os.path.join(OUTDIR, filename + '.pdf'),
              dpi = 300,
              transparent = True)

    # close handles
    plt.cla()
    plt.clf()
    plt.close()

    return None

def plot_minimal_version_B(X, filename):

    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'x label', fontsize = 10.0)
    ax1.set_ylabel(r'y label', fontsize = 10.0)
    ax1.xaxis.labelpad = 4.0
    ax1.yaxis.labelpad = 4.0

    ax1.plot(X[:, 0], X[:, 1],
             color = 'C0',
             alpha = 1.0,
             lw = 1.0)

    # set plot range and scale

    ax1.set_xscale('log')

    ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 10))

    locmin = mpl.ticker.LogLocator(base = 10.0,
                                   subs = np.arange(2, 10) * 0.1,
                                   numticks = 100)

    locminArray = locmin.tick_values(1.0e-10, 9.0e-8)
    # use to manually set the range for the minor ticks in logarithmic scaling
    print(locminArray)
    ax1.set_xticks(locminArray, minor = True)

    ax1.set_xlim(5.0e-13, 2.5e-6)

    ax1.set_ylim(-0.02, 1.05)
    major_y_ticks = np.arange(0.0, 1.1, 0.5)
    minor_y_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    ax1.set_yticklabels([0, 0.5, 1])

    ax1.set_axisbelow(False)

    filename += '_' + now
    f.savefig(os.path.join(OUTDIR, filename + '.pdf'),
              dpi = 300,
              transparent = True)

    # close handles
    plt.cla()
    plt.clf()
    plt.close()

    return None

if __name__ == '__main__':

    # create data to plot
    nVisPoints = 1000
    xValues = np.logspace(-13, -5, nVisPoints)
    yValues = np.array([x / (1.0e-9 + x) for x in xValues])
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xValues
    X[:, 1] = yValues

    outname = 'mpl_logscale_minor_tick_location_handling_minimal_version_A'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    plot_minimal_version_A(X, outname)

    outname = 'mpl_logscale_minor_tick_location_handling_minimal_version_B'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    plot_minimal_version_B(X, outname)
