#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-08-30
# file: mpl_minimal_annotation_clip_snippet.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.1
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

# set output filename
today = datetime.datetime.now().strftime("%Y-%m-%d")
outname = 'mpl_minimal_annotation_clip_snippet'
outname += '_Python_' + platform.python_version() + \
           '_mpl_' + mpl.__version__ + '_' + today

# create dummy data
xVals = np.linspace(120.0, 820.0, 100)
yVals = xVals

# plotting
f, ax1 = plt.subplots(1)
f.subplots_adjust(right = 0.65)
ax1.plot(xVals, yVals)

# specify the (x, y) position in data coordinates
(xPos_data, yPos_data) = (870.0, 400.0)

# only visible when using the annotation_clip = False keyword
ax1.annotate(r"outside label ('data')",
             xy = (xPos_data, yPos_data),
             xycoords = 'data',
             horizontalalignment = 'left',
             annotation_clip = False)

# Using xycoords = 'data' and the keyword clip_on = False does not work to place 
# annotations outside of the axes.
yPos_data = 300.0
ax1.annotate(r"outside label ('data') (clip_on = False)",
             xy = (xPos_data, yPos_data),
             xycoords = 'data',
             horizontalalignment = 'left',
             clip_on = False)

yPos_data = 200.0

# convert absolute ('data') coordinates into relative ('axes fraction') coordinates
xmin, xmax = plt.xlim()
ymin, ymax = plt.ylim()
dx, dy = xmax - xmin, ymax - ymin
xPos_axes = (xPos_data - xmin) / dx
yPos_axes = (yPos_data - ymin) / dy

# annotation visible without any additional keyword when using xycoords = 'axes fraction'
ax1.annotate(r"outside label ('axes fraction')",
             xy = (xPos_axes, yPos_axes),
             xycoords = 'axes fraction',
             horizontalalignment = 'left')

# save to file
f.savefig(os.path.join('./out', outname) + '.png', dpi = 300)
plt.show()
