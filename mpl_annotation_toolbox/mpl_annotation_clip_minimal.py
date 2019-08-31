#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-08-31
# file: mpl_annotation_clip_minimal.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.1
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

'''
mpl_annotation_clip example
This example illustrates three annotation related findings:
a) The difference between using xycoords = 'data' and xycoords = 'axes fraction' to 
place an annotation in a matplotlib plot.
b) How to place annotations outside of the plot / figure axes. When using
xcoords = 'axes fraction' this is possible without further ado. For some reason
(not sure if this is intended) one has to add the keyword
    annotation_clip = False
when using xycoords = 'data'. Using the clip_on = False keyword, which works to extend
regular plot commands to regions outside of the axes, does also not seem to work for 
matplotlib annotations.
c) How to use the (manually or automatically) set x- and y-limits to convert
an absolute coordinate placement ('data') into a relative placement ('axes fraction').
For this conversion we use pyplot's plt.xlim() and plt.ylim() functions.
'''

'''







'''

if __name__ == '__main__':

    outname = 'mpl_annotation_clip_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    # create dummy data
    nVisPoints = 500
    xVals = np.linspace(120.0, 820.0, nVisPoints)
    yVals = xVals
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    f, ax1 = plt.subplots(1)
    f.subplots_adjust(right = 0.7)
    
    ax1.plot(X[:, 0], X[:, 1],
             alpha = 1.0,
             color = 'C0',
             clip_on = False,
             zorder = 1)

    # annotations
 
    # place a center label using data coordinates
    ax1.annotate('center label in data coords',
                 xy = (500.0, 500.0),
                 xycoords = 'data',
                 horizontalalignment = 'center',
                 verticalalignment = 'center')
                 
    ax1.annotate('label crossing the right axis',
                 xy = (800.0, 500.0),
                 xycoords = 'data',
                 horizontalalignment = 'left',
                 verticalalignment = 'center')
                 
    # specify the (x, y) position in data coordinates
    xPos_data = 870.0
    yPos_data = 400.0
    ax1.annotate(r"outside label ('data')",
                 xy = (xPos_data, yPos_data),
                 xycoords = 'data',
                 horizontalalignment = 'left',
                 verticalalignment = 'center',
                 annotation_clip = False)

    yPos_data = 300.0

    # convert absolute ('data') coordinates into relative ('axes fraction') coordinates
    xmin, xmax = plt.xlim() # return the current xlim
    ymin, ymax = plt.ylim()	# return the current ylim
    dx, dy = xmax - xmin, ymax - ymin
    xPos_axes = (xPos_data - xmin) / dx
    yPos_axes = (yPos_data - ymin) / dy

    ax1.annotate(r"outside label ('axes fraction')",
                 xy = (xPos_axes, yPos_axes),
                 xycoords = 'axes fraction',
                 horizontalalignment = 'left',
                 verticalalignment = 'center')
             
    # Using xycoords = 'data' and the keyword clip_on = False does not work to place 
    # annotations outside of the axes.
    xPos_data = 870.0
    yPos_data = 200.0
    ax1.annotate(r"outside label ('data') (clip_on = False)",
                 xy = (xPos_data, yPos_data),
                 xycoords = 'data',
                 horizontalalignment = 'left',
                 verticalalignment = 'center',
                 clip_on = False)

    # set axes labels
    ax1.set_xlabel(r'x label')
    ax1.set_ylabel(r'y label')

    # save to file
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf', 
              dpi = 300, 
              transparent = True)

    plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
