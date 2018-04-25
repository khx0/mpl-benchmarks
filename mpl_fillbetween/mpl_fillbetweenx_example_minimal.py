#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-04-23
# file: mpl_fillbetweenx_example_minimal.py
##########################################################################################

'''
Minimal example to illustrate the use of matplotlib's fillbetweenx function.
Sometimes I use flipped plots to illustrate histograms or distributions, and
the overall layout of the figure needs a given plot to work with switched
x and y values. So I basically want the same functionality as the fillbetween
function, but with exchanged roles for x and y. For this purpose matplotlib's
fillbetweenx function is the ideal choice.
'''

import sys
import time
import datetime
import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend
from scipy.stats import norm

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
    
    nPoints = 400
    xVals = np.linspace(-6.0, 6.0, nPoints)
    yVals = norm.pdf(xVals, 0.0, 1.0)
    X = np.zeros((nPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    outname = 'mpl_fillbetweenx_example_minimal_' + now
    
    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'x label', fontsize = 8.0)
    ax1.set_ylabel(r'y label', fontsize = 8.0)
    ax1.xaxis.labelpad = 2.0
    ax1.yaxis.labelpad = 2.0  

    ax1.fill_betweenx(X[:, 0], X[:, 1], 0.0,
                     color = 'C0',
                     alpha = 0.5,
                     lw = 0.0)
    
    ax1.plot(X[:, 1], X[:, 0], 
             color = 'C0',
             alpha = 1.0,
             lw = 1.5,
             zorder = 3,
             label = r'legend')

    leg = ax1.legend(handlelength = 1.5, 
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)
    plt.gca().add_artist(leg)

    f.savefig(os.path.join(OUTDIR, outname) + '.pdf', dpi = 300, transparent = True);
    plt.clf()
    plt.close()


    
