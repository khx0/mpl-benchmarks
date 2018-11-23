#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-11-23
# file: mpl_empty_contour_minimal.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 3.0.1
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

if __name__ == '__main__':

    outname = 'mpl_empty_contour_minimal'

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
    
    pColors = ['k']
    
    ### minimal plot
    f, ax1 = plt.subplots(1)
    f.set_size_inches(2.0, 2.0)
    
    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = pColors[0],
             lw = 1.0,
             clip_on = True,
             zorder = 1)

    ax1.set_xlim(-55.0, 55.0)
    ax1.set_ylim(-55.0, 55.0)

    ax1.set_xticks([])
    ax1.set_yticks([])
    
    plt.axis('off')
    
    ### save plot to file
    outname += '_' + now
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf', dpi = 300, transparent = True)
    plt.show()
    plt.cla()
    plt.clf()
    plt.close()
