#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-05-30
# file: mpl_legend_manually_set_size.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.0
##########################################################################################

import sys
sys.path.append('../')
import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend
from matplotlib import ticker

from mplUtils import getFigureProps

now = datetime.datetime.now()
now = "{}-{}-{}".format(str(now.year), str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def Plot(titlestr, X, Y, Z, params, labels, outname, outdir, pColors,
         grid = False, saveSVG = False, savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 5.0})
    mpl.rc('axes', linewidth = 0.5)

    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 5.5, height = 4.0,
                       lFrac = 0.12, rFrac = 0.70,
                       bFrac = 0.17, tFrac = 0.9)
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

    ax1.tick_params(axis = 'x', which = 'major', pad = 1.5)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.5, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'x label', fontsize = 8.0)
    ax1.set_ylabel(r'y label', fontsize = 8.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 4.0
    ######################################################################################
    # plot data

    ax1.plot(X[:, 0], X[:, 1],
            color = pColors[0],
            alpha = 1.0,
            lw = 0.3,
            zorder = 2,
            label = labels[0])

    ax1.scatter(Y[:, 0], Y[:, 1],
                s = 0.75,
                marker = 'o',
                facecolors = pColors[1],
                edgecolors = 'None',
                alpha = 1.0,
                linewidth = 0.0,
                zorder = 3,
                label = labels[1])

    ax1.scatter(Z[:, 0], Z[:, 1],
                s = 3.0,
                marker = 'o',
                facecolors = 'None',
                edgecolors = pColors[2],
                alpha = 1.0,
                linewidth = 0.3,
                zorder = 3,
                label = labels[2])

    ######################################################################################
    # legend

    '''
    The core idea is to manually set the width of legend lines and legend marker symbols
    independent of their actual plot size. This is particular helpful, when
    the actual drawn size is rather small for figure composition reasons, but
    you still want your legend to be clearly and distinctly visible.
    There are the following things to consider:

    (i)  For line elements, use the legobj.set_linewidth(2.0) command below.
    (ii) For marker symbols use the markerscale keyword in the legend object itself.

    For scatter points, be aware that they can be composed of a marker component
    and a line (also depending on the marker type).
    For example the markertype '+' is only controlled by a linewidth, but not a
    markerscale. For the markertype 'o' you can have both, but can also set
    the linewidth to zero as in this example above.
    '''

    leg = ax1.legend(bbox_to_anchor = [1.0, 1.0],
                     loc = 'upper left',
                     handlelength = 1.5,
                     scatterpoints = 1,
                     markerscale = 3.0,
                     ncol = 1)

    # set the linewidth of each legend object
    for legobj in leg.legendHandles:
        legobj.set_linewidth(1.0)

    leg.draw_frame(False)

    ax1.set_axisbelow(False)

    for spine in ax1.spines.values(): # ax1.spines is a dictionary
        spine.set_zorder(10)

    ######################################################################################
    # set plot range and scale
    # USE DEFAULTS HERE
    ######################################################################################
    # grid options
    if grid:
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major',
                 linewidth = 0.4)
        ax1.grid('on')
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor',
                 linewidth = 0.2)
        ax1.grid('on', which = 'minor')
    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + now
    if savePDF: # save to file using pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    if saveSVG:
        cmd = 'pdf2svg ' + os.path.join(OUTDIR, outname + '.pdf') + \
              ' ' + os.path.join(OUTDIR, outname + '.svg')
        print(cmd)
        os.system(cmd)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':

    # fix random seed for reproducibility
    np.random.seed(223456789)

    # create synthetic plot data
    nDatapoints = 200
    xVals = np.linspace(0.0, 1.0, nDatapoints)
    yVals = np.array([x for x in xVals])
    X = np.zeros((nDatapoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    xVals = np.random.normal(0.5, 0.15, nDatapoints)
    yVals = np.random.normal(0.5, 0.20, nDatapoints)
    Y = np.zeros((nDatapoints, 2))
    Y[:, 0] = xVals
    Y[:, 1] = yVals

    xVals = np.random.normal(0.5, 0.20, nDatapoints)
    yVals = np.random.normal(0.5, 0.15, nDatapoints)
    Z = np.zeros((nDatapoints, 2))
    Z[:, 0] = xVals
    Z[:, 1] = yVals

    # call plot routine
    pColors = ['C3', 'C0', 'C2']

    labels = [r'data line',
              r'scatter points (only marker)',
              r'scatter points (only line)']

    outname = 'mpl_legend_manually_set_size'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outname = Plot(titlestr = '',
                   X = X,
                   Y = Y,
                   Z = Z,
                   params = [],
                   labels = labels,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   grid = False)
