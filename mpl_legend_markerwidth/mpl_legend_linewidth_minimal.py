#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-08-12
# file: mpl_legend_linewidth_minimal.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.2
# tested with python 3.7.0  in conjunction with mpl version 2.2.2
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
    nDatapoints = 200
    xVals = np.linspace(0.0, 1.0, nDatapoints)
    yVals = np.array([x for x in xVals])
    X = np.zeros((nDatapoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals
    
    outname = 'mpl_legend_linewidth_minimal'
    
    f, ax1 = plt.subplots(1)
    f.set_size_inches(3.0, 3.0)   
    
    ax1.plot(X[:, 0], X[:, 1],
            color = 'C0',
            alpha = 1.0,
            lw = 0.5,
            zorder = 2,
            label = r'line label')
    
    ###############################################
    ###############################################
    # legend handling           
    leg = ax1.legend(handlelength = 2.0)
    
    '''
    The linewidth of the legend object can be manually
    adjusted by the two code lines below,
    by using the
    legobj.set_linewidth(WIDTH)
    function.
    Here this is used to adjust the linewidth of the 
    scatter symbol.
    '''

    # set the linewidth of the legend object
    for i, legobj in enumerate(leg.legendHandles):
        legobj.set_linewidth(4.0)

    leg.draw_frame(False)
    ###############################################
    ###############################################  
    
    outname += '_' + now
    f.savefig(outname + '.pdf', dpi = 300, transparent = True)
    plt.cla()
    plt.clf()
    plt.close()
            

    
    
