#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-05
# file: mpl_xyFormat_passing.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 2.2.3
##########################################################################################

##########################################################################################
# xFormat and yFormat are two 6-tuples each for x- and y-format passing to
# the any given plotting function.
# The syntax is the following
# xFormat = (xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor)
# yFormat = (ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor)
# Often I wish to set the x- and y scaling and ticks after a manual inspection
# of the data. Hence a full automatization with autoscaling is often anyway not
# always desired, since many plots are simply a lot of individual custom work.
# However, often I wish to reuse a plotting function, and the only thing that
# needs to be changed is the x-y scaling. Thus using these two 6-tuples is a
# convenient way for me to quickly pass this kind of information to
# any kind of plotting function.
# By passing xFormat = None to the plotting function, matplotlib's default
# autoscaling will be used.
##########################################################################################

import time
import datetime
import sys
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

def Plot(titlestr, X, xFormat, yFormat, outname, outdir, pColors,
         grid = True, savePDF = True, savePNG = False, datestamp = True):
    
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
    
    mpl.rc('font',**{'size': 10})
    mpl.rc('legend',**{'fontsize': 7.5})
    mpl.rc("axes", linewidth = 0.5)    
    
    plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    plt.rcParams['pdf.fonttype'] = 42  
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                  r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)      
    
    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 6.5, height = 5.5,
                       lFrac = 0.20, rFrac = 0.9, bFrac = 0.17, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)    
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    labelfontsize = 10.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    
    ax1.tick_params('both', length = 3.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 2.0, width = 0.25, which = 'minor', pad = 3.0)
    
    ax1.tick_params(axis='x', which='major', pad = 2.0)
    ax1.tick_params(axis='y', which='major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'x label', fontsize = 10.0)
    ax1.set_ylabel(r'y label', fontsize = 10.0)
    ax1.xaxis.labelpad = 3.0
    ax1.yaxis.labelpad = 3.0
    ######################################################################################
    
    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = pColors[0],
             lw = 1.0,
             label = 'line',
             clip_on = True,
             zorder = 1)
    
    # manually set the axis zorder here
    ax1.set_axisbelow(False)
    for k, spine in ax1.spines.items():  #ax.spines is a dictionary
        spine.set_zorder(10)
    
    ### legend
    leg = ax1.legend(handlelength = 1.35, 
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)
        
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
    ######################################################################################
    # grid options
    if (grid):
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major', 
                 linewidth = 0.4)
        ax1.grid('on')
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor',
                 linewidth = 0.2)
        ax1.grid('on', which = 'minor')
    ######################################################################################
    # save to file
    if (datestamp):
        outname += '_' + now
    if (savePDF): # save to file using pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if (savePNG):
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return None

if __name__ == '__main__':

    # create data
    nVisPoints = 1000
    xVals = np.linspace(-0.5, 12.5, nVisPoints)
    yVals = np.array([np.sin(x) for x in xVals])
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    # plot data                    
        
    # matplotlib's default autoscaling

    xFormat = None
    yFormat = None
    
    Plot(titlestr = '',
         X = X, 
         xFormat = xFormat,
         yFormat = yFormat,
         outname = 'mpl_xyFormat_passing_autoscale',
         outdir = OUTDIR, 
         pColors = ['C0'],
         grid = False)

    # example 1    
    
    xFormat = (-0.2, 10.2, 0.0, 10.1, 5.0, 1.0)
    yFormat = (-1.1, 1.1, -1.0, 1.05, 0.5, 0.1)
    
    Plot(titlestr = '',
         X = X, 
         xFormat = xFormat,
         yFormat = yFormat,
         outname = 'mpl_xyFormat_passing_example_01',
         outdir = OUTDIR, 
         pColors = ['C0'],
         grid = False)
         
    # example 2 
    
    xFormat = (0.0, 2.0 * np.pi, 0.0, 2.0 * np.pi * 1.02, 1.0, 0.5)
    yFormat = (-1.1, 1.1, -1.0, 1.05, 1.0, 0.2)
    
    Plot(titlestr = '',
         X = X, 
         xFormat = xFormat,
         yFormat = yFormat,
         outname = 'mpl_xyFormat_passing_example_02',
         outdir = OUTDIR, 
         pColors = ['C0'],
         grid = False)

    
    
    
    
    
    
     
       
       
         
