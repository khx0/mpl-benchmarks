#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-05-09
# file: mpl_annotate_alignment.py
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

def Plot(X, outname, outdir, pColors, titlestr = None,
         grid = False, saveEPS = False, savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.5})
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
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'
    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 5.0, height = 4.0,
                       lFrac = 0.15, rFrac = 0.70,
                       bFrac = 0.20, tFrac = 0.85)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    labelfontsize = 8.0
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
    if titlestr:
        plt.title(titlestr)
    ax1.set_xlabel(r'x label', fontsize = 8.0)
    ax1.set_ylabel(r'y label', fontsize = 8.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 3.0
    ######################################################################################

    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = pColors[0],
             lw = 1.0,
             label = 'data',
             clip_on = False,
             zorder = 1)

    # legend
    leg = ax1.legend(handlelength = 1.35,
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
                 fontsize = 6.0,
                 horizontalalignment = 'right',
                 zorder = 8)

    ax1.annotate('upper left label',
                 xy = (0.0, 1.03),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'left',
                 zorder = 8)

    ax1.annotate('center label',
                 xy = (0.5, 0.5),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'center',
                 verticalalignment = 'center',
                 zorder = 8)

    ax1.annotate('right margin top label',
                 xy = (1.02, 1.0),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'left',
                 verticalalignment = 'top',
                 zorder = 8)

    ax1.annotate('right margin bottom label',
                 xy = (1.02, 0.0),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'left',
                 verticalalignment = 'bottom',
                 zorder = 8)

    ######################################################################################
    # set plot range (axis limits)
    ax1.set_xlim(-0.05, 1.05)
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

    outname = 'mpl_annotate_alignment'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # create data
    n_vispoints = 500
    xVals = np.linspace(0.0, 1.0, n_vispoints)
    yVals = np.sin(xVals) ** 3
    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    # plot data
    Plot(X = X,
         outname = outname,
         outdir = OUTDIR,
         pColors = ['C0'])
