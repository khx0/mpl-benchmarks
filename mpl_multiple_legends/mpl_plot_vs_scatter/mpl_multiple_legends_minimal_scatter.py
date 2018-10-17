#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-10-17
# file: mpl_multiple_legends_minimal_scatter.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 2.2.3
##########################################################################################

import time
import datetime
import sys
import os
import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
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

if __name__ == '__main__':
    
    outname = 'mpl_multiple_legends_minimal_scatter'
    
    ### create data
    nVisPoints = 20
    xVals = np.linspace(0.0, 1.0, nVisPoints)
    
    yVals1 = [x * (1.0 - x) for x in xVals]
    yVals2 = [2.0 * x * (1.0 - x) for x in xVals] 
    
    X = np.zeros((nVisPoints, 3))
    X[:, 0] = xVals
    X[:, 1] = yVals1
    X[:, 2] = yVals2 
    
    ### minimal plot
    f, ax1 = plt.subplots(1)
    
    ######################################################################################
    '''
    When using matplotlib's standard plot command use
    p, = ax.plot(...)
    to get the correct plot handle as a return value from the plot command.
    
    If you instead use using matplotlib's scatter command use
    p = ax.scatter(...)
    without the comma "," to get the correct plot handle p.
    '''
    ######################################################################################
    # scatter plot 1
    p1 = ax1.scatter(X[:, 0], X[:, 1], 
                     marker = 'o', 
                     s = 50, 
                     facecolors = 'None',
                     alpha = 1.0, 
                     linewidth = 1.0,
                     edgecolors = 'C0', 
                     zorder = 2)
    
    pHandles = [p1]
    labels_1 = [r'scatter 1']
    leg_1 = plt.legend(pHandles, labels_1,
                       loc = 'upper left',
                       handlelength = 0.1,
                       fontsize = 10.0)
    leg_1.draw_frame(False)
    plt.gca().add_artist(leg_1)
    ######################################################################################
    # scatter plot 2
    p2 = ax1.scatter(X[:, 0], X[:, 2], 
                     marker = 'o', 
                     s = 50, 
                     facecolors = 'None',
                     alpha = 1.0, 
                     linewidth = 1.0,
                     edgecolors = 'C3', 
                     zorder = 2)
    
    pHandles = [p2]
    labels_2 = [r'scatter 2']
    leg_2 = plt.legend(pHandles, labels_2,
                       loc = 'upper right',
                       handlelength = 0.1,
                       fontsize = 10.0)
    leg_2.draw_frame(False)
    plt.gca().add_artist(leg_2)
    ######################################################################################
    
    # labeling
    ax1.set_xlabel(r'$x$ label')
    ax1.set_ylabel(r'$y$ label')
    ax1.xaxis.labelpad = 3.5
    ax1.yaxis.labelpad = 5.5
    
    outname += '_' + now
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf', dpi = 300, transparent = True)
    plt.show()
    
    plt.cla()
    plt.clf()
    plt.close()
