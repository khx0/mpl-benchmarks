 #!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-04-09
# file: mplUtils.py
##########################################################################################

import sys
import time
import datetime
import os
import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib import gridspec
from matplotlib import ticker

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

now = datetime.datetime.now()
now = "%s-%s-%s" %(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

def getFigureProps(width, height, lFrac = 0.17, rFrac = 0.9, bFrac = 0.17, tFrac = 0.9):
    '''
    Specify widht and height in cm
    '''
    axesWidth = width / 2.54 # convert to inches
    axesHeight = height / 2.54 # convert to inches
    fWidth = axesWidth / (rFrac - lFrac)
    fHeight = axesHeight / (tFrac - bFrac)
    return fWidth, fHeight, lFrac, rFrac, bFrac, tFrac

def get_pcolorCoordinateAxis(X, type = 'linear'):
    if (type == 'linear'):
        dx = X[1] - X[0]
        Xcoords = np.linspace(X[0] - dx / 2.0, X[-1] + dx / 2.0, len(X) + 1)
    elif (type == 'log'):
        dx = np.log10(X[1] / X[0])
        minExp = np.log10(X[0])
        maxExp = np.log10(X[-1])
        Xcoords = np.logspace(minExp - dx / 2.0, maxExp + dx / 2.0, len(X) + 1)
    else:
        print "Error: Unknown type encountered."
        sys.exit(1)
    return Xcoords

if __name__ == '__main__':

    pass

