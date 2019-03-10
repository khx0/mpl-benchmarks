#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-10
# file: mpl_heatmap_log_xy-scale_demo.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.2  in conjunction with mpl version 3.0.3
##########################################################################################

import sys
sys.path.append('../../')
import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib import ticker

from mplUtils import getFigureProps
from mplUtils import getPcolorBoxCoordinates

from ticker import getLogTicksBase10

from axisPadding import getLogAxisPadding

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

def plot_pcolor(X, Y, Z, titlestr, params,
    fProps, xFormat, yFormat, zFormat, zColor, show_cBar, 
    outname, outdir, showlabels,
    grid = False, saveSVG = False, savePDF = True, savePNG = False, datestamp = True):
    
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
    
    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 8.0})
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
    
    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 1.0, zorder = 10)
    
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(xFormat[7], fontsize = 8.0)
    ax1.set_ylabel(yFormat[7], fontsize = 8.0)
    ax1.xaxis.labelpad = 1.0
    ax1.yaxis.labelpad = 1.0
    ######################################################################################
    
    ######################################################################################
    # color map settings
    cMap = zColor[0]
    cNorm = mpl.colors.Normalize(vmin = zColor[1], vmax = zColor[2])
    scalarMap = cm.ScalarMappable(norm = cNorm, cmap = cMap)  
    print("Colormap colornorm limits =", scalarMap.get_clim())
    ######################################################################################
    # colorbar
    if show_cBar:
        ##########################################################
        # add_axes(left, bottom, width, height) all between [0, 1] 
        # relative to the figure size
        ##########################################################
        cax = f.add_axes([0.86, bFrac, 0.03, (tFrac - bFrac)])
        
        cax.tick_params('both', length = 2.0, width = 0.5, which = 'major')
        cax.tick_params('both', length = 1.0, width = 0.25, which = 'minor') 
        cax.tick_params(axis = 'both', which = 'major', pad = 1.5)  
        
        cb1 = mpl.colorbar.ColorbarBase(cax, 
                                        cmap = cMap,
                                        norm = cNorm,
                                        orientation = 'vertical')
                
        ax1.annotate(zColor[3],
                     xy = (1.175, 1.06),
                     xycoords = 'axes fraction',
                     fontsize = 6.0, 
                     horizontalalignment = 'right')
        
        cb1.outline.set_linewidth(0.5)
        cb1.ax.tick_params(axis = 'y', direction = 'out', which = 'both')
        cb1.ax.tick_params(labelsize = 6.0)
        
        if (zFormat[0] == 'linear'):
            cb_labels = np.arange(zFormat[1], zFormat[2], zFormat[3])
            cb1.set_ticks(cb_labels)
    
    ax1.pcolormesh(X, Y, Z,
                   cmap = cMap,
                   norm = cNorm,
                   edgecolors = 'none')
    
    ######################################################################################
    # z-max / z-min annotation
         
    str1 = r"$z_{\mathrm{max}} = %.5f \,$" %(params[1])
    str2 = r"$z_{\mathrm{min}} = %.5f \,$" %(params[0])
    
    ax1.annotate(str1,
                 xy = (0.0, 1.10),
                 xycoords = 'axes fraction',
                 fontsize = 6.0, 
                 horizontalalignment = 'left')

    ax1.annotate(str2,
                 xy = (0.0, 1.025),
                 xycoords = 'axes fraction',
                 fontsize = 6.0, 
                 horizontalalignment = 'left')
    
    ######################################################################################
    # axis formatting
    if (xFormat[0] == 'auto'):
        pass
    if (xFormat[0] == 'linear'):
        ax1.set_xlim(xFormat[1], xFormat[2]) # xmin, xmax
        major_x_ticks = np.arange(xFormat[3], xFormat[4], xFormat[5])
        minor_x_ticks = np.arange(xFormat[3], xFormat[4], xFormat[6])
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
            
    elif (xFormat[0] == 'log'):
        
        ax1.set_xscale('log')
        ax1.xaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 3))
        
        xMinorTicks = getLogTicksBase10(1.0e1, 1.0e3)
        ax1.xaxis.set_minor_locator(ticker.FixedLocator((xMinorTicks)))
        ax1.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())        
        ax1.set_xlim(xFormat[1], xFormat[2])
    
    else:
        print("Error: Unknown xFormat[0] type encountered.")
        sys.exit(1)
    #####################################################################################
    if (yFormat[0] == 'auto'):
        pass
    if (yFormat[0] == 'linear'):
        ax1.set_ylim(yFormat[1], yFormat[2])
        major_y_ticks = np.arange(yFormat[3], yFormat[4], yFormat[5])
        minor_y_ticks = np.arange(yFormat[3], yFormat[4], yFormat[6])
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)
            
    elif (yFormat[0] == 'log'):
        ax1.set_yscale('log')
        
        ax1.yaxis.set_major_locator(ticker.LogLocator(base = 10.0, numticks = 3))
        yMinorTicks = getLogTicksBase10(1.0e-3, 1.0e-1)
        ax1.yaxis.set_minor_locator(ticker.FixedLocator((yMinorTicks)))
        ax1.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())        
        ax1.set_ylim(yFormat[1], yFormat[2])
    else:
        print("Error: Unknown yFormat[0] type encountered.")
        sys.exit(1)
    
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
        f.savefig(os.path.join(outdir, outname) + '.pdf',
                  dpi = 300,
                  transparent = True)
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png',
                  dpi = 600,
                  transparent = False)
    if saveSVG:
        cmd = 'pdf2svg ' + os.path.join(OUTDIR, outname + '.pdf') + \
              ' ' + os.path.join(OUTDIR, outname + '.svg')
        os.system(cmd)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':
    
    params = [(31, 0.035, cm.viridis, 'viridis'),
              (31, 0.035, cm.magma, 'magma'),
              (31, 0.035, cm.gray, 'gray'),
              (31, 0.035, cm.plasma, 'plasma')] 
      
    for nDataPoints, paddingFraction, cMap, cMapString in params:
        
        filename = 'demo_nDataPoints_{}_cMap_{}'.format(nDataPoints, cMapString)
        
        # create dummy data
        Z = np.zeros((nDataPoints, nDataPoints))
        print('Z.shape =', Z.shape)
        
        xVals = np.logspace(1, 3, nDataPoints)
        yVals = np.logspace(-3, -1, nDataPoints)
    
        # fill Z matrix
        for i in range(len(yVals)):
            for j in range(len(xVals)):
                Z[i, j] = np.sin(np.pi * np.log(yVals[i])) * \
                          np.cos(np.pi * np.log(xVals[j]) - np.pi / 2.0)
    
        Z_min = np.min(Z)
        Z_max = np.max(Z)
        
        xBoxCoords = getPcolorBoxCoordinates(xVals, 'log')
        yBoxCoords = getPcolorBoxCoordinates(yVals, 'log')
        
        assert xBoxCoords.shape == (len(xVals) + 1,), "Error: Shape assertion failed."
        assert yBoxCoords.shape == (len(yVals) + 1,), "Error: Shape assertion failed."
        
        # call plot function
        fProps = [3.5, 3.5, 0.20, 0.84, 0.16, 0.88]
        
        xminData = 1.0e1
        xmaxData = 1.0e3
        xmin, xmax = getLogAxisPadding(xminData, xmaxData, paddingFraction)
        
        yminData = 1.0e-3
        ymaxData = 1.0e-1
        ymin, ymax = getLogAxisPadding(yminData, ymaxData, paddingFraction)
        
        xFormat = ['log', xmin, xmax, -1.0, -1.0, -1.0, -1.0,
                   r'x label $x$']
        yFormat = ['log', ymin, ymax, -1.0, -1.0, -1.0, -1.0,
                   r'y label $y$']
        
        # absolute scaling
        # cMap = cm.viridis # cm.plasma
        zmin = -1.0
        zmax = 1.0
        zColor = [cMap, zmin, zmax, r'z label $\, z$']
        zFormat = ['linear', -1.0, 1.1, 0.5]
        
        plot_pcolor(X = xBoxCoords,
                    Y = yBoxCoords,
                    Z = Z,
                    titlestr = '',
                    params = [Z_min, Z_max],
                    fProps = fProps,
                    xFormat = xFormat,
                    yFormat = yFormat,
                    zFormat = zFormat,
                    zColor = zColor,
                    show_cBar = True,
                    outname = filename, 
                    outdir = OUTDIR,
                    showlabels = True,
                    grid = False,
                    savePDF = True,
                    saveSVG = True,
                    savePNG = False)
