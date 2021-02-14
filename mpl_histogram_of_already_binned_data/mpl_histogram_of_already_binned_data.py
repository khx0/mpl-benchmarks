#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-02-14
# file: mpl_histogram_of_already_binned_data.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.4
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from scipy.stats import norm

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
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

def Plot(bins, values, outname, outdir, pColors, labelString = None,
         titlestr = None, params = None, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.0})
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
        getFigureProps(width = 5.0, height = 5.0,
                       lFrac = 0.18, rFrac = 0.95,
                       bFrac = 0.12, tFrac = 0.95)
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

    ax1.tick_params(axis = 'x', which = 'major', pad = 1.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.0, zorder = 10)
    ######################################################################################
    # labeling
    if titlestr:
        plt.title(titlestr)
    ax1.set_xlabel(r'$x_i$', fontsize = 8.0)
    # rotation (angle) is expressed in degrees, not radians.
    ax1.set_ylabel(r'probabilities  $ p(x_i)$', fontsize = 8.0)
    ax1.xaxis.labelpad = 1.0
    ax1.yaxis.labelpad = 4.0
    ######################################################################################
    # plotting

    ######################################################################################
    # CENTER PIECE (not center fold)
    # This way of calling mpl's hist function is suitable for plotting already
    # binned data, as it is the case here.
    # The key is using the weights keyword in the hist command as below.

    ax1.hist(bins[:-1], bins, weights = values,
             color = pColors['opaque_standard_blue'],
             edgecolor = 'k',
             linewidth = 1.0)

    # For further explanations, please see:
    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.hist.html
    # e.g. using
    #   counts, bins = np.histogram(data)
    #   plt.hist(bins[:-1], bins, weights=counts)
    ######################################################################################


    ######################################################################################
    # annotations
    if labelString:
        x_pos, y_pos = 0.025, 0.92
        ax1.annotate(labelString,
                     xy = (x_pos, y_pos),
                     xycoords = 'axes fraction',
                     fontsize = 6.0,
                     horizontalalignment = 'left')

    ######################################################################################
    # set plot range and scale
    if xFormat:
        xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor = xFormat
        major_x_ticks = np.arange(xTicksMin, xTicksMax, dxMajor)
        minor_x_ticks = np.arange(xTicksMin, xTicksMax, dxMinor)
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
        ax1.set_xlim(xmin, xmax) # set x limits last (order matters here)
    if yFormat:
        ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor = yFormat
        major_y_ticks = np.arange(yTicksMin, yTicksMax, dyMajor)
        minor_y_ticks = np.arange(yTicksMin, yTicksMax, dyMinor)
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)
        ax1.set_ylim(ymin, ymax) # set y limits last (order matters here)

    # tick label formatting
    majorFormatter = FuncFormatter(cleanFormatter)
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax1.yaxis.set_major_formatter(majorFormatter)

    ax1.set_axisbelow(False)

    for spine in ax1.spines.values(): # ax1.spines is a dictionary
        spine.set_zorder(10)

    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + today
    if savePDF: # save to file using pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = True)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':

    ######################################################################################
    # Create binned data:
    # Here the data is taken at discrete points from a normal distribution and then
    # renormalized to create a properly normalized discrete probability distribution.
    # Here we want to plot this pre-binned data using mpl's histogram function.
    ######################################################################################

    xmin, xmax = 0.0, 1.0
    n_bins = 30
    dx = (xmax - xmin) / float(n_bins)
    bins = np.linspace(xmin, xmax, n_bins + 1)
    binCenters = bins[:-1] + dx / 2.0

    pValues = np.zeros((n_bins,))
    pValues = norm.pdf(binCenters,
                       loc = binCenters[14],
                       scale = 0.184)

    # normalize the discrete probability distribution
    normalization = np.sum(pValues)
    pValues /= normalization

    assert np.isclose(np.sum(pValues), 1.0), "Normalization assertion failed."

    # Now bins and pValues contains the pre-binned and (here) normalized data, 
    # that we wish to plot using a histogram.

    ######################################################################################
    # plotting

    xFormat = (0.0, 1.0, 0.0, 1.05, 0.5, 0.1)
    yFormat = (0.0, 0.1547, 0.0, 0.55, 0.05, 0.025)

    outname = 'mpl_histogram_of_already_binned_data'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    ########################################################
    # color settings
    # #0000FF = RGB(0, 0, 255)
    # #6666ff roughly corresponds to #0000FF at 0.55 opacity
    # plot color dictionary
    pColors = {
        'blue': '#0000FF',
        'opaque_standard_blue': '#6666ff'
        }
    ########################################################

    outname = Plot(bins = bins,
                   values = pValues,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   labelString = r"Using mpl's histogram with already binned data.",
                   xFormat = xFormat,
                   yFormat = yFormat,
                   savePNG = True)
