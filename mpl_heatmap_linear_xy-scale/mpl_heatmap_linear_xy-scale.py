#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-08-22
# file: mpl_heatmap_linear_xy-scale.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.1
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
import matplotlib.colors as colors
import matplotlib.cm as cm

from mplUtils import getFigureProps
from mplUtils import getPcolorBoxCoordinates

from axisPadding import getLinearAxisPadding

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def plot_pcolor(X, Y, Z, titlestr, params,
    fProps, xFormatObj, yFormatObj, zFormat, zColor, show_cBar,
    outname, outdir, showlabels,
    grid = False, saveSVG = False, savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 8.0})
    mpl.rc('axes', linewidth = 0.5)

    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}

    mpl.rcParams.update(fontparams)

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
    plt.title(titlestr)
    ax1.set_xlabel(xFormatObj[2], fontsize = 8.0)
    ax1.set_ylabel(yFormatObj[2], fontsize = 8.0)
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
        ##########################################################
        # add_axes(left, bottom, width, height) all between [0, 1]
        # relative to the figure size
        ##########################################################
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
                     fontsize = 6.0,
                     horizontalalignment = 'right')

        cb1.outline.set_linewidth(0.5)
        cb1.ax.tick_params(axis = 'y', direction = 'out', which = 'both')
        cb1.ax.tick_params(labelsize = 6.0)

        if (zFormat[0] == 'linear'):
            cb_labels = np.arange(zFormat[1], zFormat[2], zFormat[3])
            cb1.set_ticks(cb_labels)
        # cb1.ax.minorticks_on()

    ax1.pcolormesh(X, Y, Z,
                   cmap = cMap,
                   norm = cNorm,
                   edgecolors = 'none')

    ######################################################################################
    # z-max / z-min annotation

    str1 = r"$z_{\mathrm{max}} = %.5f \,$" %(params[1])
    str2 = r"$z_{\mathrm{min}} = %.5f \,$" %(params[0])

    ax1.annotate(str1,
                 xy = (0.0, 1.10),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'left')

    ax1.annotate(str2,
                 xy = (0.0, 1.025),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'left')

    ######################################################################################
    # axis formatting
    if (xFormatObj[0] == 'auto'):
        pass
    if (xFormatObj[0] == 'linear'):
        xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor = xFormatObj[1]
        ax1.set_xlim(xmin, xmax)
        major_x_ticks = np.arange(xTicksMin, xTicksMax, dxMajor)
        minor_x_ticks = np.arange(xTicksMin, xTicksMax, dxMinor)
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)

    elif (xFormatObj[0] == 'log'):
        ax1.set_xscale('log')
        xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor = xFormatObj[1]
        ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 8))
        ax1.xaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 8,
                                    subs = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
#         for label in ax1.xaxis.get_ticklabels()[1::2]:
#             label.set_visible(False)
        ax1.set_xlim(xmin, xmax)
    else:
        print("Error: Unknown xFormatObj[0] type encountered.")
        sys.exit(1)
    ######################################################################################
    if (yFormatObj[0] == 'auto'):
        pass
    if (yFormatObj[0] == 'linear'):
        ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor = yFormatObj[1]
        ax1.set_ylim(ymin, ymax)
        major_y_ticks = np.arange(yTicksMin, yTicksMax, dyMajor)
        minor_y_ticks = np.arange(yTicksMin, yTicksMax, dyMinor)
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)

    elif (yFormatObj[0] == 'log'):
        ax1.set_yscale('log')
        ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor = yFormatObj[1]
        ax1.yaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 8))
        ax1.yaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 8,
                                    subs = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
#         for label in ax1.yaxis.get_ticklabels()[1::2]:
#             label.set_visible(False)
        ax1.set_ylim(ymin, ymax)
    else:
        print("Error: Unknown yFormat[0] type encountered.")
        sys.exit(1)

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
        cmd = 'pdf2svg ' + os.path.join(OUTDIR, outname + '.pdf') + \
              ' ' + os.path.join(OUTDIR, outname + '.svg')
        os.system(cmd)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':

    basename = 'mpl_heatmap_linear_xy-scale'

    outnameAbs = basename + '_absZscale'
    outnameAbs += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    outnameRel = basename + '_relZscale'
    outnameRel += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    ######################################################################################
    # create dummy data

    nDataPoints = 30
    Z = np.zeros((nDataPoints, nDataPoints))
    print('Z.shape =', Z.shape)

    xVals = np.linspace(0.0, 1.0, nDataPoints)
    yVals = np.linspace(-1.0, 1.0, nDataPoints)

    # fill Z matrix
    for i in range(len(yVals)):
        for j in range(len(xVals)):
            Z[i, j] = np.sin(np.pi * xVals[j]) * np.sin(np.pi * yVals[i])

    Z_min = np.min(Z)
    Z_max = np.max(Z)
    print("mininmal z value =", Z_min)
    print("maximal  z value =", Z_max)
    ######################################################################################

    xBoxCoords = getPcolorBoxCoordinates(xVals)
    yBoxCoords = getPcolorBoxCoordinates(yVals)

    assert xBoxCoords.shape == (len(xVals) + 1,), "Error: Shape assertion failed."
    assert yBoxCoords.shape == (len(yVals) + 1,), "Error: Shape assertion failed."

    # call plot function
    fProps = [4.0, 4.0, 0.20, 0.80, 0.20, 0.88]

    # left and right axis padding fraction
    paddingFraction = 0.035

    xminData = 0.0
    xmaxData = 1.0
    xmin, xmax = getLinearAxisPadding(xminData, xmaxData, paddingFraction)

    yminData = -1.0
    ymaxData = 1.0
    ymin, ymax = getLinearAxisPadding(yminData, ymaxData, paddingFraction)

    xFormat = (xmin, xmax, 0.0, 1.05, 0.5, 0.1)
    xFormatObj = ['linear', xFormat, r'x label $x$']

    yFormat = (ymin, ymax, -1.0, 1.05, 0.5, 0.1)
    yFormatObj = ['linear', yFormat, r'y label $y$']

    # absolute scaling
    cMap = cm.viridis # cm.plasma
    zmin = -1.0
    zmax = 1.0
    zColor = [cMap, zmin, zmax, r'z label $\, z$']
    zFormat = ['linear', -1.0, 1.05, 0.5]

    plot_pcolor(X = xBoxCoords,
                Y = yBoxCoords,
                Z = Z,
                titlestr = '',
                params = [Z_min, Z_max],
                fProps = fProps,
                xFormatObj = xFormatObj,
                yFormatObj = yFormatObj,
                zFormat = zFormat,
                zColor = zColor,
                show_cBar = True,
                outname = outnameAbs,
                outdir = OUTDIR,
                showlabels = True,
                grid = False,
                saveSVG = False)

    # relative scaling
    cMap = cm.viridis # cm.plasma
    zmin = np.min(Z)
    zmax = np.max(Z)
    print("relative scaling: ", zmin, zmax)
    zColor = [cMap, zmin, zmax, r'z label $\, z$']
    zFormat = ['linear', -0.75, 0.8, 0.25]

    plot_pcolor(X = xBoxCoords,
                Y = yBoxCoords,
                Z = Z,
                titlestr = '',
                params = [Z_min, Z_max],
                fProps = fProps,
                xFormatObj = xFormatObj,
                yFormatObj = yFormatObj,
                zFormat = zFormat,
                zColor = zColor,
                show_cBar = True,
                outname = outnameRel,
                outdir = OUTDIR,
                showlabels = True,
                grid = False,
                saveSVG = False)
