#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-03-28
# file: mpl_AB_categorical_boxplot.py
# tested with python 3.7.6 and matplotlib 3.2.1
##########################################################################################

import os
import datetime
import platform
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)
os.makedirs(OUTDIR, exist_ok = True)

def getFigureProps(width, height, lFrac = 0.17, rFrac = 0.9, bFrac = 0.17, tFrac = 0.9):
    '''
    True size scaling auxiliary function to setup mpl plots with a desired size.
    Specify widht and height in cm.
    lFrac = left fraction   in [0, 1]
    rFrac = right fraction  in [0, 1]
    bFrac = bottom fraction in [0, 1]
    tFrac = top fraction    in [0, 1]
    returns:
        fWidth = figure width
        fHeight = figure height
    These figure width and height values can then be used to create a figure instance
    of the desired size, such that the actual plotting canvas has the specified
    target width and height, as provided by the input parameters of this function.
    '''
    axesWidth = width / 2.54    # convert to inches
    axesHeight = height / 2.54  # convert to inches
    fWidth = axesWidth / (rFrac - lFrac)
    fHeight = axesHeight / (tFrac - bFrac)
    return fWidth, fHeight, lFrac, rFrac, bFrac, tFrac

def create_boxplot(X, outname, outdir = './', xLabel = None, yLabel = None,
	pColors = None, datestamp = True, savePDF = True, savePNG = False):
    '''
    cretaes a single categorical (x - axis) boxplot using the given data sample X
    :params X: numpy.ndarray
    '''

    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 3.0, height = 4.0,
                       lFrac = 0.28, rFrac = 0.95, bFrac = 0.20, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################
    
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    # boxplot parameter
    xPos = [1.0, 2.0]
    width = 0.4
    
    bp1 = ax1.boxplot(X[:, 0],
                      positions = [xPos[0]],
    				  widths = width)

    bp2 = ax1.boxplot(X[:, 1],
                      positions = [xPos[1]],
    				  widths = width)

    if pColors:
    	plt.setp(bp1['medians'], color = pColors[0])
    	plt.setp(bp2['medians'], color = pColors[1])

    if xLabel:
    	ax1.set_xlabel(xLabel)
    if yLabel:
    	ax1.set_ylabel(yLabel)

    ax1.set_xticks(xPos)
    ax1.set_xticklabels([r'A', r'B'])

    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + today
    if savePDF: # save to file using pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return outname

if __name__ == '__main__':

    print("running on python", platform.python_version())
    print("using mpl.__version__ =", mpl.__version__)

    filename = r'normal_samples_AB_np_seed_987654321.npy'

    data = np.load(os.path.join(RAWDIR, filename))
    print(data.shape)

    outname = 'mpl_AB_categorical_boxplot'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    xLabel = r''
    yLabel = r'$y$ label'

    create_boxplot(X = data,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = ['C3', 'C0'],
                   xLabel = xLabel,
                   yLabel = yLabel)
