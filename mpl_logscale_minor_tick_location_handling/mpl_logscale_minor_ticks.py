#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-05-28
# file: mpl_logscale_minor_ticks.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
# requires: pdf2svg installed
##########################################################################################

"""
Benchmark matplotlib script illustrating how to set a lower and upper limit for the
minor tick locations in logarithmic axis scaling independent of the axis limits.
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

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def getFigureProps(width, height, lFrac = 0.17, rFrac = 0.9, bFrac = 0.17, tFrac = 0.9):
    '''
    True size scaling auxiliary function to setup mpl plots with a desired size.
    Specify widht and height in cm.
    lFrac = left fraction   in [0, 1]
    rFrac = right fraction  in [0, 1]
    bFrac = bottom fraction in [0, 1]
    tFrac = top fraction    in [0, 1]
    returns:
        fWidth = figure width
        fHeight = figure height
    These figure width and height values can then be used to create a figure instance
    of the desired size, such that the actual plotting canvas has the specified
    target width and height, as provided by the input parameters of this function.
    '''
    axesWidth = width / 2.54    # convert to inches
    axesHeight = height / 2.54  # convert to inches
    fWidth = axesWidth / (rFrac - lFrac)
    fHeight = axesHeight / (tFrac - bFrac)
    return fWidth, fHeight, lFrac, rFrac, bFrac, tFrac

def Plot(type, X, outname, outdir, pColors, showlabels = True, titlestr = None,
         grid = False, savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 9.0})
    mpl.rc('axes', linewidth = 0.5)

    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 5.5, height = 4.5,
                       lFrac = 0.16, rFrac = 0.85,
                       bFrac = 0.17, tFrac = 0.9)

    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################

    major_y_ticks = np.arange(0.0, 1.1, 0.5)
    minor_y_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)

    labelfontsize = 8.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 2.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.5, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 1.5)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.5, zorder = 10)
    ######################################################################################
    # labeling
    if titlestr:
        plt.title(titlestr)
    ax1.set_xlabel(r'x label', fontsize = 10.0)
    ax1.set_ylabel(r'y label', fontsize = 10.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 2.0
    ######################################################################################
    # plot data

    ax1.plot(X[:, 0], X[:, 1],
             color = pColors[0],
             alpha = 1.0,
             lw = 1.0,
             zorder = 2,
             label = r'plot label')

    ######################################################################################
    # legend
    leg = ax1.legend(loc = 'upper left',
                     handlelength = 1.5,
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)

    ######################################################################################
    # set plot range and scale

    ax1.set_xscale('log')

    ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 10))

    if type == 'A':

        ax1.xaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 10,
                                    subs = np.arange(2, 10) * 0.1))

    elif type == 'B':

        locmin = mpl.ticker.LogLocator(base = 10.0,
                                       subs = np.arange(2, 10) * 0.1,
                                       numticks = 100)
        locminArray = locmin.tick_values(1.0e-10, 9.0e-8)
        # use to manually set the range for the minor ticks in logarithmic scaling
        print(locminArray)
        ax1.set_xticks(locminArray, minor = True)

    else:
        print("Error: Unknown case encountered.")
        sys.exit(1)

    ax1.set_xlim(5.0e-13, 2.5e-6)

    ###############################################################################
    # uncomment the two lines below for only using every second x-tick major label
    #     for label in ax1.xaxis.get_ticklabels()[::2]:
    #         label.set_visible(False)
    ###############################################################################

    ax1.set_axisbelow(False)

    ax1.set_ylim(-0.02, 1.05)
    ax1.set_yticklabels([0, 0.5, 1])

    ######################################################################################
    # grid options
    if grid:
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major',
                 linewidth = 0.4)
        ax1.grid(True)
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor',
                 linewidth = 0.2)
        ax1.grid(True, which = 'minor')
    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + today
    if savePDF: # save to file using pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':

    convert2svg = False

    # create data to plot
    n_vispoints = 1000
    xValues = np.logspace(-13, -5, n_vispoints)
    yValues = np.array([x / (1.0e-9 + x) for x in xValues])
    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xValues
    X[:, 1] = yValues

    # plotting
    colorVals = ['C0']

    outname = 'mpl_logscale_minor_tick_location_handling_version_A'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    returnname = Plot(type = 'A',
                      X = X,
                      outname = outname,
                      outdir = OUTDIR,
                      pColors = colorVals)

    if convert2svg:
        cmd = 'pdf2svg ' + os.path.join(OUTDIR, returnname + '.pdf') + \
            ' ' + os.path.join(OUTDIR, returnname + '.svg')
        os.system(cmd)

    outname = 'mpl_logscale_minor_tick_location_handling_version_B'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    returnname = Plot(type = 'B',
                      X = X,
                      outname = outname,
                      outdir = OUTDIR,
                      pColors = colorVals)

    if convert2svg:
        cmd = 'pdf2svg ' + os.path.join(OUTDIR, returnname + '.pdf') + \
            ' ' + os.path.join(OUTDIR, returnname + '.svg')
        os.system(cmd)
