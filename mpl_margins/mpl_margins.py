#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-03-12
# file: mpl_margins.py
# tested with python 3.7.6 in conjunction with mpl version 3.2.0
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
from matplotlib.pyplot import legend

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
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

def Plot(titlestr, X, margins, outname, outdir, pColors,
         grid = True, saveEPS = False, savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.0})
    mpl.rc('axes', linewidth = 0.5)

    ######################################################################################
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'Helvetica'
    # the above two lines could also be replaced by the single line below
    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})

    mpl.rcParams['pdf.fonttype'] = 42
    ######################################################################################

    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 5.0, height = 4.0,
                       lFrac = 0.20, rFrac = 0.90, bFrac = 0.20, tFrac = 0.85)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)

    ######################################################################################
    labelfontsize = 6.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 2.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.5, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'x label', fontsize = 6.0)
    ax1.set_ylabel(r'y label', fontsize = 6.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 3.0
    ######################################################################################

    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = pColors[0],
             lw = 1.0,
             label = 'data',
             clip_on = True,
             zorder = 1)

    # legend
    leg = ax1.legend(handlelength = 1.35,
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)

    ######################################################################################
    # annotations

    labelString = 'x margin: {}\ny margin: {}'.format(margins[0], margins[1])

    ax1.annotate(labelString,
                 xy = (0.0, 1.03),
                 xycoords = 'axes fraction',
                 fontsize = 4.0,
                 horizontalalignment = 'left',
                 zorder = 8)

    ######################################################################################
    # set plot range, scale and padding

    # use plt.margins instead of absolute set_xlim and set_ylim axis limit specifications.
    plt.margins(x = margins[0], y = margins[1])

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
    return None

if __name__ == '__main__':

    # create dummy data
    nVisPoints = 300
    xVals = np.linspace(0.0, 1.0, nVisPoints)
    yVals = np.array([x for x in xVals])
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################

    xMargin, yMargin = 0.5, 0.5
    outname = f'mpl_margins_A_xMargin_{xMargin}_yMargin_{yMargin}y'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # plot data
    Plot(titlestr = '',
         X = X,
         margins = [xMargin, yMargin],
         outname = outname,
         outdir = OUTDIR,
         pColors = ['C0'],
         grid = False)

    ######################################################################################

    xMargin, yMargin = 0.0, 0.25
    outname = f'mpl_margins_B_xMargin_{xMargin}_yMargin_{yMargin}'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # plot data
    Plot(titlestr = '',
         X = X,
         margins = [xMargin, yMargin],
         outname = outname,
         outdir = OUTDIR,
         pColors = ['C0'],
         grid = False)

    ######################################################################################

    xMargin, yMargin = 0.25, 0.0
    outname = f'mpl_margins_C_xMargin_{xMargin}_yMargin_{yMargin}'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # plot data
    Plot(titlestr = '',
         X = X,
         margins = [xMargin, yMargin],
         outname = outname,
         outdir = OUTDIR,
         pColors = ['C0'],
         grid = False)

    ######################################################################################

    xMargin, yMargin = 0.073, 0.073
    outname = f'mpl_margins_D_xMargin_{xMargin}_yMargin_{yMargin}'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # plot data
    Plot(titlestr = '',
         X = X,
         margins = [xMargin, yMargin],
         outname = outname,
         outdir = OUTDIR,
         pColors = ['C0'],
         grid = False)
