#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-08-16
# file: mpl_scatter_histogram_minimal.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.2
# tested with python 3.7.0  in conjunction with mpl version 2.2.2
##########################################################################################

import sys
import time
import datetime
import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(OUTDIR)

# a copy of the getHistogramCoordinates function
# from the mplUtils.py file, copied to this minimal script
# for stand alone convenience

def getHistogramCoordinates(X, nBins, normed = True):
    '''
    Creates (x, y) data pairs of the histogram data using
    numpy's histogram function.
    '''
    hist, bin_edges = np.histogram(X, bins = nBins, normed = normed)
    bin_centers = (bin_edges[1:] + bin_edges[0:-1]) / 2.0
    assert hist.shape == bin_centers.shape, "Error: Shape assertion failed."
    
    res = np.zeros((nBins, 2))
    res[:, 0] = bin_centers
    res[:, 1] = hist
    return res

if __name__ == '__main__':

    outname = 'mpl_scatter_histogram_minimal'

    # create data
    meanValue = 1.5
    nBins = 25
    nSamples = 20000
    
    # fix random seed for reproducibility
    np.random.seed(123456789)
    samples = np.random.exponential(meanValue, nSamples)
    scatterData = getHistogramCoordinates(samples, 
                                          nBins = nBins,  
                                          normed = True)
    
    # create analytical curve
    nVisPoints = 500
    xVals = np.linspace(0.0, 15.0, nVisPoints)
    yVals = np.array([np.exp(-t / meanValue) / meanValue for t in xVals])
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    ######################################################################################
    
    ### minimal plot
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
    
    outname += '_' + now
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf', dpi = 300, transparent = True)
    plt.show()
    
    # close handles
    plt.cla()
    plt.clf()
    plt.close() 


