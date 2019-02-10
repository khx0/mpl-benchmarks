#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-10
# file: mpl_legend_element_order.py
# tested with python 2.7.15 using matplotlib 2.2.3
# tested with python 3.7.2  using matplotlib 3.0.2
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

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

def Plot(titlestr, X, data, outname, outdir, 
         grid = False, drawLegend = True, xFormat = None, yFormat = None, 
         savePDF = True, savePNG = False, datestamp = True):
    
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
    
    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 4.0})
    mpl.rc("axes", linewidth = 0.5)    
    
    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
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
        getFigureProps(width = 3.6, height = 2.42,
                       lFrac = 0.16, rFrac = 0.96,
                       bFrac = 0.18, tFrac = 0.94)
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
    
    ax1.tick_params('both', length = 2.0, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 1.5, width = 0.25, which = 'minor', pad = 3.0)
    
    ax1.tick_params(axis = 'x', which = 'major', pad = 1.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'$x$ label', fontsize = 6.0)
    ax1.set_ylabel(r'$y$ label', fontsize = 6.0)
    ax1.xaxis.labelpad = -2.0
    ax1.yaxis.labelpad = 0.0
    ######################################################################################
    # plotting
    
    lineWidth = 0.5
    
    p1, = ax1.plot(X[:, 0], X[:, 1], 
                  color = 'k',
                  alpha = 1.0,
                  lw = lineWidth,
                  zorder = 2,
                  label = r"p1 handle's label")
    
    p2 = ax1.scatter(data[:, 0], data[:, 1],
                s = 10.0,
                lw = lineWidth,
                facecolor = 'None',
                edgecolor = 'k',
                zorder = 3,
                label = r"p2 handle's label")    
    
    error = 0.5
    p3 = ax1.fill_between(X[:, 0], X[:, 1] - error, X[:, 1] + error, 
                          color = 'k',
                          alpha = 0.15,
                          lw = 0.0,
                          zorder = 2,
                          label = r"p3 handle's label")
        
    ######################################################################################
    # legend
    if drawLegend:
        
        print("Plot handle data types:")
        print("type(p1) =", type(p1))
        print("type(p2) =", type(p2))
        print("type(p3) =", type(p3))
        '''
        The order of the plot handles in the pHandles list determines their
        oder in the figure's legend.
        '''
        pHandles = [p3, p2, p1]
        pLabels = [handle.get_label() for handle in pHandles]
        
        leg = ax1.legend(pHandles,
                         pLabels,
                         # bbox_to_anchor = [0.07, 0.02],
                         loc = 'upper right',
                         handlelength = 1.5, 
                         scatterpoints = 1,
                         markerscale = 1.0,
                         ncol = 1)
        leg.draw_frame(False)
        plt.gca().add_artist(leg)
    ######################################################################################
    # set plot range  
    if (xFormat == None):
        pass
    else:
        major_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[4])
        minor_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[5])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
        ax1.set_xlim(xFormat[0], xFormat[1])
        
    if (yFormat == None):
        pass
    else:
        major_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[4])
        minor_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[5])
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)
        ax1.set_ylim(yFormat[0], yFormat[1])
    
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
        outname += '_' + now
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
    
    # create synthetic data
    nVisPoints = 500
    xVals = np.linspace(-0.25, 1.25, nVisPoints)
    yVals = np.sin(2.0 * np.pi * xVals)
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    # fix random number seed for reproducibility
    np.random.seed(123456789)
    mu = 0.0
    sigma = 0.3
    nDatapoints = 30
    data = np.zeros((nDatapoints, 2))
    data[:, 0] = np.linspace(0.0, 1.0, nDatapoints)
    data[:, 1] = np.sin(2.0 * np.pi * data[:, 0]) + np.random.normal(mu, sigma, nDatapoints)
    
    outname = 'mpl_legend_element_order'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    
    xFormat = [-0.035, 1.035, 0.0, 1.1, 1.0, 0.25]
    yFormat = [-1.65, 1.65, -1.0, 1.1, 1.0, 1.0]
    
    outname = Plot(titlestr = '',
                   X = X,
                   data = data,
                   outname = outname,
                   outdir = OUTDIR,
                   grid = False, 
                   drawLegend = True, 
                   xFormat = xFormat,
                   yFormat = yFormat)
