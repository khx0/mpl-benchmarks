#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-08-31
# file: mpl_empty_contour.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 2.2.3
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

def Plot(titlestr, X, outname, outdir, pColors,
         grid = True, saveEPS = False, savePDF = True, savePNG = False, datestamp = True):
    
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = False
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'
    
    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.5})
    mpl.rc("axes", linewidth = 0.5)    
    
    plt.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    plt.rcParams['pdf.fonttype'] = 42  
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}', r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)      
    
    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 4.0, height = 4.0,
                       lFrac = 0.1, rFrac = 0.9, bFrac = 0.1, tFrac = 0.9)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)    
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    
    ######################################################################################
    # labeling
    ######################################################################################
        
    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = pColors[0],
             lw = 1.0,
             clip_on = True,
             zorder = 1)
    
    # plt.axes().set_aspect('equal')
            
    ######################################################################################
    # set plot range and scale
    #ax1.set_xlim(0.0, 628.0)
    #ax1.set_ylim(0.0, 628.0)
    ax1.set_axisbelow(False)
    ######################################################################################
    
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    plt.axis('off')
    
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
    return outname

if __name__ == '__main__':

	# create data
    nDataPoints = 500
    radius = 50.0
    angles = np.linspace(0.0, 2.0 * np.pi, nDataPoints)
    xVals = np.array([radius * np.cos(x) for x in angles])
    yVals = np.array([radius * np.sin(x) for x in angles])

    X = np.zeros((nDataPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    print("X.shape =", X.shape)

    # plot data                    
    outname = Plot(titlestr = '',
         		   X = X,
         		   outname = 'mpl_empty_contour',
         		   outdir = OUTDIR, 
         		   pColors = ['k'],
         		   grid = False)
         
