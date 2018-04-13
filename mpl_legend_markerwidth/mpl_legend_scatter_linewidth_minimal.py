#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-04-13
# file: mpl_legend_scatter_linewidth_minimal.py
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

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

if __name__ == '__main__':

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
    f.savefig(outname + '.pdf', dpi = 300, transparent = True)
    plt.clf()
    plt.close()
            

    
    
