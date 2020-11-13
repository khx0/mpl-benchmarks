#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-13
# file: mpl_scatter_histogram_minimal.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.3
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

# a copy of the getHistogramCoordinates function
# from the mplUtils.py file, copied to this minimal script
# to make it self sufficient by itself
# (stand alone version for convenience)

def getHistogramCoordinates(X, nBins, density = True):
    '''
    Creates (x, y) data pairs of the histogram data using
    numpy's histogram function.
    '''
    hist, bin_edges = np.histogram(X, bins = nBins, density = density)
    bin_centers = (bin_edges[1:] + bin_edges[0:-1]) / 2.0
    assert hist.shape == bin_centers.shape, "Error: Shape assertion failed."

    res = np.zeros((nBins, 2))
    res[:, 0] = bin_centers
    res[:, 1] = hist
    return res

if __name__ == '__main__':

    outname = 'mpl_scatter_histogram_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    # create data
    meanValue = 1.5
    n_bins = 25
    n_samples = 20000

    # fix random seed for reproducibility
    np.random.seed(123456789)
    samples = np.random.exponential(meanValue, n_samples)
    scatterData = getHistogramCoordinates(samples,
                                          nBins = n_bins,
                                          density = True)

    # create analytical curve
    n_vispoints = 500
    xVals = np.linspace(0.0, 15.0, n_vispoints)
    yVals = np.array([np.exp(-t / meanValue) / meanValue for t in xVals])
    X = np.zeros((n_vispoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    ######################################################################################
    # minimal plot
    f, ax1 = plt.subplots(1)

    ax1.plot([-0.25, 15.0], [0.0, 0.0],
             dashes = [4.0, 2.0],
             color = '#CCCCCC',
             zorder = 1)

    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = 'C3',
             label = 'analytical data',
             zorder = 1)

    ax1.scatter(scatterData[:, 0], scatterData[:, 1],
                facecolor = 'None',
                edgecolor = 'C3',
                zorder = 2,
                label = r'sampled data')

    # set plot range and scale
    ax1.set_xlim(-0.25, 14.25)
    ax1.set_ylim(-0.05, 0.625)

    # legend
    leg = ax1.legend(handlelength = 2.0,
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)

    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
