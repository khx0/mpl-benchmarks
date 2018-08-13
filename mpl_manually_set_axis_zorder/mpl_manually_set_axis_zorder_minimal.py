#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-08-13
# file: mpl_manually_set_axis_zorder_minimal.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.2
# tested with python 3.7.0  in conjunction with mpl version 2.2.2
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
OUTDIR = os.path.join(BASEDIR, 'out')

ensure_dir(OUTDIR)

if __name__ == '__main__':

    outname = 'mpl_manually_set_axis_zorder_minimal'
    # create data
    nVisPoints = 500
    
    xVals = np.linspace(-0.5, 1.5, nVisPoints)
    yVals1 = np.array([np.sin(x) for x in xVals])
    yVals2 = np.array([np.sin(2.0 * x) - 0.1 for x in xVals])
    X = np.zeros((nVisPoints, 3))
    X[:, 0] = xVals
    X[:, 1] = yVals1
    X[:, 2] = yVals2
    
    ### minimal plot
    f, ax1 = plt.subplots(1)
    
    '''
    Using the zorder keyword we plot the first line below the
    axis, whereas we put the second line above it.
    Comapare the corresponding zorder values:
    zorder = 1 and 11 for the two lines
    and zorder = 10 for the axis, as manually set below.
    The value of zoder = 10 for the axis should be adjusted
    for your individual needs.
    '''
    
    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = 'C0',
             lw = 1.0,
             label = 'data 1',
             clip_on = False,
             zorder = 1)

    ax1.plot(X[:, 0], X[:, 2],
             alpha = 1.0,
             color = 'C1',
             lw = 1.0,
             label = 'data 2',
             clip_on = False,
             zorder = 11)

    ######################################################################################
    ######################################################################################
    # manually set the axis zorder here
    ax1.set_axisbelow(False)
    for k, spine in ax1.spines.items():  #ax.spines is a dictionary
        spine.set_zorder(10)
    ######################################################################################
    ######################################################################################
    
    leg = ax1.legend(handlelength = 1.35, 
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)
        
    ######################################################################################
    # set plot range and scale
    ax1.set_xlim(-0.05, 1.05)              
    
    outname += '_' + now
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf', dpi = 300, transparent = True)
    plt.show()
    
    plt.cla()
    plt.clf()
    plt.close()

    
    
