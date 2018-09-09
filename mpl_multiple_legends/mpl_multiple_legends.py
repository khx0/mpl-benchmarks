#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: nikolas.schnellbaecher@bioquant.uni-heidelberg.de
# date: 2018-09-09
# file: mpl_multiple_legends.py
##########################################################################################

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

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, './')

def getFigureProps(width, height):
    '''
    Specify widht and height in cm
    '''
    lFrac, rFrac = 0.15, 0.95
    bFrac, tFrac = 0.15, 0.95
    axesWidth = width / 2.54 # convert to inches
    axesHeight = height / 2.54 # convert to inches
    fWidth = axesWidth / (rFrac - lFrac)
    fHeight = axesHeight / (tFrac - bFrac)
    return fWidth, fHeight, lFrac, rFrac, bFrac, tFrac

def Plot(titlestr, Xs, X, params, outname, outdir, pColors,
         grid = True, savePDF = True, savePNG = False, datestamp = True):
    
    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    
    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 8.0})
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
        getFigureProps(width = 7.5, height = 6.0)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)    
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    
    ######################################################################################
    # ticks
    major_x_ticks = np.arange(0.0, 40.1, 20.0)
    minor_x_ticks = np.arange(0.0, 40.1, 5.0)
    ax1.set_xticks(major_x_ticks)
    ax1.set_xticks(minor_x_ticks, minor = True)

    major_y_ticks = np.arange(0.0, 0.20, 0.05)
    minor_y_ticks = np.arange(0.0, 0.20, 0.01)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    
    labelfontsize = 10.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    
    ax1.tick_params('both', length = 3.5, width = 0.5, which = 'major', pad = 3.0)
    ax1.tick_params('both', length = 2.0, width = 0.25, which = 'minor', pad = 3.0)
    
    ax1.tick_params(axis='x', which='major', pad = 3.0)
    ax1.tick_params(axis='y', which='major', pad = 3.0, zorder = 10)
    
    ######################################################################################
    # labeling
    plt.title(titlestr)
    ax1.set_xlabel(r'$x$ label', fontsize = 10.0)
    ax1.set_ylabel(r'$y$ label', fontsize = 10.0)
    ax1.xaxis.labelpad = 3.5
    ax1.yaxis.labelpad = 5.5
    
    ######################################################################################
    # plot data
    
    pHandles = []
    
    for i in range(len(params)):
    
        p, = ax1.plot(X[:, 0], X[:, i + 1], 
                      alpha = 1.0, 
                      linewidth = 0.5, 
                      color = pColors[i], 
                 zorder = 1)
                 #label = labels[i])
                 
        pHandles.append(p)
    
    labels = [r'$\mathcal{A} = 2.5\cdot 10^{-4}$',
              r'$\mathcal{A} = 1.5\cdot 10^{-4}$',
              r'$\mathcal{A} = 5 \cdot 10^{-5}$']
    
    legLeft = plt.legend(pHandles, labels,
                         loc = 'upper left',
                         handlelength = 2.0)
    legLeft.draw_frame(False)
    plt.gca().add_artist(legLeft)
    
    for i in range(len(params)):
      
        ax1.scatter(Xs[:, 0], Xs[:, i + 1], 
                    marker = '+', 
                    s = 50, 
                    facecolors = pColors[i],
                    alpha = 1.0, 
                    linewidth = 0.5,
                    edgecolors = pColors[i], 
                    zorder = 2)

        ax1.scatter(Xs[:, 0], Xs[:, i + 1], 
                    marker = 'v', 
                    s = 30, 
                    facecolors = 'None',
                    alpha = 1.0, 
                    linewidth = 0.5,
                    edgecolors = pColors[i], 
                    zorder = 2)

        ax1.scatter(Xs[:, 0], Xs[:, i + 1], 
                    s = 28, 
                    facecolors = 'None',
                    alpha = 1.0, 
                    linewidth = 0.5,
                    edgecolors = pColors[i], 
                    zorder = 2)
    
    # dummy data for manual scatterpoint legend
    x = [-10.0]
    y = [-10.0]
    dummyColor = '#666666'
    ax1.scatter(x, y, 
                marker = '+', 
                s = 38, 
                facecolors = dummyColor, 
                alpha = 1.0, 
                linewidth = 1.0, 
                edgecolors = dummyColor, 
                label = 'M1')
    ax1.scatter(x, y, 
                marker = 'v', 
                s = 33, 
                facecolors = 'none', 
                alpha = 1.0, 
                linewidth = 1.0, 
                edgecolors = dummyColor, 
                label = 'M2')
    ax1.scatter(x, y, 
                facecolors = 'none', 
                alpha = 1.0, 
                s = 28, 
                linewidth = 1.0, 
                edgecolors = dummyColor, 
                label = 'M3')
    
    ######################################################################################
    # legend
    mpl.rc('legend',**{'fontsize': 9.0})
    leg = ax1.legend(loc = 'upper right',
                     handlelength = 0.1, 
                     scatterpoints = 1,
                     ncol = 1)
    leg.draw_frame(False)
    ######################################################################################
    # set plot range and scale
    ax1.set_xlim(0.0, 40.0)    
    ax1.set_ylim(0.0, 0.135)
    ax1.set_axisbelow(False)
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
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return None

if __name__ == '__main__':
        
    ### create synthetic data
    
    nVisPoints = 500
    nScatterPoints = 20
    Lx = 40.0
    xVals = np.linspace(0.0, Lx, nVisPoints)
    xVals2 = np.linspace(0.0, Lx, nScatterPoints)
    
    amplitudes = [0.00025, 0.00015, 0.00005]

    X = np.zeros((nVisPoints, 4))
    Xs = np.zeros((nScatterPoints, 4))
    
    for i in range(len(amplitudes)):
       
        yVals = [amplitudes[i] * x * (Lx - x) for x in xVals]
        X[:, i + 1] = yVals
    
        yVals2 = [amplitudes[i] * x * (Lx - x) for x in xVals2] 
        Xs[:, i + 1] = yVals2
    
    X[:, 0] = xVals
    Xs[:, 0] = xVals2
    
    ### call plotting function
         
    pColors = ['k', 'C3', 'C0']
     
    Plot(titlestr = '', 
         Xs = Xs, 
         X = X, 
         params = amplitudes, 
         outname = 'mpl_multiple_legends', 
         outdir = OUTDIR, 
         pColors = pColors,
         grid = False, 
         savePDF = True, 
         savePNG = False, 
         datestamp = True)




