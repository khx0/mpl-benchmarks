#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-15
# file: mpl_offset_text_handling_05.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.3
##########################################################################################

import os
import datetime
import platform
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR  = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def Plot(X, pcolors, xFormat, yFormat, plotLabel, outname, outdir, labels = True,
         titlestr = None, grid = True, savePDF = True, savePNG = False, datestamp = True):

    xmin, xmax = xFormat[0], xFormat[1]
    ymin, ymax = yFormat[0], yFormat[1]

    mpl.rc('legend', **{'fontsize': 3.0})
    mpl.rc('axes', linewidth = 0.3)

    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'

    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'

    ######################################################################################
    # set up figure
    f, ax1 = plt.subplots(1)
    f.set_size_inches(1.3, 1.3)
    f.subplots_adjust(hspace = 2.5)
    f.subplots_adjust(wspace = 2.5)
    f.subplots_adjust(left = 0.18)
    f.subplots_adjust(bottom = 0.22)

    major_x_ticks = np.arange(xmin, xmax + 10.0, xFormat[2])
    minor_x_ticks = np.arange(xmin, xmax + 10.0, xFormat[3])
    ax1.set_xticks(major_x_ticks)
    ax1.set_xticks(minor_x_ticks, minor = True)

    major_y_ticks = np.arange(ymin, ymax + 0.5, yFormat[2])
    minor_y_ticks = np.arange(ymin, ymax + 0.5, yFormat[3])
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(4.0)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(4.0)

    ax1.tick_params('both', length = 1.5, width = 0.3, which = 'major', pad = 1.5)
    ax1.tick_params('both', length = 0.8, width = 0.2, which = 'minor', pad = 1.5)
    ######################################################################################
    # labeling
    if labels:
        if titlestr:
            plt.title(titlestr)
        ax1.set_xlabel(xFormat[4], fontsize = 5)
        ax1.set_ylabel(yFormat[4], fontsize = 5)
        ax1.xaxis.labelpad = 1.5
        ax1.yaxis.labelpad = 1.5
        ax1.annotate(r'right top label',
                     xy = (1.0, 1.02),
                     xycoords = 'axes fraction',
                     fontsize = 3.0,
                     horizontalalignment = 'right')
    ######################################################################################
    # plotting
    ax1.plot(X[:, 0], X[:, 1],
             color = pcolors[0],
             lw = 0.5,
             alpha = 1.0,
             label = plotLabel)
    ######################################################################################
    # legend
    if labels:
        leg = ax1.legend(loc = 'upper left',
                         handlelength = 2.8,
                         scatterpoints = 1,
                         markerscale = 1.0,
                         ncol = 1)
        leg.draw_frame(False)

    ######################################################################################
    ######################################################################################
    # offset text handling
    ax1 = plt.gca()
    ax1.ticklabel_format(axis = 'y', style = 'sci', scilimits = (0, 2))

    f.savefig('./dummy_figure_TMP.svg')

    offset = ax1.get_yaxis().get_offset_text()
    ax1.yaxis.offsetText.set_visible(False)

    def formatPowerOfTen(text):

        index = text.index('e')
        exponent = text[(index + 1):]
        label = r'$\mathdefault{\times \, 10^{' +  exponent + '}}$'
        return label

    powerLabel = formatPowerOfTen(offset.get_text())

    ax1.annotate(powerLabel,
                 xy = (0.0, 1.01),
                 xycoords = 'axes fraction',
                 fontsize = 3.5,
                 horizontalalignment = 'left')
    os.remove('./dummy_figure_TMP.svg')
    ######################################################################################
    ######################################################################################

    ######################################################################################
    # set plot range
    ax1.set_xlim(xmin, xmax)
    ax1.set_ylim(ymin, ymax)
    ######################################################################################
    # grid options
    if grid:
        ax1.grid(color = 'gray', alpha = 0.15, lw = 0.2, linestyle = 'dashed',
                 dashes = [7.5, 3.0])
        ax1.grid(True)
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
    return None

if __name__ == '__main__':

    outname = 'figure_05' + \
              '_Python_' + platform.python_version() + \
              '_mpl_' + mpl.__version__

    # create dummy data to plot
    n_points = 200
    xVals = np.linspace(0, 100.0, n_points)
    yVals = [1.0e4 * x for x in xVals]
    X = np.zeros((n_points, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    # set formatting
    xFormat = (0.0, 100.0, 20.0, 5.0 , r'x label')
    yFormat = (0.0, 1.0e6, 200000.0, 100000.0 , r'y label')

    # plot data
    Plot(X = X,
         pcolors = ['#003399'],
         xFormat = xFormat,
         yFormat = yFormat,
         plotLabel = r'plot legend label',
         outname = outname,
         outdir = OUTDIR)
