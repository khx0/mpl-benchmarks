#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-06-06
# file: pcolor_pseudoColor_plot_logX_linearY.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
##########################################################################################

import sys
sys.path.append('../')
import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter

from mplUtils import getFigureProps
from mplUtils import getPcolorBoxCoordinates
from ticker import cleanFormatter

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def plot_pcolor(X, Y, Z, fProps, xFormat, yFormat, zFormat, zColor, outname, outdir,
                showlabels = True, show_cBar = True, titlestr = None, grid = False, saveSVG = False,
                savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 8.0})
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
        getFigureProps(width = fProps[0], height = fProps[1],
                       lFrac = fProps[2], rFrac = fProps[3],
                       bFrac = fProps[4], tFrac = fProps[5])
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    tick_fontsize = 8.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(tick_fontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(tick_fontsize)

    ax1.tick_params('both', length = 3.0, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 2.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 1.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.0, zorder = 10)

    ######################################################################################
    # labeling
    if titlestr:
        plt.title(titlestr)
    ax1.set_xlabel(xFormat[7], fontsize = 8.0)
    ax1.set_ylabel(yFormat[7], fontsize = 8.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 4.0
    ######################################################################################

    ######################################################################################
    # color map settings
    cMap = zColor[0]
    cNorm = mpl.colors.Normalize(vmin = zColor[1], vmax = zColor[2])
    scalarMap = cm.ScalarMappable(norm = cNorm, cmap = cMap)
    print("Colormap colornorm limits =", scalarMap.get_clim())
    ######################################################################################
    # colorbar
    if show_cBar:
        # add_axes(left, bottom, width, height) all between [0, 1]
        # relative to the figure size
        cax = f.add_axes([0.82, bFrac, 0.03, (tFrac - bFrac)])

        cax.tick_params('both', length = 3.0, width = 0.5, which = 'major')
        cax.tick_params('both', length = 2.0, width = 0.25, which = 'minor')
        cax.tick_params(axis = 'both', which = 'major', pad = 2)

        cb1 = mpl.colorbar.ColorbarBase(cax,
                                        cmap = cMap,
                                        norm = cNorm,
                                        orientation = 'vertical')

#         cb1.set_label(zColor[3],
#                       labelpad = 2.5, fontsize = 6)

        ax1.annotate(zColor[3],
                     xy = (1.175, 1.06),
                     xycoords = 'axes fraction',
                     fontsize = 8.0,
                     horizontalalignment = 'right')

        cb1.outline.set_linewidth(0.5)
        cb1.ax.tick_params(axis = 'y', direction = 'out', which = 'both')
        cb1.ax.tick_params(labelsize = 8.0)

        if (zFormat[0] == 'linear'):
            cb_labels = np.arange(zFormat[1], zFormat[2], zFormat[3])
            cb1.set_ticks(cb_labels)
        # cb1.ax.minorticks_on()

    ax1.pcolormesh(X, Y, Z,
                   cmap = cMap,
                   norm = cNorm,
                   edgecolors = 'none')

    #####################################################################################
    # axis formatting
    if xFormat[0] == 'auto':
        pass
    if xFormat[0] == 'linear':
        ax1.set_xlim(xFormat[1], xFormat[2]) # xmin, xmax
        major_x_ticks = np.arange(xFormat[3], xFormat[4], xFormat[5])
        minor_x_ticks = np.arange(xFormat[3], xFormat[4], xFormat[6])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)

        # manual formatting here:
        # ax1.set_xticklabels([0, 0.5, 1])

    elif xFormat[0] == 'log':
        ax1.set_xscale('log')
        ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 8))
        ax1.xaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 8,
                                    subs = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
        ax1.set_xlim(xFormat[1], xFormat[2]) # xmin, xmax
    else:
        print("Error: Unknown xFormat[0] type encountered.")
        sys.exit(1)
    #####################################################################################
    if yFormat[0] == 'auto':
        pass
    if yFormat[0] == 'linear':
        ax1.set_ylim(yFormat[1], yFormat[2]) # xmin, xmax
        major_y_ticks = np.arange(yFormat[3], yFormat[4], yFormat[5])
        minor_y_ticks = np.arange(yFormat[3], yFormat[4], yFormat[6])
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)

        # manual formatting here:
        # ax1.set_yticklabels([0, 0.5, 1])

    elif yFormat[0] == 'log':
        ax1.set_yscale('log')
        ax1.yaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 5))
        ax1.yaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 5,
                                    subs = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
        for label in ax1.yaxis.get_ticklabels()[1::2]:
            label.set_visible(False)
        ax1.set_ylim(yFormat[1], yFormat[2]) # xmin, xmax
    else:
        print("Error: Unknown yFormat[0] type encountered.")
        sys.exit(1)

    # tick label formatting
    majorFormatter = FuncFormatter(cleanFormatter)
    ax1.yaxis.set_major_formatter(majorFormatter)

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
    if saveSVG:
        cmd = 'pdf2svg ' + os.path.join(outdir, outname + '.pdf') + \
              ' ' + os.path.join(outdir, outname + '.svg')
        os.system(cmd)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':

    outname = 'pcolor_pseudoColor_plot_logX_linearY'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # create synthetic plot data
    n_samples_x = 5
    n_samples_y = 5

    xmin, xmax = 0.1, 1000.0
    xminExp, xmaxExp = np.log10(xmin), np.log10(xmax)
    ymin, ymax = 0.0, 1.0

    xVals = np.logspace(xminExp, xmaxExp, n_samples_x)
    yVals = np.linspace(ymin, ymax, n_samples_y)

    zVals = np.zeros((n_samples_y, n_samples_x))

    for j in range(n_samples_y):         # iterate over y values
        for i in range(n_samples_x):     # iterate over x values
            zVals[i, j] = 0.2 * yVals[i]

    #################################################################################
    print("xVals.shape =", xVals.shape)
    print("yVals.shape =", yVals.shape)
    print("zVals.shape =", zVals.shape)
    assert xVals.shape == yVals.shape, "Shape assertion failed."
    assert zVals.shape == (n_samples_x, n_samples_y), "Shape assertion failed."
    #################################################################################

    xBoxCoords = getPcolorBoxCoordinates(xVals, 'log')
    yBoxCoords = getPcolorBoxCoordinates(yVals)

    assert xBoxCoords.shape == (n_samples_x + 1,), "Shape assertion failed."
    assert yBoxCoords.shape == (n_samples_y + 1,), "Shape assertion failed."

    # call plot function
    fProps = (4.0, 4.0, 0.16, 0.80, 0.20, 0.88)
    xFormat = ('log', 0.23 * 1.0e-1, 4.5 * 1.0e3, 0.0, 1.05, 0.5, 0.1, r'x axis label')
    yFormat = ('linear', -0.16, 1.16, 0.0, 1.05, 0.5, 0.1, r'y axis label')

    cMap = cm.viridis
    zmin = np.min(zVals)
    zmax = np.max(zVals)
    zColor = (cMap, zmin, zmax, r'z label (cbar)')
    zFormat = ('linear', 0.0, 0.21, 0.05)

    outname = plot_pcolor(X = xBoxCoords,
                          Y = yBoxCoords,
                          Z = zVals,
                          fProps = fProps,
                          xFormat = xFormat,
                          yFormat = yFormat,
                          zFormat = zFormat,
                          zColor = zColor,
                          outname = outname,
                          outdir = OUTDIR)
