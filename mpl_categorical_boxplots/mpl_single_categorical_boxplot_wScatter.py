#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-02-07
# file: mpl_single_categorical_boxplot_wScatter.py
# tested with python 3.7.6 and matplotlib 3.3.4
##########################################################################################

# TODO: update with bee scatter algorithm
# TODO: find alternative better scatter point visualizations

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

def create_boxplot(X, outname, outdir = './', x_label = None, y_label = None,
	pColors = None, datestamp = True, savePDF = True, savePNG = False):
    '''
    cretaes a single categorical (x - axis) boxplot using the given data sample X
    :params X: numpy.ndarray
    '''

    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 3.0, height = 4.0,
                       lFrac = 0.28, rFrac = 0.95,
                       bFrac = 0.20, tFrac = 0.95)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################

    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    # boxplot parameter
    xPos = [1.0]
    width = 0.2

    bp1 = ax1.boxplot(X, widths = width)

    xVals = np.array(len(X) * xPos) + 0.25

    ax1.scatter(xVals, X,
                s = 8.0,
                alpha = 0.45,
                facecolor = pColors[0],
                edgecolor = 'None',
                zorder = 2)

    if pColors:
        plt.setp(bp1['medians'], color = pColors[0])

    if x_label:
        ax1.set_xlabel(x_label)
    if y_label:
        ax1.set_ylabel(y_label)

    ax1.set_xticks(xPos)
    ax1.set_xticklabels([r'category'])

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

    print(__file__)
    print("running on python", platform.python_version())
    print("using mpl.__version__ =", mpl.__version__)

    filename = r'normal_samples_np_seed_987654321.npy'

    data = np.load(os.path.join(RAWDIR, filename))
    print("data.shape =", data.shape)

    outname = 'mpl_single_categorical_boxplot_wScatter'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    x_label = r'optional $x$ label'
    y_label = r'$y$ label'

    create_boxplot(X = data,
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = ['C3'],
                   x_label = x_label,
                   y_label = y_label)
