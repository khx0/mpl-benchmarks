#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-23
# file: mplUtils.py
##########################################################################################

import sys
import numpy as np

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def nextHigher(value, baseUnit):
    return np.ceil(value / baseUnit) * baseUnit 

def getFigureProps(width, height, lFrac = 0.17, rFrac = 0.9, bFrac = 0.17, tFrac = 0.9):
    '''
    True size scaling auxiliary function to setup mpl plots with a desired size in cm.
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
    axesWidth = width / 2.54    # convert to inches (1 inch = 2.54 cm)
    axesHeight = height / 2.54  # convert to inches
    fWidth = axesWidth / (rFrac - lFrac)
    fHeight = axesHeight / (tFrac - bFrac)
    return fWidth, fHeight, lFrac, rFrac, bFrac, tFrac

def getPcolorBoxCoordinates(X, type = 'linear'):
    '''
    Create coordinates for the x and y axis of a pseudo-color 2D plot in matplotlib.
    This function was tailored to provide the BoxCoordinates with the mpl function
    pcolor.
    input:
        X = 1D array (i.e. the x or y axis values)
    returns:
        Xcoords = xoordinate values for the recatangular patches of the 
                  corresponding pcolor plot.
    Note:
        When X is a (N, 1) od (N,) numpy array, then Xcoords will always be created 
        to be a (N+1, 1) or (N+1,) numpy array.
    '''
    if (type == 'linear'):
        dx = X[1] - X[0]
        Xcoords = np.linspace(X[0] - dx / 2.0, X[-1] + dx / 2.0, len(X) + 1)
    elif (type == 'log'):
        dx = np.log10(X[1] / X[0])
        minExp = np.log10(X[0])
        maxExp = np.log10(X[-1])
        Xcoords = np.logspace(minExp - dx / 2.0, maxExp + dx / 2.0, len(X) + 1)
    else:
        print("Error: Unknown type encountered.")
        sys.exit(1)
    return Xcoords

def getHistogramCoordinates(X, nBins, density = True):
    '''
    Creates (x, y) data pairs of the histogram data using
    numpy's histogram function.
    
    Numpy's histogram normed keyword is deprecated and has been replaced
    by density = True / False.
    '''
    hist, bin_edges = np.histogram(X, bins = nBins, density = density)
    bin_centers = (bin_edges[1:] + bin_edges[0:-1]) / 2.0
    assert hist.shape == bin_centers.shape, "Error: Shape assertion failed."
    
    res = np.zeros((nBins, 2))
    res[:, 0] = bin_centers
    res[:, 1] = hist
    return res
    
if __name__ == '__main__':

    pass
