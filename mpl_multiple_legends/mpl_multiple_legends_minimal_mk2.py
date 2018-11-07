#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-12
# file: mpl_multiple_legends_minimal_mk2.py
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
    
    outname = 'mpl_multiple_legends_minimal_mk2'
    
    ### create data
    nVisPoints = 500
    xVals = np.linspace(0.0, 1.0, nVisPoints)
    
    yVals1 = [1.0 * x for x in xVals]
    yVals2 = [1.5 * x for x in xVals] 
    yVals3 = [2.0 * x for x in xVals] 
    
    X = np.zeros((nVisPoints, 4))
    X[:, 0] = xVals
    X[:, 1] = yVals1
    X[:, 2] = yVals2
    X[:, 3] = yVals3 
    
    ### minimal plot
    f, ax1 = plt.subplots(1)
    
    p1, = ax1.plot(X[:, 0], X[:, 1], 
                   alpha = 1.0,
                   color = 'C0', 
                   zorder = 1)
    p1 = [p1]
    
    p2, = ax1.plot(X[:, 0], X[:, 2], 
                   alpha = 1.0,
                   color = 'C1', 
                   zorder = 1)    
    p2 = [p2]
    
    p3, = ax1.plot(X[:, 0], X[:, 3], 
                   alpha = 1.0,
                   color = 'C2', 
                   zorder = 1)
    p3 = [p3]
    
    label1 = [r'line 1']
    label2 = [r'line 2']
    label3 = [r'line 3']
    
    leg1 = plt.legend(p1, label1,
                      loc = 'upper left',
                      handlelength = 2.0,
                      fontsize = 10.0)
    leg1.draw_frame(False)
    plt.gca().add_artist(leg1)
    
    leg2 = plt.legend(p2, label2,
                      loc = 'lower right',
                      handlelength = 2.0,
                      fontsize = 10.0)
    leg2.draw_frame(False)
    plt.gca().add_artist(leg2)
    
    leg3 = plt.legend(p3, label3,
                      bbox_to_anchor = [0.0, 0.5],
                      loc = 'upper left',
                      handlelength = 2.0,
                      fontsize = 10.0)
    leg3.draw_frame(False)
    plt.gca().add_artist(leg3)
    
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


