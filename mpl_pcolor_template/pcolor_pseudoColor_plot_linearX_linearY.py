#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-04-09
# file: pcolor_pseudoColor_plot_linearX_linearY.py
##########################################################################################

import sys
sys.path.append('../')
import time
import datetime
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

from mplUtils import getFigureProps
from mplUtils import get_pcolorCoordinateAxis

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
    
def plot_pcolor(X, Y, Z, titlestr, fProps, xFormat, yFormat, zFormat, zColor, show_cBar, outname, outdir, showlabels,
    grid = False, saveSVG = False, savePDF = True, savePNG = False, datestamp = True):
            
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
    
    mpl.rc('font',**{'size': 10})
    mpl.rc('legend',**{'fontsize': 8.0})
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
        getFigureProps(width = fProps[0], height = fProps[1], 
                       lFrac = fProps[2], rFrac = fProps[3],
                       bFrac = fProps[4], tFrac = fProps[5])
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)    
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################    
    tick_fontsize = 8.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(tick_fontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(tick_fontsize) 
    
    ax1.tick_params('both', length = 3.0, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 2.0, width = 0.25, which = 'minor', pad = 3.0)
    
    ax1.tick_params(axis='x', which='major', pad = 1.0)
    ax1.tick_params(axis='y', which='major', pad = 1.0, zorder = 10)

    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(xFormat[7], fontsize = 8.0)
    ax1.set_ylabel(yFormat[7], fontsize = 8.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 4.0
    ######################################################################################

    ######################################################################################
    # color map settings
    cMap = zColor[0]
    cNorm = mpl.colors.Normalize(vmin = zColor[1], vmax = zColor[2])
    scalarMap = cm.ScalarMappable(norm = cNorm, cmap = cMap)  
    print "Colormap colornorm limits =", scalarMap.get_clim()
    ######################################################################################
    # colorbar
    if (show_cBar):
        # add_axes(left, bottom, width, height) all between [0, 1] relative to the figure size
        cax = f.add_axes([0.82, bFrac, 0.03, (tFrac - bFrac)])
        
        cax.tick_params('both', length = 3.0, width = 0.5, which = 'major')
        cax.tick_params('both', length = 2.0, width = 0.25, which = 'minor') 
        cax.tick_params(axis = 'both', which = 'major', pad = 2)  

        cb1 = mpl.colorbar.ColorbarBase(cax, 
                                        cmap = cMap,
                                        norm = cNorm,
                                        orientation = 'vertical')

#         cb1.set_label(zColor[3], 
#                       labelpad = 2.5, fontsize = 6)
        
        ax1.annotate(zColor[3],
                     xy = (1.175, 1.06),
                     xycoords = 'axes fraction',
                     fontsize = 8.0, 
                     horizontalalignment = 'right')
        
        cb1.outline.set_linewidth(0.5)
        cb1.ax.tick_params(axis = 'y', direction = 'out', which = 'both')
        cb1.ax.tick_params(labelsize = 8.0)
    
        if (zFormat[0] == 'linear'):
            cb_labels = np.arange(zFormat[1], zFormat[2], zFormat[3])
            cb1.set_ticks(cb_labels)
        # cb1.ax.minorticks_on()
    
    ax1.pcolormesh(X, Y, Z,
                   cmap = cMap,
                   norm = cNorm,
                   edgecolors = 'none')

    #####################################################################################
    # axis formatting
    if (xFormat[0] == 'auto'):
        pass
    if (xFormat[0] == 'linear'):
        ax1.set_xlim(xFormat[1], xFormat[2]) # xmin, xmax
        major_x_ticks = np.arange(xFormat[3], xFormat[4], xFormat[5])
        minor_x_ticks = np.arange(xFormat[3], xFormat[4], xFormat[6])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)

        # manual formatting here:
        # ax1.set_xticklabels([0, 0.5, 1])
    
    elif (xFormat[0] == 'log'):
        ax1.set_xscale('log')
        ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 8))
        ax1.xaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 8,
                                    subs = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
        for label in ax1.xaxis.get_ticklabels()[1::2]:
            label.set_visible(False)
        ax1.set_xlim(xFormat[1], xFormat[2]) # xmin, xmax
    else:
        print "Error: Unknown xFormat[0] type encountered."
        sys.exit(1)
    #####################################################################################
    if (yFormat[0] == 'auto'):
        pass
    if (yFormat[0] == 'linear'):
        ax1.set_ylim(yFormat[1], yFormat[2]) # xmin, xmax
        major_y_ticks = np.arange(yFormat[3], yFormat[4], yFormat[5])
        minor_y_ticks = np.arange(yFormat[3], yFormat[4], yFormat[6])
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)

        # manual formatting here:
        # ax1.set_yticklabels([0, 0.5, 1])
    
    elif (yFormat[0] == 'log'):
        ax1.set_yscale('log')
        ax1.yaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 8))
        ax1.yaxis.set_minor_locator(ticker.LogLocator(base = 10.0, numticks = 8,
                                    subs = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
        for label in ax1.yaxis.get_ticklabels()[1::2]:
            label.set_visible(False)
        ax1.set_ylim(yFormat[1], yFormat[2]) # xmin, xmax
    else:
        print "Error: Unknown yFormat[0] type encountered."
        sys.exit(1)

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
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if (savePNG):
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    if (saveSVG):
        cmd = 'pdf2svg ' + os.path.join(OUTDIR, outname + '.pdf') + \
              ' ' + os.path.join(OUTDIR, outname + '.svg')
        print cmd
        os.system(cmd)
    ######################################################################################
    # close handles
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':
    
    ### create plot data
    
    nSamples_x = 5
    nSamples_y = 5

    xmin, xmax = 0.0, 1.0
    ymin, ymax = 0.0, 1.0

    xVals = np.linspace(xmin, xmax, nSamples_x)
    yVals = np.linspace(ymin, ymax, nSamples_y)

    zVals = np.zeros((nSamples_y, nSamples_x))

    for j in range(nSamples_y): # iterate over y values
        for i in range(nSamples_x): # iterate over x values
            zVals[i, j] = 0.2 * xVals[i]

    #################################################################################
    print "xVals.shape =", xVals.shape
    print "yVals.shape =", yVals.shape
    print "zVals.shape =", zVals.shape
    assert xVals.shape == yVals.shape, "Error: Shape assertion failed."
    assert zVals.shape == (nSamples_x, nSamples_y), "Error: Shape assertion failed."
    #################################################################################

    xBoxCoords = get_pcolorCoordinateAxis(xVals)
    yBoxCoords = get_pcolorCoordinateAxis(yVals)

    assert xBoxCoords.shape == (nSamples_x + 1,), "Error: Shape assertion failed."
    assert yBoxCoords.shape == (nSamples_y + 1,), "Error: Shape assertion failed."
        
    ### call plot function

    fProps = [4.0, 4.0, 0.16, 0.80, 0.20, 0.88]
    xFormat = ['linear', -0.16, 1.16, 0.0, 1.05, 0.5, 0.1, r'x axis label']
    yFormat = ['linear', -0.16, 1.16, 0.0, 1.05, 0.5, 0.1, r'y axis label']

    cMap = cm.viridis #cm.plasma
    zmin = np.min(zVals)
    zmax = np.max(zVals)
    zColor = [cMap, zmin, zmax, r'z label (cbar)']
    zFormat = ['linear', 0.0, 0.21, 0.05]

    outname = plot_pcolor(X = xBoxCoords,
                          Y = yBoxCoords,
                          Z = zVals,
                          titlestr = '',
                          fProps = fProps,
                          xFormat = xFormat,
                          yFormat = yFormat,
                          zFormat = zFormat,
                          zColor = zColor,
                          show_cBar = True,
                          outname = 'pcolor_pseudoColor_plot_linearX_linearY', 
                          outdir = OUTDIR,
                          showlabels = True,
                          grid = False,
                          saveSVG = False)



