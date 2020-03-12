#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-03-12
# file: mpl_logscale_minor_ticks_minimal_explicit.py
# tested with python 3.7.6 in conjunction with mpl version 3.2.0
##########################################################################################

"""
(Minimal) Benchmark matplotlib script illustrating how to set a lower and upper limit
for the minor tick locations in logarithmic axis scaling independent of the axis limits.
This script shows how to do this for a logarithmic x-axis.
In this version C script, the major ticks are set using the ticker.LogLocator class.
The minor ticks are created using the getLogTicksBase10 function from the ticker module.
In this way the minor ticks are cropped, such that the newly chosen minor tick
locations become independent from the ax1.set_xlim(xmin, xmax) satement.
For aesthetic reasons I often prefer not to have minor tick marks towards
both the left and right margin of a chosen log-axis.
In general, I typically want to control the range for ticks indepedent of the view range,
which is straight forward in matplotlibs normal view, but a little more challenging
when using logarithmic axis scaling.
"""

import sys
sys.path.append('../')
import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import LogFormatter

from ticker import getLogTicksBase10

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def plot_minimal(X, filename):

    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'x label', fontsize = 10.0)
    ax1.set_ylabel(r'y label', fontsize = 10.0)
    ax1.xaxis.labelpad = 4.0
    ax1.yaxis.labelpad = 4.0

    ax1.plot(X[:, 0], X[:, 1],
             color = 'C0',
             alpha = 1.0,
             lw = 1.0)

    ######################################################################################
    ######################################################################################
    # set plot range and scale
    ax1.set_xscale('log')

    # 1 set major ticks using LogLocator
    ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 10))

    # 2 create ticks manually (explicit)
    xMinorTicks = getLogTicksBase10(1.0e-12, 1.0e-6)

    # 3 set minor ticks using the FixedLocator
    ax1.xaxis.set_minor_locator(ticker.FixedLocator((xMinorTicks)))

    # 4 use the NullFormatter for minor ticks without tick labels
    ax1.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())

    ax1.set_xlim(5.0e-13, 2.5e-6)
    ######################################################################################
    ######################################################################################

    ax1.set_ylim(-0.02, 1.05)
    major_y_ticks = np.arange(0.0, 1.1, 0.5)
    minor_y_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    ax1.set_yticklabels([0, 0.5, 1])

    ax1.set_axisbelow(False)

    filename += '_' + today
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

    outname = 'mpl_logscale_minor_tick_location_handling_minimal_version_C_explicit'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    plot_minimal(X, outname)
