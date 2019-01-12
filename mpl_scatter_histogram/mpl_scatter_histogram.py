#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-01-12
# file: mpl_scatter_histogram.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 3.0.2
##########################################################################################

import sys
sys.path.append('../')
import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

from mplUtils import getHistogramCoordinates

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "{}-{}-{}".format(str(now.year), str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(OUTDIR)

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

def Plot(titlestr, X, Y, outname, outdir, pColors,
         grid = True, saveEPS = False, savePDF = True, savePNG = False, datestamp = True):
    
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
    
    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.5})
    mpl.rc('axes', linewidth = 0.5)    
    
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
        getFigureProps(width = 5.0, height = 4.0,
                       lFrac = 0.17, rFrac = 0.95, bFrac = 0.20, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)    
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    
    major_x_ticks = np.arange(0.0, 20.1, 5.0)
    minor_x_ticks = np.arange(0.0, 20.1, 1.0)
    ax1.set_xticks(major_x_ticks)
    ax1.set_xticks(minor_x_ticks, minor = True)
    
    major_y_ticks = np.arange(0.0, 1.1, 0.2)
    minor_y_ticks = np.arange(0.0, 1.1, 0.05)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    
    labelfontsize = 8.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    
    ax1.tick_params('both', length = 3.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 2.0, width = 0.25, which = 'minor', pad = 3.0)
    
    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'x label', fontsize = 8.0)
    ax1.set_ylabel(r'frequency', fontsize = 8.0)
    ax1.xaxis.labelpad = 5.0
    ax1.yaxis.labelpad = 5.0
    ######################################################################################
    
    ax1.plot([-1.0, 20.0], [0.0, 0.0],
             dashes = [4.0, 2.0],
             color = '#CCCCCC',
             lw = 1.0,
             zorder = 1)
    
    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = pColors[0],
             lw = 0.5,
             label = 'analytical data',
             clip_on = True,
             zorder = 1)
             
    ax1.scatter(Y[:, 0], Y[:, 1],
                s = 20,
                lw = 0.5,
                facecolor = 'None',
                edgecolor = pColors[0],
                zorder = 2,
                label = r'sampled data')
    
    # legend
    leg = ax1.legend(handlelength = 1.5, 
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)
            
    ######################################################################################
    # set plot range and scale
    ax1.set_xlim(-0.25, 13.25)
    ax1.set_ylim(-0.025, 0.625)
    ax1.set_axisbelow(False)
    ######################################################################################
    # grid options
    if grid:
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major',
                 linewidth = 0.4)
        ax1.grid('on')
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor',
                 linewidth = 0.2)
        ax1.grid('on', which = 'minor')
    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + now
    if savePDF: # save to file using pdf backend
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

    outname = 'mpl_scatter_histogram'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # create data
    meanValue = 1.5
    nBins = 25
    nSamples = 20000
    
    # fix random seed for reproducibility
    np.random.seed(123456789)
    samples = np.random.exponential(meanValue, nSamples)
    scatterData = getHistogramCoordinates(samples, 
                                          nBins = nBins,  
                                          density = True)
    
    # create analytical curve
    nVisPoints = 500
    xVals = np.linspace(0.0, 20.0, nVisPoints)
    yVals = np.array([np.exp(-t / meanValue) / meanValue for t in xVals])
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    # plot data                    
    Plot(titlestr = '',
         X = X, 
         Y = scatterData,
         outname = outname,
         outdir = OUTDIR, 
         pColors = ['C3'],
         grid = False)
