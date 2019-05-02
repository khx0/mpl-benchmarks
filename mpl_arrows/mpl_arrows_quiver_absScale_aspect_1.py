#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-05-02
# file: mpl_arrows_absScale_aspect_1.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.2  in conjunction with mpl version 3.0.3
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend
from matplotlib.ticker import FuncFormatter

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def cleanFormatter(x, pos):
    '''
    will format 0.0 as 0 and
    will format 1.0 as 1
    '''
    return '{:g}'.format(x)

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
         grid = False, drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.0})
    mpl.rc("axes", linewidth = 0.5)

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
        getFigureProps(width = 3.0, height = 3.0,
                       lFrac = 0.22, rFrac = 0.95,
                       bFrac = 0.20, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)

    # minimal layout
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    ######################################################################################
    labelfontsize = 6.0

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 2.0, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.5, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 1.5)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.5, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'x label', fontsize = 6.0)
    ax1.set_ylabel(r'y label', fontsize = 6.0)
    ax1.xaxis.labelpad = 4.0
    ax1.yaxis.labelpad = 4.0
    ######################################################################################
    # plotting

    lineWidth = 0.5

    '''
	mpl.arrows example
	In this example the arrow position and in particular the arrow head size are
	specified by absolute scaling.
    '''

    ######################################################################################
    # horizontal reference line
    ax1.plot([0.6, 0.8], [0.4, 0.4],
             color = pColors[0],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ax1.plot([0.6, 0.6], [0.35, 0.85],
    		 linewidth = lineWidth,
    		 color = '#CCCCCC',
    		 zorder = 1)


    # horizontal arrows
    dx = 0.2 # x displacement of the arrow head
    hWidth = 0.05
    hLength = 0.05

    ax1.arrow(0.6, 0.5, dx, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    ax1.arrow(0.6, 0.7, dx, 0.0,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = False,
              clip_on = False,
              zorder = 3)

    x_pos = 0.6
    y_pos = 0.6
    x_direct = 1.0
    y_direct = 0.0

    ax1.quiver(x_pos, y_pos, x_direct, y_direct, units = 'width',
               scale = 5.0,
               scale_units = 'width',
               linewidth = 1.5,
               headwidth = 6.0,
               headlength = 8.0,
               headaxislength = 6.0)

    x_pos = 0.6
    y_pos = 0.8
    x_direct = 1.0
    y_direct = 0.0

    ax1.quiver(x_pos, y_pos, x_direct, y_direct, units = 'width',
               scale = 4.0,
               scale_units = 'width',
               linewidth = 1.5,
               headwidth = 6.0,
               headlength = 8.0,
               headaxislength = 6.0)

    ######################################################################################
    # vertical reference line
    ax1.plot([0.1, 0.1], [0.6, 0.8],
             color = pColors[0],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ax1.plot([0.075, 0.55], [0.6, 0.6],
    		 linewidth = lineWidth,
    		 color = '#CCCCCC',
    		 zorder = 1)

    # vertical arrows
    dy = 0.2 # y displacement of the arrow head
    ax1.arrow(0.2, 0.6, 0.0, dy,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    ax1.arrow(0.4, 0.6, 0.0, dy,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = False,
              clip_on = False,
              zorder = 3)

    x_pos = 0.3
    y_pos = 0.6
    x_direct = 0.0
    y_direct = 1.0

    ax1.quiver(x_pos, y_pos, x_direct, y_direct, units = 'height',
               scale = 5.0,
               scale_units = 'height',
               linewidth = 1.5,
               headwidth = 6.0,
               headlength = 8.0,
               headaxislength = 6.0)

    x_pos = 0.5
    y_pos = 0.6
    x_direct = 0.0
    y_direct = 1.0

    ax1.quiver(x_pos, y_pos, x_direct, y_direct, units = 'height',
               scale = 4.0,
               scale_units = 'height',
               linewidth = 1.5,
               headwidth = 6.0,
               headlength = 8.0,
               headaxislength = 6.0)

    ######################################################################################
    # 45 degree tilted reference line
    radius = 0.2
    phi = np.pi / 4.0 # = 45 degrees
    dx = radius * np.cos(phi)
    dy = radius * np.sin(phi)

    ax1.plot([0.1, 0.1 + dx], [0.3, 0.3 + dy],
             color = pColors[0],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             label = r'')

    ax1.arrow(0.2, 0.2, dx, dy,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = True,
              clip_on = False,
              zorder = 3)

    ax1.arrow(0.3, 0.1, dx, dy,
              lw = 0.5,
              color = 'k',
              head_width = hWidth,
              head_length = hLength,
              length_includes_head = False,
              clip_on = False,
              zorder = 3)

    ######################################################################################
    # annotations

    ax1.annotate(r'horizontal arrows',
                 xy = (0.6, 0.88),
                 xycoords = 'axes fraction',
                 fontsize = 4.0,
                 horizontalalignment = 'left')

    ax1.annotate(r'vertical arrows',
                 xy = (0.1, 0.90),
                 xycoords = 'axes fraction',
                 fontsize = 4.0,
                 horizontalalignment = 'left')

    ax1.annotate(r'45$^{\circ}$ tilted arrows',
                 xy = (0.4, 0.1),
                 xycoords = 'axes fraction',
                 fontsize = 4.0,
                 horizontalalignment = 'left')

    ######################################################################################
    # legend
    if drawLegend:
        leg = ax1.legend(# bbox_to_anchor = [0.7, 0.8],
                         # loc = 'upper left',
                         handlelength = 1.5,
                         scatterpoints = 1,
                         markerscale = 1.0,
                         ncol = 1)
        leg.draw_frame(False)
        plt.gca().add_artist(leg)

    ######################################################################################
    # set plot range and scale
    if (xFormat == None):
        pass # mpl autoscale
    else:
        xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor = xFormat
        ax1.set_xlim(xmin, xmax)
        major_x_ticks = np.arange(xTicksMin, xTicksMax, dxMajor)
        minor_x_ticks = np.arange(xTicksMin, xTicksMax, dxMinor)
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
    if (yFormat == None):
        pass # mpl autoscale
    else:
        ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor = yFormat
        ax1.set_ylim(ymin, ymax)
        major_y_ticks = np.arange(yTicksMin, yTicksMax, dyMajor)
        minor_y_ticks = np.arange(yTicksMin, yTicksMax, dyMinor)
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)

    # tick label formatting
    majorFormatter = FuncFormatter(cleanFormatter)
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax1.yaxis.set_major_formatter(majorFormatter)

    ax1.set_axisbelow(False)

    for spine in ax1.spines.values(): # ax1.spines is a dictionary
        spine.set_zorder(10)

    ######################################################################################
    # grid options
    if grid:
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major',
                 linewidth = 0.2)
        ax1.grid('on')
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor',
                 linewidth = 0.1)
        ax1.grid('on', which = 'minor')
    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + now
    if savePDF:
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

    outname = 'mpl_arrows_quiver_absScale_aspect_1'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    ################################################################
    # xyFormat syntax:
    # xFormat = (xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor)
    # yFormat = (ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor)
    xFormat = (0.0, 1.0, 0.0, 1.1, 0.5, 0.1)
    yFormat = (0.0, 1.0, 0.0, 1.1, 0.5, 0.1)
    ################################################################

    pColors = ['k']

    # call the plotting function
    outname = Plot(titlestr = '',
                   X = None,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   grid = False,
                   drawLegend = False,
                   xFormat = xFormat,
                   yFormat = yFormat)
