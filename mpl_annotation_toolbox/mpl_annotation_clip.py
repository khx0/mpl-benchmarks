#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-03-08
# file: mpl_annotation_clip.py
# tested with python 3.7.6 in conjunction with mpl version 3.2.0
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

def Plot(titlestr, X, outname, outdir, pColors,
         grid = True, saveEPS = False, savePDF = True, savePNG = False, datestamp = True):

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
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 5.0, height = 4.0,
                       lFrac = 0.12, rFrac = 0.65,
                       bFrac = 0.15, tFrac = 0.92)

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
    ax1.set_xlabel(r'x label', fontsize = 8.0)
    ax1.set_ylabel(r'y label', fontsize = 8.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 3.0
    ######################################################################################

    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = pColors[0],
             lw = 1.0,
             label = 'data legend',
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
    mpl_annotation_clip example
    This example illustrates three annotation related findings:
    a) The difference between using xycoords = 'data' and xycoords = 'axes fraction' to 
    place an annotation in a matplotlib plot.
    b) How to place annotations outside of the plot / figure axes. When using
    xcoords = 'axes fraction' this is possible without further ado. For some reason
    (not sure if this is intended) one has to add the keyword
        annotation_clip = False
    when using xycoords = 'data'. Using the clip_on = False keyword, which works to extend
    regular plot commands to regions outside of the axes, does also not seem to work for 
    matplotlib annotations.
    c) How to use the (manually or automatically) set x- and y-limits to convert
    an absolute coordinate placement ('data') into a relative placement ('axes fraction').
    For this conversion we use pyplot's plt.xlim() and plt.ylim() functions.
    '''

    # place a center label using data coordinates
    ax1.annotate('center label in data coords',
                 xy = (500.0, 500.0),
                 xycoords = 'data',
                 fontsize = 6.0,
                 horizontalalignment = 'center',
                 verticalalignment = 'center',
                 zorder = 8)

    ax1.annotate('label crossing the right axis',
                 xy = (800.0, 500.0),
                 xycoords = 'data',
                 fontsize = 6.0,
                 horizontalalignment = 'left',
                 verticalalignment = 'center',
                 zorder = 8)

    # specify the (x, y) position in data coordinates
    xPos_data = 870.0
    yPos_data = 400.0
    ax1.annotate(r"outside label ('data')",
                 xy = (xPos_data, yPos_data),
                 xycoords = 'data',
                 fontsize = 6.0,
                 horizontalalignment = 'left',
                 verticalalignment = 'center',
                 zorder = 8,
                 annotation_clip = False)

    yPos_data = 300.0
    
    # convert absolute ('data') coordinates into relative ('axes fraction') coordinates
    xmin, xmax = plt.xlim() # return the current xlim
    ymin, ymax = plt.ylim()	# return the current ylim
    dx, dy = xmax - xmin, ymax - ymin
    xPos_axes = (xPos_data - xmin) / dx
    yPos_axes = (yPos_data - ymin) / dy

    ax1.annotate(r"outside label ('axes fraction')",
                 xy = (xPos_axes, yPos_axes),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'left',
                 verticalalignment = 'center',
                 zorder = 8)
                 
    # Using xycoords = 'data' and the keyword clip_on = False does not work to place 
    # annotations outside of the axes.
    xPos_data = 870.0
    yPos_data = 200.0
    ax1.annotate(r"outside label ('data') (clip_on = False)",
                 xy = (xPos_data, yPos_data),
                 xycoords = 'data',
                 fontsize = 6.0,
                 horizontalalignment = 'left',
                 verticalalignment = 'center',
                 zorder = 8,
                 clip_on = False)

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

    outname = 'mpl_annotation_clip'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # create dummy data
    nVisPoints = 500
    xVals = np.linspace(120.0, 820.0, nVisPoints)
    yVals = xVals
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    # plot data
    Plot(titlestr = '',
         X = X,
         outname = outname,
         outdir = OUTDIR,
         pColors = ['C0'],
         grid = False)
