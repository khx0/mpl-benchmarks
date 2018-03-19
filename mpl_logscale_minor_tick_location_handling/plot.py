#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-03-19
# file: plot.py
##########################################################################################

"""
Benchmark matplotlib script illustrating how to set a lower and upper limit for the 
minor tick locations in logarithmic scaling independent of the x axis limits.
Version A uses the default behavior from the ticker.LogLocator class
whereas version B manually crops the minor ticks, such that the newly chosen minor tick 
locations become independent from the ax1.set_xlim(xmin, xmax) satement. 
For aesthetic reasons, I often prever to avoid minor ticks towards
both the left and right margin of a chosen log-axis. 
In general typically want to control the range for ticks indepedent of the view range,
which is straight forward in matplotlibs normal view, but a little more challenging
in the logarithmic scaling.
"""

import time
import datetime
import sys
import os
import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib import gridspec
from matplotlib import ticker
from scipy import stats
from matplotlib.ticker import LogFormatter 

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

def getFigureProps(width, height):
    '''
    Specify widht and height in cm
    '''
    lFrac, rFrac = 0.16, 0.85
    bFrac, tFrac = 0.17, 0.9
    axesWidth = width / 2.54 # convert to inches
    axesHeight = height / 2.54 # convert to inches
    fWidth = axesWidth / (rFrac - lFrac)
    fHeight = axesHeight / (tFrac - bFrac)
    return fWidth, fHeight, lFrac, rFrac, bFrac, tFrac
    
def Plot(titlestr, type, X, showlabels, outname, outdir, pColors,
         grid = True, savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
     
    mpl.rc('font',**{'size': 10})
    mpl.rc('legend',**{'fontsize': 9.0})
    mpl.rc("axes", linewidth = 0.5)    
    
    plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    plt.rcParams['pdf.fonttype'] = 42  
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}', r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)       

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 5.5, height = 4.5)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)    
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    
    major_y_ticks = np.arange(0.0, 1.1, 0.5)
    minor_y_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    
    labelfontsize = 8.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    
    ax1.tick_params('both', length = 2.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.5, width = 0.25, which = 'minor', pad = 3.0)
    
    ax1.tick_params(axis='x', which='major', pad = 1.5)
    ax1.tick_params(axis='y', which='major', pad = 1.5, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'x label', fontsize = 10.0)
    ax1.set_ylabel(r'y label', fontsize = 10.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 2.0
    ######################################################################################
    # plot data
    
    ax1.plot(X[:, 0], X[:, 1],
             color = pColors[0],
             alpha = 1.0,
             lw = 1.0,
             zorder = 2,
             label = r'plot label')
     
    ######################################################################################
    # legend
    leg = ax1.legend(loc = 'upper left',
                     handlelength = 1.5, 
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)
    
    ######################################################################################
    # set plot range and scale

    ax1.set_xscale('log')
    
    ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 10))
    
    if (type == 'A'):
    
        ax1.xaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 10,
                                    subs = np.arange(2, 10) * 0.1))
                                    
    elif (type == 'B'):
    
        locmin = mpl.ticker.LogLocator(base = 10.0, 
                                       subs = np.arange(2, 10) * 0.1,  
                                       numticks = 100)
                                   
        locminArray = locmin.tick_values(1.0e-10, 9.0e-8)
        print locminArray 
        ax1.set_xticks(locminArray, minor = True)

    else:
        print "Error: Unknown case encountered."
        sys.exit(1)
    
    
    ax1.set_xlim(5.0e-13, 2.5e-6)
     
    # uncomment the two lines below for only using every second x-tick major label                                             
    #     for label in ax1.xaxis.get_ticklabels()[::2]:
    #         label.set_visible(False)

    ax1.set_axisbelow(False)
    
    ax1.set_ylim(-0.02, 1.05)
    ax1.set_yticklabels([0, 0.5, 1])
    
    ######################################################################################
    # grid options
    if (grid):
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major', linewidth = 0.4)
        ax1.grid('on')
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor', linewidth = 0.2)
        ax1.grid('on', which = 'minor')
    ######################################################################################
    # save to file
    if (datestamp):
        outname += '_' + now
    if (savePDF): # save to file using pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True);
    if (savePNG):
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False);
    ######################################################################################
    # close handles
    plt.clf()
    plt.close()
    return outname
                
if __name__ == '__main__':

    # create data to plot
    nVisPoints = 1000
    xValues = np.logspace(-13, -5, nVisPoints)
    yValues = np.array([x / (1.0e-9 + x) for x in xValues])
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xValues
    X[:, 1] = yValues
    
    # plotting
    colorVals = ['C0']

    outname = 'mpl_logscale_minor_tick_location_handling_version_A'
    
    returnname = Plot(titlestr = '',
                      type = 'A',
                      X = X,
                      showlabels = True,
                      outname = outname,
                      outdir = OUTDIR, 
                      pColors = colorVals,
                      grid = False)

    cmd = 'pdf2svg ' + os.path.join(OUTDIR, returnname + '.pdf') + \
          ' ' + os.path.join(OUTDIR, returnname + '.svg')
    print cmd
    os.system(cmd)
                   
    outname = 'mpl_logscale_minor_tick_location_handling_version_B'
                   
    returnname = Plot(titlestr = '',
                      type = 'B',
                      X = X,
                      showlabels = True,
                      outname = outname,
                      outdir = OUTDIR, 
                      pColors = colorVals,
                      grid = False)

    cmd = 'pdf2svg ' + os.path.join(OUTDIR, returnname + '.pdf') + \
          ' ' + os.path.join(OUTDIR, returnname + '.svg')
    print cmd
    os.system(cmd)
             

    
    
