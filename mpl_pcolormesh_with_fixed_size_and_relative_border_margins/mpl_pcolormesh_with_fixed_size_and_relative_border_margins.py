#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-12-17
# file: mpl_pcolormesh_with_fixed_size_and_relative_border_margins.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.2
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
from matplotlib.ticker import FuncFormatter

from mplUtils import getPcolorBoxCoordinates
from mplUtils import getFigureProps
from ticker import cleanFormatter

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def plot_pcolor(X, Y, Z, titlestr, fProps, xFormat, yFormat, zFormat, zColor, show_cBar,
                outname, outdir, showlabels, params = None, grid = False, saveSVG = False,
                savePDF = True, savePNG = False, datestamp = True):

    # retrieve box coordinates for pcolormesh plotting
    if params:
        width_X, height_Y = params[0], params[1]
        xBoxCoords = getPcolorBoxCoordinates(X, unitWidth = width_X)
        yBoxCoords = getPcolorBoxCoordinates(Y, unitWidth = height_Y)
    else:
        xBoxCoords = getPcolorBoxCoordinates(X)
        yBoxCoords = getPcolorBoxCoordinates(Y)

    assert xBoxCoords.shape == (len(X) + 1,), "Error: Shape assertion failed."
    assert yBoxCoords.shape == (len(Y) + 1,), "Error: Shape assertion failed."

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

    ax1.tick_params('both', length = 2.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.5, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 1.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.0, zorder = 10)

    ######################################################################################
    # labeling
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
        # add_axes(left, bottom, width, height), all between [0, 1]
        # relative to the figure size
        cax = f.add_axes([0.82, bFrac, 0.03, (tFrac - bFrac)])

        cax.tick_params('both', length = 2.5, width = 0.5, which = 'major')
        cax.tick_params('both', length = 1.5, width = 0.25, which = 'minor')
        cax.tick_params(axis = 'both', which = 'major', pad = 2)

        cb1 = mpl.colorbar.ColorbarBase(cax,
                                        cmap = cMap,
                                        norm = cNorm,
                                        orientation = 'vertical')

        ##################################################################################
        # color bar labels
        # Here axes.annotate is used to set a color bar label.
        # One can alternatively also use the colorbar.set_label function call, e.g. via:
        # cb1.set_label(zColor[3],
        #               labelpad = 2.5,
        #               fontsize = 6)
        # which creats a vertical color bar label along the color bar.
        ##################################################################################
        ax1.annotate(zColor[3],
                     xy = (1.175, 1.06),
                     xycoords = 'axes fraction',
                     fontsize = 8.0,
                     horizontalalignment = 'right')
        ##################################################################################

        cb1.outline.set_linewidth(0.5)
        cb1.ax.tick_params(axis = 'y', direction = 'out', which = 'both')
        cb1.ax.tick_params(labelsize = 6.0)

        if (zFormat[0] == 'linear'):
            cb_labels = np.arange(zFormat[1], zFormat[2], zFormat[3])
            cb1.set_ticks(cb_labels)

        #################################################################################
        # colorbar minor tick switch
        # uncomment the line below to switch on minor ticks on the color bar axis
        # cb1.ax.minorticks_on()
        #################################################################################

    ax1.pcolormesh(xBoxCoords, 
                   yBoxCoords, 
                   Z,
                   cmap = cMap,
                   norm = cNorm,
                   edgecolors = 'None')

    #####################################################################################
    # axis formatting
    if (xFormat[0] == 'auto'):
        pass
    if (xFormat[0] == 'linear'):
        ax1.set_xlim(xFormat[1], xFormat[2])
        major_x_ticks = np.arange(xFormat[3], xFormat[4], xFormat[5])
        minor_x_ticks = np.arange(xFormat[3], xFormat[4], xFormat[6])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)

    elif (xFormat[0] == 'log'):
        ax1.set_xscale('log')
        ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 8))
        ax1.xaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 8,
                                    subs = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
        for label in ax1.xaxis.get_ticklabels()[1::2]:
            label.set_visible(False)
        ax1.set_xlim(xFormat[1], xFormat[2])
    else:
        print("Error: Unknown xFormat[0] type encountered.")
        sys.exit(1)
    #####################################################################################
    if (yFormat[0] == 'auto'):
        pass
    if (yFormat[0] == 'linear'):
        ax1.set_ylim(yFormat[1], yFormat[2]) # xmin, xmax
        major_y_ticks = np.arange(yFormat[3], yFormat[4], yFormat[5])
        minor_y_ticks = np.arange(yFormat[3], yFormat[4], yFormat[6])
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)

    elif (yFormat[0] == 'log'):
        ax1.set_yscale('log')
        ax1.yaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 8))
        ax1.yaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 8,
                                    subs = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
        for label in ax1.yaxis.get_ticklabels()[1::2]:
            label.set_visible(False)
        ax1.set_ylim(yFormat[1], yFormat[2]) # xmin, xmax
    else:
        print("Error: Unknown yFormat[0] type encountered.")
        sys.exit(1)

    # tick label formatting
    majorFormatter = FuncFormatter(cleanFormatter)
    ax1.xaxis.set_major_formatter(majorFormatter)
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

def test_01(cMaps = [cm.viridis]):

    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running test 01 /////////////////////////////////////////////////////////////")

    # create synthetic 10 x 10 2d image array
    nPxs_x = 10
    nPxs_y = 10
    pixelWidth = 1.0
    pixelHeight = 1.0

    xmin, xmax = 0.0, pixelWidth  * (nPxs_x - 1)
    ymin, ymax = 0.0, pixelHeight * (nPxs_y - 1)

    xVals = np.linspace(xmin, xmax, nPxs_x)
    yVals = np.linspace(ymin, ymax, nPxs_y)

    width_X = nPxs_x * pixelWidth
    height_Y = nPxs_y * pixelHeight

    # fill matrix
    zVals = np.zeros((nPxs_x, nPxs_y))

    for j in range(nPxs_y):     # iterate over y values
        for i in range(nPxs_x): # iterate over x values
            zVals[i, j] = 0.2 * xVals[i]

    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."
    assert zVals.shape == (nPxs_x, nPxs_y), "Error: Shape assertion failed."

    zmin = np.min(zVals)
    zmax = np.max(zVals)

    ######################################################################################
    # print info for development purposes and sanity checks
    print("/////////////////////////////////////////////////////////////////////////////")
    print("xVals.shape =", xVals.shape)
    print("yVals.shape =", yVals.shape)
    print("zVals.shape =", zVals.shape)
    print("(zmin, zmax) =", zmin, zmax)
    print("/////////////////////////////////////////////////////////////////////////////")
    ######################################################################################

    # plot settings

    fProps = (4.0, 4.0, 0.16, 0.80, 0.16, 0.88)
    relativePaddingFrac = 0.015 # relative padding fraction

    xlim_left  = xmin - pixelWidth  / 2.0 - relativePaddingFrac * width_X
    xlim_right = xmax + pixelWidth  / 2.0 + relativePaddingFrac * width_X
    ylim_left  = ymin - pixelHeight / 2.0 - relativePaddingFrac * height_Y
    ylim_right = ymax + pixelHeight / 2.0 + relativePaddingFrac * height_Y

    xFormat = ('linear', xlim_left, xlim_right, 0.0, 9.05, 2.0, 1.0, r'x axis label')
    yFormat = ('linear', ylim_left, ylim_right, 0.0, 9.05, 2.0, 1.0, r'y axis label')
    zFormat = ('linear', 0.0, 1.85, 0.20)

    # loop over color maps
    for cMap in cMaps:

        zColor = (cMap, zmin, zmax, r'z label (cbar)')

        # assemble outname string
        outname = 'mpl_imshow_autowindow_test_01'
        outname += '_cmap_' + cMap.name
        outname += '_Python_' + platform.python_version() + \
                   '_mpl_' + mpl.__version__

        # call plot function
        outname = plot_pcolor(X = xVals,
                              Y = yVals,
                              Z = zVals,
                              titlestr = '',
                              fProps = fProps,
                              xFormat = xFormat,
                              yFormat = yFormat,
                              zFormat = zFormat,
                              zColor = zColor,
                              show_cBar = True,
                              outname = outname,
                              outdir = OUTDIR,
                              showlabels = True,
                              grid = False,
                              saveSVG = False)

    return None

def test_02(cMaps = [cm.viridis]):

    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running test 02 /////////////////////////////////////////////////////////////")

    # create synthetic 10 x 10 2d image array
    nPxs_x = 10
    nPxs_y = 10
    pixelWidth = 1.0
    pixelHeight = 1.0

    xmin, xmax = 0.0, pixelWidth  * (nPxs_x - 1)
    ymin, ymax = 0.0, pixelHeight * (nPxs_y - 1)

    xVals = np.linspace(xmin, xmax, nPxs_x)
    yVals = np.linspace(ymin, ymax, nPxs_y)

    width_X = nPxs_x * pixelWidth
    height_Y = nPxs_y * pixelHeight

    # fill matrix
    zVals = np.zeros((nPxs_x, nPxs_y))

    for j in range(nPxs_y):     # iterate over y values
        for i in range(nPxs_x): # iterate over x values
            zVals[i, j] = 0.2 * xVals[i]

    zVals -= 1.0 / 3.0

    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."
    assert zVals.shape == (nPxs_x, nPxs_y), "Error: Shape assertion failed."

    zmin = np.min(zVals)
    zmax = np.max(zVals)

    ######################################################################################
    # print info for development purposes and sanity checks
    print("/////////////////////////////////////////////////////////////////////////////")
    print("xVals.shape =", xVals.shape)
    print("yVals.shape =", yVals.shape)
    print("zVals.shape =", zVals.shape)
    print("(zmin, zmax) =", zmin, zmax)
    print("/////////////////////////////////////////////////////////////////////////////")
    ######################################################################################

    # plot settings

    fProps = (4.0, 4.0, 0.16, 0.80, 0.16, 0.88)
    relativePaddingFrac = 0.015 # relative padding fraction

    xlim_left  = xmin - pixelWidth  / 2.0 - relativePaddingFrac * width_X
    xlim_right = xmax + pixelWidth  / 2.0 + relativePaddingFrac * width_X
    ylim_left  = ymin - pixelHeight / 2.0 - relativePaddingFrac * height_Y
    ylim_right = ymax + pixelHeight / 2.0 + relativePaddingFrac * height_Y

    xFormat = ('linear', xlim_left, xlim_right, 0.0, 9.05, 2.0, 1.0, r'x axis label')
    yFormat = ('linear', ylim_left, ylim_right, 0.0, 9.05, 2.0, 1.0, r'y axis label')
    zFormat = ('linear', -0.4, 1.85, 0.20)

    # loop over color maps
    for cMap in cMaps:

        zColor = (cMap, zmin, zmax, r'z label (cbar)')

        # assemble outname string
        outname = 'mpl_imshow_autowindow_test_02'
        outname += '_cmap_' + cMap.name
        outname += '_Python_' + platform.python_version() + \
                   '_mpl_' + mpl.__version__

        # call plot function
        outname = plot_pcolor(X = xVals,
                              Y = yVals,
                              Z = zVals,
                              titlestr = '',
                              fProps = fProps,
                              xFormat = xFormat,
                              yFormat = yFormat,
                              zFormat = zFormat,
                              zColor = zColor,
                              show_cBar = True,
                              outname = outname,
                              outdir = OUTDIR,
                              showlabels = True,
                              grid = False,
                              saveSVG = False)

    return None

def test_03(cMaps = [cm.viridis]):

    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running test 03 /////////////////////////////////////////////////////////////")

    # create synthetic image array data

    for n in np.arange(1, 10 + 1, 1): # (from, to (excluding), increment)

        nPxs_x = n
        nPxs_y = n
        pixelWidth = 1.0
        pixelHeight = 1.0

        xmin, xmax = 0.0, pixelWidth  * (nPxs_x - 1)
        ymin, ymax = 0.0, pixelHeight * (nPxs_y - 1)

        xVals = np.linspace(xmin, xmax, nPxs_x)
        yVals = np.linspace(ymin, ymax, nPxs_y)

        width_X = nPxs_x * pixelWidth
        height_Y = nPxs_y * pixelHeight

        # fill matrix
        zVals = np.zeros((nPxs_x, nPxs_y))

        for j in range(nPxs_y):     # iterate over y values
            for i in range(nPxs_x): # iterate over x values
                zVals[i, j] = 0.2 * xVals[i]

        assert xVals.shape == yVals.shape, "Error: Shape assertion failed."
        assert zVals.shape == (nPxs_x, nPxs_y), "Error: Shape assertion failed."

        zmin = np.min(zVals)
        zmax = np.max(zVals)

        ##################################################################################
        # print info for development purposes and sanity checks
        print("/////////////////////////////////////////////////////////////////////////////")
        print("xVals.shape =", xVals.shape)
        print("yVals.shape =", yVals.shape)
        print("zVals.shape =", zVals.shape)
        print("(zmin, zmax) =", zmin, zmax)
        print("/////////////////////////////////////////////////////////////////////////////")
        ##################################################################################

        # plot settings

        fProps = (4.0, 4.0, 0.16, 0.80, 0.16, 0.88)
        relativePaddingFrac = 0.015 # relative padding fraction

        xlim_left  = xmin - pixelWidth  / 2.0 - relativePaddingFrac * width_X
        xlim_right = xmax + pixelWidth  / 2.0 + relativePaddingFrac * width_X
        ylim_left  = ymin - pixelHeight / 2.0 - relativePaddingFrac * height_Y
        ylim_right = ymax + pixelHeight / 2.0 + relativePaddingFrac * height_Y

        if n == 1: # pathological handling of n == 1 case
            xFormat = ('linear', xlim_left, xlim_right, 0.0, 1.02 * xmax + 0.01, 1.0, 1.0, r'x axis label')
            yFormat = ('linear', ylim_left, ylim_right, 0.0, 1.02 * ymax + 0.01, 1.0, 1.0, r'y axis label')
        else:
            xFormat = ('linear', xlim_left, xlim_right, 0.0, 1.02 * xmax, 1.0, 1.0, r'x axis label')
            yFormat = ('linear', ylim_left, ylim_right, 0.0, 1.02 * ymax, 1.0, 1.0, r'y axis label')

        zFormat = ('linear', -0.4, 1.85, 0.20)

        # loop over color maps
        for cMap in cMaps:

            zColor = (cMap, zmin, zmax, r'z label (cbar)')

            # assemble outname string
            outname = 'mpl_imshow_autowindow_test_03_nPxs_{}'.format(str(n).zfill(2))
            outname += '_cmap_' + cMap.name
            outname += '_Python_' + platform.python_version() + \
                       '_mpl_' + mpl.__version__

            # call plot function
            outname = plot_pcolor(X = xVals,
                                  Y = yVals,
                                  Z = zVals,
                                  params = [width_X, height_Y],
                                  titlestr = '',
                                  fProps = fProps,
                                  xFormat = xFormat,
                                  yFormat = yFormat,
                                  zFormat = zFormat,
                                  zColor = zColor,
                                  show_cBar = True,
                                  outname = outname,
                                  outdir = OUTDIR,
                                  showlabels = True,
                                  grid = False,
                                  saveSVG = False)

    return None

def test_04(cMaps = [cm.viridis]):

    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running test 04 /////////////////////////////////////////////////////////////")

    # create synthetic 32 x 32 2d image array
    nPxs_x, nPxs_y = 32, 32
    pixelWidth, pixelHeight = 1.0, 1.0

    xmin, xmax = 1.0, pixelWidth  * nPxs_x
    ymin, ymax = 1.0, pixelHeight * nPxs_y

    xVals = np.linspace(xmin, xmax, nPxs_x)
    yVals = np.linspace(ymin, ymax, nPxs_y)

    width_X = nPxs_x * pixelWidth
    height_Y = nPxs_y * pixelHeight

    # fill matrix
    zVals = np.zeros((nPxs_x, nPxs_y))

    for j in range(nPxs_y):     # iterate over y values
        for i in range(nPxs_x): # iterate over x values
            zVals[i, j] = 0.2 * xVals[i] - 0.2

    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."
    assert zVals.shape == (nPxs_x, nPxs_y), "Error: Shape assertion failed."

    zmin = np.min(zVals)
    zmax = np.max(zVals)

    ######################################################################################
    # print info for development purposes and sanity checks
    print("/////////////////////////////////////////////////////////////////////////////")
    print("xVals.shape =", xVals.shape)
    print("yVals.shape =", yVals.shape)
    print("zVals.shape =", zVals.shape)
    print("(zmin, zmax) =", zmin, zmax)
    print("/////////////////////////////////////////////////////////////////////////////")
    ######################################################################################

    # plot settings

    fProps = (4.0, 4.0, 0.16, 0.80, 0.16, 0.88)
    relativePaddingFrac = 0.015 # relative padding fraction

    xlim_left  = xmin - pixelWidth  / 2.0 - relativePaddingFrac * width_X
    xlim_right = xmax + pixelWidth  / 2.0 + relativePaddingFrac * width_X
    ylim_left  = ymin - pixelHeight / 2.0 - relativePaddingFrac * height_Y
    ylim_right = ymax + pixelHeight / 2.0 + relativePaddingFrac * height_Y

    xFormat = ('linear', xlim_left, xlim_right, 0.0, 1.05 * float(nPxs_x), 8.0, 4.0, r'x axis label')
    yFormat = ('linear', ylim_left, ylim_right, 0.0, 1.05 * float(nPxs_x), 8.0, 4.0, r'y axis label')
    zFormat = ('linear', 0.0, 6.85, 1.0)

    # loop over color maps
    for cMap in cMaps:

        zColor = (cMap, zmin, zmax, r'z label (cbar)')

        # assemble outname string
        outname = 'mpl_imshow_autowindow_test_04_32x32_matrix'
        outname += '_cmap_' + cMap.name
        outname += '_Python_' + platform.python_version() + \
                   '_mpl_' + mpl.__version__

        # call plot function
        outname = plot_pcolor(X = xVals,
                              Y = yVals,
                              Z = zVals,
                              titlestr = '',
                              fProps = fProps,
                              xFormat = xFormat,
                              yFormat = yFormat,
                              zFormat = zFormat,
                              zColor = zColor,
                              show_cBar = True,
                              outname = outname,
                              outdir = OUTDIR,
                              showlabels = True,
                              grid = False,
                              saveSVG = False)

    return None

def test_05(cMaps = [cm.viridis]):

    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running test 05 /////////////////////////////////////////////////////////////")

    # create synthetic 64 x 64 2d image array
    nPxs_x, nPxs_y = 64, 64
    pixelWidth, pixelHeight = 1.0, 1.0

    xmin, xmax = 1.0, pixelWidth  * nPxs_x
    ymin, ymax = 1.0, pixelHeight * nPxs_y

    xVals = np.linspace(xmin, xmax, nPxs_x)
    yVals = np.linspace(ymin, ymax, nPxs_y)

    width_X = nPxs_x * pixelWidth
    height_Y = nPxs_y * pixelHeight

    # fill matrix
    zVals = np.zeros((nPxs_x, nPxs_y))

    for j in range(nPxs_y):     # iterate over y values
        for i in range(nPxs_x): # iterate over x values
            zVals[i, j] = 0.2 * xVals[i] - 0.2

    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."
    assert zVals.shape == (nPxs_x, nPxs_y), "Error: Shape assertion failed."

    zmin = np.min(zVals)
    zmax = np.max(zVals)

    ######################################################################################
    # print info for development purposes and sanity checks
    print("/////////////////////////////////////////////////////////////////////////////")
    print("xVals.shape =", xVals.shape)
    print("yVals.shape =", yVals.shape)
    print("zVals.shape =", zVals.shape)
    print("(zmin, zmax) =", zmin, zmax)
    print("/////////////////////////////////////////////////////////////////////////////")
    ######################################################################################

    # plot settings

    fProps = (4.0, 4.0, 0.16, 0.80, 0.16, 0.88)
    relativePaddingFrac = 0.015 # relative padding fraction

    xlim_left  = xmin - pixelWidth  / 2.0 - relativePaddingFrac * width_X
    xlim_right = xmax + pixelWidth  / 2.0 + relativePaddingFrac * width_X
    ylim_left  = ymin - pixelHeight / 2.0 - relativePaddingFrac * height_Y
    ylim_right = ymax + pixelHeight / 2.0 + relativePaddingFrac * height_Y

    xFormat = ('linear', xlim_left, xlim_right, 0.0, 1.05 * float(nPxs_x), 16.0, 8.0, r'x axis label')
    yFormat = ('linear', ylim_left, ylim_right, 0.0, 1.05 * float(nPxs_x), 16.0, 8.0, r'y axis label')
    zFormat = ('linear', 0.0, 12.62, 2.0)

    # loop over color maps
    for cMap in cMaps:

        zColor = (cMap, zmin, zmax, r'z label (cbar)')

        # assemble outname string
        outname = 'mpl_imshow_autowindow_test_05_64x64_matrix'
        outname += '_cmap_' + cMap.name
        outname += '_Python_' + platform.python_version() + \
                   '_mpl_' + mpl.__version__

        # call plot function
        outname = plot_pcolor(X = xVals,
                              Y = yVals,
                              Z = zVals,
                              titlestr = '',
                              fProps = fProps,
                              xFormat = xFormat,
                              yFormat = yFormat,
                              zFormat = zFormat,
                              zColor = zColor,
                              show_cBar = True,
                              outname = outname,
                              outdir = OUTDIR,
                              showlabels = True,
                              grid = False,
                              saveSVG = False)

    return None

def test_06(cMaps = [cm.viridis]):

    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running test 06 /////////////////////////////////////////////////////////////")

    # create synthetic 128 x 128 2d image array
    nPxs_x, nPxs_y = 128, 128
    pixelWidth, pixelHeight = 1.0, 1.0

    xmin, xmax = 1.0, pixelWidth  * nPxs_x
    ymin, ymax = 1.0, pixelHeight * nPxs_y

    xVals = np.linspace(xmin, xmax, nPxs_x)
    yVals = np.linspace(ymin, ymax, nPxs_y)

    width_X = nPxs_x * pixelWidth
    height_Y = nPxs_y * pixelHeight

    # fill matrix
    zVals = np.zeros((nPxs_x, nPxs_y))

    for j in range(nPxs_y):     # iterate over y values
        for i in range(nPxs_x): # iterate over x values
            zVals[i, j] = 0.2 * xVals[i] - 0.2

    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."
    assert zVals.shape == (nPxs_x, nPxs_y), "Error: Shape assertion failed."

    zmin = np.min(zVals)
    zmax = np.max(zVals)

    ######################################################################################
    # print info for development purposes and sanity checks
    print("/////////////////////////////////////////////////////////////////////////////")
    print("xVals.shape =", xVals.shape)
    print("yVals.shape =", yVals.shape)
    print("zVals.shape =", zVals.shape)
    print("(zmin, zmax) =", zmin, zmax)
    print("/////////////////////////////////////////////////////////////////////////////")
    ######################################################################################

    # plot settings

    fProps = (4.0, 4.0, 0.16, 0.80, 0.16, 0.88)
    relativePaddingFrac = 0.015 # relative padding fraction

    xlim_left  = xmin - pixelWidth  / 2.0 - relativePaddingFrac * width_X
    xlim_right = xmax + pixelWidth  / 2.0 + relativePaddingFrac * width_X
    ylim_left  = ymin - pixelHeight / 2.0 - relativePaddingFrac * height_Y
    ylim_right = ymax + pixelHeight / 2.0 + relativePaddingFrac * height_Y

    xFormat = ('linear', xlim_left, xlim_right, 0.0, 1.05 * float(nPxs_x), 32.0, 16.0, r'x axis label')
    yFormat = ('linear', ylim_left, ylim_right, 0.0, 1.05 * float(nPxs_x), 32.0, 16.0, r'y axis label')
    zFormat = ('linear', 0.0, 25.42, 4.0)

    # loop over color maps
    for cMap in cMaps:

        zColor = (cMap, zmin, zmax, r'z label (cbar)')

        # assemble outname string
        outname = 'mpl_imshow_autowindow_test_06_128x128_matrix'
        outname += '_cmap_' + cMap.name
        outname += '_Python_' + platform.python_version() + \
                   '_mpl_' + mpl.__version__

        # call plot function
        outname = plot_pcolor(X = xVals,
                              Y = yVals,
                              Z = zVals,
                              titlestr = '',
                              fProps = fProps,
                              xFormat = xFormat,
                              yFormat = yFormat,
                              zFormat = zFormat,
                              zColor = zColor,
                              show_cBar = True,
                              outname = outname,
                              outdir = OUTDIR,
                              showlabels = True,
                              grid = False,
                              saveSVG = False)

    return None

if __name__ == '__main__':

    test_01(cMaps = [cm.viridis])

    test_02(cMaps = [cm.viridis])

    # test_03(cMaps = [cm.viridis])

    test_04(cMaps = [cm.viridis])

    test_05(cMaps = [cm.viridis])
    
    test_06(cMaps = [cm.viridis])

    ######################################################################################
    # Alternative usage
    # To create the output with more colormaps call e.g.
    # test_01(cMaps = [cm.viridis, cm.gray])
    ######################################################################################






    '''
    # create a 2d image matrix class
    # which has the following members
    # xVals (centerd pixel coordinate)
    # yVals (Centered pixel coordinate)
    '''

    # TODO: define window modes:
    # 1 ) set zmin and zmax
    # 2 ) apply restriced window / level range

    # TODO: create test for non-square image matrices
    # make this test_04
    
    # TODO: create unit test for the
    # getPcolorBoxCoordinates function.


