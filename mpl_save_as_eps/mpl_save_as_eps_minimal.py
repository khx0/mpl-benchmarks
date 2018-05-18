#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-05-18
# file: mpl_save_as_eps_minimal.py
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

    outname = 'mpl_save_as_eps_minimal'
    
    ### create data
    nVisPoints = 500
    xVals = np.linspace(0.0, 1.0, nVisPoints)
    yVals = np.array([np.sin(x) for x in xVals])
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    ### minimal plot
    f, ax1 = plt.subplots(1)
    
    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = 'C0',
             lw = 1.0,
             label = 'data',
             clip_on = False,
             zorder = 1)

    leg = ax1.legend(handlelength = 1.5, 
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)
        
    ### set plot range and scale
    ax1.set_xlim(-0.05, 1.05)              
    
    ### save plot to file
    outname += '_' + now
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf', dpi = 300, transparent = True)
    f.savefig(os.path.join(OUTDIR, outname) + '.eps', dpi = 600, format = 'eps')
    plt.show()
    plt.clf()
    plt.close()

    
    
