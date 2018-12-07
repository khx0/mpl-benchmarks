#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-12-07
# file: mpl_standalone_colorbar.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 3.0.1
##########################################################################################

import os
import platform
import time
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

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

def Plot(titlestr, X, params, outname, outdir, pColors, cMap,
         grid = True, savePDF = True, savePNG = False, datestamp = True):
    
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = False
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['ytick.left'] = False
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    
    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 9.0})
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
        getFigureProps(width = 0.4, height = 3.5, 
                       lFrac = 0.10, rFrac = 0.32,
                       bFrac = 0.1, tFrac = 0.9)

    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)    
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    
    major_x_ticks = np.arange(0.0, 1.1, 0.5)
    minor_x_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_xticks(major_x_ticks)
    ax1.set_xticks(minor_x_ticks, minor = True)
    
    major_y_ticks = np.arange(0.0, 1.1, 0.5)
    minor_y_ticks = np.arange(0.0, 1.1, 0.1)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    
    labelfontsize = 10.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    
    ax1.tick_params('both', length = 5.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 3.0, width = 0.25, which = 'minor', pad = 3.0)
    
    ax1.tick_params(axis = 'x', which = 'major', pad = 3.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 3.0, zorder = 10)
    
    ######################################################################################
    # colormap settings
    cmap_min = 0.0
    cmap_max = 1.0
    print('cmap_min = ', cmap_min)
    print('cmap_max = ', cmap_max)
    cNorm = mpl.colors.Normalize(vmin = cmap_min, vmax = cmap_max)
    ######################################################################################
    # plot (dummy) data
    ax1.imshow(X, cmap = cMap, vmin = cmap_min, vmax = cmap_max)
    plt.gca().set_visible(False)
    ######################################################################################
    # colorbar
    # add_axes(left, bottom, width, height) all between [0, 1] relative to the figure size
    
    cb_label = params[0]
    
    cax = f.add_axes([lFrac, bFrac, (rFrac - lFrac), (tFrac - bFrac)])
    
    cax.tick_params('both', length = 4.5, width = 0.5, which = 'major', pad = 3.0)
    cax.tick_params('both', length = 3.0, width = 0.25, which = 'minor', pad = 3.0)
    cax.tick_params(axis = 'both', which = 'major', pad = 2)
    
    cb1 = mpl.colorbar.ColorbarBase(cax, 
                                    cmap = cMap,
                                    norm = cNorm,
                                    orientation = 'vertical')
                                       
    cb1.set_label(cb_label, labelpad = 5.0, fontsize = 10.0)
    cb1.outline.set_linewidth(0.5)

    cb_labels = np.arange(0.0, 1.1, 0.5)
    cb1.set_ticks(cb_labels)
    cb1.set_ticklabels([0, 0.5, 1])
    cb1.ax.tick_params(labelsize = 10.0)
    cb1.ax.minorticks_on()  
    # cb1.solids.set_rasterized(True)  
    
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
    return outname

if __name__ == '__main__':
    
    X = np.array([[0, 1]])
       
    cb_label = r'color bar label $\, z$'

    cMaps = [cm.viridis,
             cm.plasma,
             cm.inferno,
             cm.magma,
             cm.gray]

    outnames = ['mpl_standalone_colorbar_viridis',
                'mpl_standalone_colorbar_plasma',
                'mpl_standalone_colorbar_inferno',
                'mpl_standalone_colorbar_magma',
                'mpl_standalone_colorbar_gray']

    assert len(cMaps) == len(outnames), "Length assertion failed."

    for i, cMap in enumerate(cMaps):
        
        outname = outnames[i]
        outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

        outname = Plot(titlestr = '',
                       X = X, 
                       params = [cb_label],
                       outname = outname, 
                       outdir = OUTDIR, 
                       pColors = [],
                       cMap = cMap,
                       grid = False)
