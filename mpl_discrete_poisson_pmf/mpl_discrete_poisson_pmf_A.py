#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-10-18
# file: mpl_discrete_poisson_pmf_A.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.2
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend
from matplotlib.ticker import FuncFormatter

from scipy.stats import poisson

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def cleanFormatter(x, pos = None):
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

def Plot(titlestr, X, params, outname, outdir, pColors,
         grid = False, drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 6.0})
    mpl.rc('axes', linewidth = 0.5)

    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 4.1, height = 2.9,
                       lFrac = 0.18, rFrac = 0.95, bFrac = 0.18, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    labelfontsize = 5.0

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 1.75, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.0, width = 0.25, which = 'minor', pad = 3.0)

    ax1.tick_params(axis = 'x', which = 'major', pad = 1.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'$k$', fontsize = 6.0)
    ax1.set_ylabel(r'$p(k\, |\, \mu)$', fontsize = 6.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 2.0
    ######################################################################################
    # plotting

    lineWidth = 0.5

    ax1.plot([-1.0, 21.0], [0.0, 0.0],
             color = pColors[0],
             alpha = 1.0,
             lw = lineWidth,
             zorder = 2,
             dashes = [4.0, 2.0])

    for i in range(len(muVals)):

        ax1.plot(X[:, 0], X[:, i + 1],
                 color = pColors[i + 1],
                 alpha = 1.0,
                 lw = lineWidth,
                 zorder = 2,
                 label = r'')

        ax1.scatter(X[:, 0], X[:, i + 1],
                    s = 4.5,
                    lw = lineWidth,
                    facecolor = pColors[i + 1],
                    edgecolor = 'None',
                    zorder = 11,
                    label = labels[i])

    ######################################################################################
    # annotations

    label = r'$p(k\, |\, \mu) = \dfrac{\mu^k}{k!} e^{-\mu}$'

    x_pos = 0.25

    ax1.annotate(label,
                 xy = (x_pos, 0.85),
                 xycoords = 'axes fraction',
                 fontsize = 6.0,
                 horizontalalignment = 'left')

    ######################################################################################
    # legend
    if drawLegend:
        leg = ax1.legend(# bbox_to_anchor = [0.7, 0.8],
                         # loc = 'upper left',
                         handlelength = 0.25,
                         scatterpoints = 1,
                         markerscale = 1.0,
                         ncol = 1)
        leg.draw_frame(False)
        plt.gca().add_artist(leg)

    ######################################################################################
    # set plot range
    if xFormat is not None: # else pass
        major_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[4])
        minor_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[5])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
        ax1.set_xlim(xFormat[0], xFormat[1])

    if yFormat is not None: # else pass
        major_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[4])
        minor_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[5])
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)
        ax1.set_ylim(yFormat[0], yFormat[1])

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
        outname += '_' + today
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

    '''
    pmf = probability mass function
    pmf function signature
    poisson.pmf(k, mu, loc = 0)
    where k is the random variable, mu the shape parameter and loc
    the distribution of the corresponding Poisson distribution
    '''

    ######################################################################################
    # create Poisson distribution
    muVals = [1.0, 5.0, 9.0]

    xVals = np.arange(0, 30, 1)

    X = np.zeros((len(xVals), len(muVals) + 1))
    X[:, 0] = xVals

    for i, mu in enumerate(muVals):

        yVals = poisson.pmf(xVals, mu)
        assert xVals.shape == yVals.shape, "Error: Shape assertion failed."

        X[:, i + 1] = yVals

        ##################################################################################
        # check for normalization
        norm = np.sum(yVals)
        print("Normalization = np.sum(yVals) = ", norm)
        assert np.isclose(norm, 1.0), \
               "Error: Poisson distribution seems NOT to be normalized."

    ######################################################################################
    # call plotting function

    labels = [r'$\mu = 1$',
              r'$\mu = 5$',
              r'$\mu = 9$']

    outname = 'mpl_discrete_poisson_pmf_A'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    xFormat = (-0.5, 19.5, 0.0, 19.1, 5.0, 1.0)
    yFormat = (-0.02, 0.42, 0.0, 0.405, 0.1, 0.05)

    pColors = ['#CCCCCC', 'C0', 'C1', 'C2']

    outname = Plot(titlestr = '',
                   X = X,
                   params = [],
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   grid = False,
                   drawLegend = True,
                   xFormat = xFormat,
                   yFormat = yFormat)
