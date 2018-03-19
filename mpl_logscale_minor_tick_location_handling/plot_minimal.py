#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-03-19
# file: plot_minimal.py
##########################################################################################

"""
(Minimal) Benchmark matplotlib script illustrating how to set a lower and upper limit for the 
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

import sys
import os
import time
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import LogFormatter 

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(OUTDIR)

def  plot_minimal_version_A(X, filename):

    f, ax1 = plt.subplots(1)
    
    ax1.set_xlabel(r'x label', fontsize = 10.0)
    ax1.set_ylabel(r'y label', fontsize = 10.0)
    ax1.xaxis.labelpad = 4.0
    ax1.yaxis.labelpad = 4.0

    ax1.plot(X[:, 0], X[:, 1],
             color = 'C0',
             alpha = 1.0,
             lw = 1.0)
             
    # set plot range and scale

    ax1.set_xscale('log')
    
    ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 10))

    ax1.xaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 10,
                                subs = np.arange(2, 10) * 0.1))
    
    ax1.set_xlim(5.0e-13, 2.5e-6)
        
    ax1.set_ylim(-0.02, 1.05)
    major_y_ticks = np.arange(0.0, 1.1, 0.5)
    minor_y_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    ax1.set_yticklabels([0, 0.5, 1])
    
    ax1.set_axisbelow(False)
    
    filename += '_' + now
    f.savefig(os.path.join(OUTDIR, filename + '.pdf'), dpi = 300, transparent = True)
    
    # close handles
    plt.clf()
    plt.close()
    
def  plot_minimal_version_B(X, filename):

    f, ax1 = plt.subplots(1)
    
    ax1.set_xlabel(r'x label', fontsize = 10.0)
    ax1.set_ylabel(r'y label', fontsize = 10.0)
    ax1.xaxis.labelpad = 4.0
    ax1.yaxis.labelpad = 4.0

    ax1.plot(X[:, 0], X[:, 1],
             color = 'C0',
             alpha = 1.0,
             lw = 1.0)
             
    # set plot range and scale

    ax1.set_xscale('log')
    
    ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 10))

    locmin = mpl.ticker.LogLocator(base = 10.0, 
                                   subs = np.arange(2, 10) * 0.1,  
                                   numticks = 100)
                                   
    locminArray = locmin.tick_values(1.0e-10, 9.0e-8)
    # use to manually set the range for the minor ticks in logarithmic scaling
    print locminArray 
    ax1.set_xticks(locminArray, minor = True)
    
    ax1.set_xlim(5.0e-13, 2.5e-6)
        
    ax1.set_ylim(-0.02, 1.05)
    major_y_ticks = np.arange(0.0, 1.1, 0.5)
    minor_y_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    ax1.set_yticklabels([0, 0.5, 1])
    
    ax1.set_axisbelow(False)
    
    filename += '_' + now
    f.savefig(os.path.join(OUTDIR, filename + '.pdf'), dpi = 300, transparent = True)
    
    # close handles
    plt.clf()
    plt.close()

if __name__ == '__main__':

    # create data to plot
    nVisPoints = 1000
    xValues = np.logspace(-13, -5, nVisPoints)
    yValues = np.array([x / (1.0e-9 + x) for x in xValues])
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xValues
    X[:, 1] = yValues
    
    outname = 'mpl_logscale_minor_tick_location_handling_minimal_version_A'
    plot_minimal_version_A(X, outname)

    outname = 'mpl_logscale_minor_tick_location_handling_minimal_version_B'
    plot_minimal_version_B(X, outname)


    
