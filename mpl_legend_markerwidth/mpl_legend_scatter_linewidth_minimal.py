#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-11-26
# file: mpl_legend_scatter_linewidth_minimal.py
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

    # fix random seed for reproducibility
    np.random.seed(123456789)

    ### create plot data
    nDatapoints = 500
    xVals = np.random.normal(0.5, 0.15, nDatapoints)
    yVals = np.random.normal(0.5, 0.2, nDatapoints)
    X = np.zeros((nDatapoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    outname = 'mpl_legend_scatter_linewidth_minimal'
    
    f, ax1 = plt.subplots(1)
    f.set_size_inches(3.0, 3.0)   
    
    ax1.scatter(X[:, 0], X[:, 1], 
                s = 3.0,
                marker = 'o', 
                facecolors = 'None',
                edgecolors = 'C0', 
                alpha = 1.0, 
                linewidth = 0.2, 
                zorder = 3,
                label = r'scatter label')
                         
    ###############################################
    ###############################################
    # legend handling           
    leg = ax1.legend(handlelength = 0.1,
                     markerscale = 3.5)
                     
    '''
    The linewidth of the legend object can be manually
    adjusted by the two code lines below,
    by using the
    legobj.set_linewidth(WIDTH)
    function.
    '''

    # set the linewidth of the legend object
    for i, legobj in enumerate(leg.legendHandles):
        legobj.set_linewidth(1.0)

    leg.draw_frame(False)
    ###############################################
    ###############################################  
    
    outname += '_' + now
    f.savefig(os.path.join(OUTDIR, outname + '.pdf'), dpi = 300, transparent = True)
    plt.cla()
    plt.clf()
    plt.close()
    