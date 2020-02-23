#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-02-23
# file: plot_uncorrelateGaussian_wMarginals.py
# tested with python 3.7.6 in conjunction with mpl version 3.1.3
##########################################################################################
# description: plots the uncorrelated data samples that can be generated using the
# provided create_samples.py script
##########################################################################################

import os
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend
from matplotlib.ticker import FuncFormatter

import scipy
from scipy.stats import norm

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def cleanFormatter(x, pos = None):
    '''
    will format 0.0 as 0 and
    will format 1.0 as 1
    '''
    return '{:g}'.format(x)

def Plot(titlestr, X, marginalX, marginalY, params, outname, outdir, pColors,
         drawLegend = True, xFormat = None, yFormat = None,
         savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 7.0})
    mpl.rc('legend', **{'fontsize': 7.0})
    mpl.rc('axes', linewidth = 0.5)

    # mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Myriad Pro']})
    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fontparams = {'text.latex.preamble': [r'\usepackage{cmbright}',
                                          r'\usepackage{amsmath}']}
    mpl.rcParams.update(fontparams)

    f = plt.figure()
    f.set_size_inches(3.8, 3.8)
   
    # create grid
    gs = plt.GridSpec(4, 4)
    
    ax1 = f.add_subplot(gs[:-1, 1:])
    marginX = f.add_subplot(gs[-1, 1:])
    marginY = f.add_subplot(gs[:-1, 0])

    # position axis elements explicitly
    xStartCenter = 0.35
    yStartCenter = 0.34
    
    yStartMarginX = 0.11
    xStartMarginY = 0.12
    
    centerWidthFrac = 0.57
    centerHeightFrac = centerWidthFrac
    subHeight = 0.22
    
    ax1.set_position([xStartCenter, yStartCenter, centerWidthFrac, centerHeightFrac])
    marginX.set_position([xStartCenter, yStartMarginX, centerWidthFrac, subHeight])
    marginY.set_position([xStartMarginY, yStartCenter, subHeight, centerHeightFrac])
    
    marginX.yaxis.tick_right()
    marginY.xaxis.tick_top()
    
    ax1.axes.tick_params(which = 'both',
                         direction = 'in')
    
    axes = [ax1, marginX, marginY]
    
    ######################################################################################
    # labeling
    plt.title(titlestr)
    marginX.set_xlabel(r'$x_1$', fontsize = 9.0)
    marginY.set_ylabel(r'$x_2$', fontsize = 9.0, rotation = 0.0)

    marginY.yaxis.labelpad = 7.5
    ######################################################################################
    # plotting
    
    lineWidth = 1.0
    
    ax1.scatter(X[:, 0], X[:, 1],
                s = 12.0,
                marker = '.',
                lw = lineWidth,
                facecolor = pColors[0],
                edgecolor = 'None',
                zorder = 11,
                alpha = 0.18)
    
    marginX.hist(X[:, 0], histtype = 'stepfilled',
                 orientation = 'vertical',
                 color = pColors[1],
                 range = (55, 125.0),
                 bins = 45,
                 density = True,
                 label = r'sampling')
    
    marginX.plot(marginalX[:, 0], marginalX[:, 1],
                 lw = 1.25,
                 color = pColors[0],
                 label = r'reference')

    marginX.invert_yaxis() 

    marginY.hist(X[:, 1], histtype = 'stepfilled',
                 orientation = 'horizontal',
                 color = pColors[1],
                 bins = 45,
                 range = (75.0, 175.0),
                 density = True,
                 label = r'sampling')     

    marginY.plot(marginalY[:, 1], marginalY[:, 0],
                 lw = 1.25,
                 color = pColors[0],
                 label = r'reference')

    marginY.invert_xaxis()

    ######################################################################################
    # annotations

    label = r'$p(x_1\, |\, \mu_1, \sigma_1)$'
    marginX.annotate(label,
                  xy = (0.64, 0.1),
                  xycoords = 'axes fraction',
                  fontsize = 10.0,
                  horizontalalignment = 'left',
                  zorder = 20,
                  clip_on = False)

    label = r'$p(x_2\, |\, \mu_2, \sigma_2)$'
    marginY.annotate(label,
                  xy = (0.075, 0.04),
                  xycoords = 'axes fraction',
                  fontsize = 10.0,
                  horizontalalignment = 'left',
                  zorder = 20,
                  clip_on = False)

    ax1.annotate(r'$\mu_1 = {}, \sigma_1 = {}$'.format(mu1, sigma1),
                 xy = (-0.465, -0.07),
                 xycoords = 'axes fraction',
                 fontsize = 7.0,
                 horizontalalignment = 'left',
                 zorder = 20,
                 clip_on = False)

    ax1.annotate(r'$\mu_2 = {}, \sigma_2 = {}$'.format(mu2, sigma2),
                 xy = (-0.465, -0.14),
                 xycoords = 'axes fraction',
                 fontsize = 7.0,
                 horizontalalignment = 'left',
                 zorder = 20,
                 clip_on = False)
     
    ax1.annotate(params[0],
                 xy = (-0.465, -0.21),
                 xycoords = 'axes fraction',
                 fontsize = 7.0,
                 horizontalalignment = 'left',
                 zorder = 20,
                 clip_on = False)
     
    ax1.annotate(r'# samples $= 2\cdot 10^{4}$',
                 xy = (-0.465, -0.28),
                 xycoords = 'axes fraction',
                 fontsize = 7.0,
                 horizontalalignment = 'left',
                 zorder = 20,
                 clip_on = False)

    ######################################################################################
    # legend
    if drawLegend:
        leg = marginX.legend(# bbox_to_anchor = [0.7, 0.8],
                             loc = 'lower left',
                             handlelength = 1.75,
                             scatterpoints = 1,
                             markerscale = 1.0,
                             ncol = 1)
        leg.draw_frame(False)

        # set the linewidth of the legend object
        for legobj in leg.legendHandles:
            legobj.set_linewidth(2.25)

        leg2 = marginY.legend(# bbox_to_anchor = [0.7, 0.8],
                              # loc = 'upper left',
                              handlelength = 1.75,
                              scatterpoints = 1,
                              markerscale = 1.0,
                              ncol = 1)
        leg2.draw_frame(False)

        for legobj in leg2.legendHandles:
            legobj.set_linewidth(2.25)

    ######################################################################################
    # set plot range and ticks

    major_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[4])
    minor_x_ticks = np.arange(xFormat[2], xFormat[3], xFormat[5])
    
    major_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[4])
    minor_y_ticks = np.arange(yFormat[2], yFormat[3], yFormat[5])
    
    mX_major_y_ticks = np.arange(0.0, 0.06, 0.02)
    mX_minor_y_ticks = np.arange(0.0, 0.05, 0.01)
    
    mY_major_x_ticks = np.arange(0.0, 0.05, 0.02)
    mY_minor_x_ticks = np.arange(0.0, 0.05, 0.01)
    
    # set ax1
    ax1.set_xticks(major_x_ticks)
    ax1.set_xticks(minor_x_ticks, minor = True)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.set_xlim(xFormat[0], xFormat[1])
    ax1.set_ylim(yFormat[0], yFormat[1])
    
    # set marginX
    marginX.set_xticks(major_x_ticks)
    marginX.set_xticks(minor_x_ticks, minor = True)
    marginX.set_yticks(mX_major_y_ticks)
    marginX.set_yticks(mX_minor_y_ticks, minor = True)
    marginX.set_xlim(xFormat[0], xFormat[1])
    marginX.set_ylim(0.0522, 0.0)
    
    # set marginY
    marginY.set_yticks(major_y_ticks)
    marginY.set_yticks(minor_y_ticks, minor = True)
    marginY.set_xticks(mY_major_x_ticks)
    marginY.set_xticks(mY_minor_x_ticks, minor = True)
    marginY.set_xlim(0.042, 0.0)
    marginY.set_ylim(yFormat[0], yFormat[1])
        
    # tick label formatting
    majorFormatter = FuncFormatter(cleanFormatter)
    marginX.xaxis.set_major_formatter(majorFormatter)
    marginX.yaxis.set_major_formatter(majorFormatter)
    marginY.xaxis.set_major_formatter(majorFormatter)
    marginY.yaxis.set_major_formatter(majorFormatter)
    
    labelfontsize = 7.0
    
    for ax in axes:
        
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(labelfontsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(labelfontsize)
            
        ax.tick_params('both', length = 2.5, width = 0.5, which = 'major', pad = 2.0)
        ax.tick_params('both', length = 1.5, width = 0.35, which = 'minor', pad = 2.0)
        
        ax.tick_params(axis = 'x', which = 'major', pad = 1.0)
        ax.tick_params(axis = 'y', which = 'major', pad = 1.0, zorder = 10)
    
    for ax in axes:
        
        ax.set_axisbelow(False)
        
        for spine in ax.spines.values(): # ax.spines is a dictionary
        
            spine.set_zorder(10)

    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + today
    if savePDF:
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

    # set loc and scale parameters
    mu1, sigma1 = 87.25, 8.124
    mu2, sigma2 = 125.75, 11.25

    X = np.genfromtxt(os.path.join(RAWDIR, 'GaussianSamples_uncorrelated_seed_987654321.txt'))
    sample1, sample2 = X[:, 0], X[:, 1]

    ######################################################################################
    # inspect random samples
    print("sample1.shape =", sample1.shape)
    print("sample2.shape =", sample2.shape)

    print("np.min(sample1) =", np.min(sample1))
    print("np.max(sample1) =", np.max(sample1))
    print("np.min(sample2) =", np.min(sample2))
    print("np.max(sample2) =", np.max(sample2))
    ######################################################################################

    # check correlation by computing the Pearson correlation coefficient
    rhoPearson = scipy.stats.pearsonr(sample1, sample2)    
    print("rho(Pearson) =", rhoPearson)

    rhoString = r'$\rho = {}$'.format(np.round(rhoPearson[0], 4))

    ######################################################################################
    # create analytical poisson distributions
    xVals1 = np.linspace(0.0, 135.0, 700)
    yVals1 = norm.pdf(xVals1, loc = mu1, scale = sigma1)
    gaussianDist1 = np.zeros((len(xVals1), 2))
    gaussianDist1[:, 0] = xVals1
    gaussianDist1[:, 1] = yVals1

    xVals2 = np.linspace(0.0, 175.0, 700)
    yVals2 = norm.pdf(xVals2, loc = mu2, scale = sigma2)
    gaussianDist2 = np.zeros((len(xVals2), 2))
    gaussianDist2[:, 0] = xVals2
    gaussianDist2[:, 1] = yVals2

    ######################################################################################
    # plotting

    ####################################################################
    # xFormat and yFormat are 6-tuples each for x- and y-format passing.
    # The syntax is as follows:
    # xFormat = (xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor)
    # yFormat = (ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor)
    xFormat = (48.0, 123.0, 40.0, 1.02 * 123.0, 20.0, 5.0)
    yFormat = (78.0, 177.0, 60.0, 1.02 * 177.0, 20.0, 5.0)
    ####################################################################

    pColors = ['C0', '#999999']

    outname = 'uncorrelated_gaussian_RVs_with_marginal_distributions'

    outname = Plot(titlestr = '',
                   X = X,
                   marginalX = gaussianDist1,
                   marginalY = gaussianDist2,
                   params = [rhoString],
                   outname = outname,
                   outdir = OUTDIR,
                   pColors = pColors,
                   drawLegend = True,
                   xFormat = xFormat,
                   yFormat = yFormat)

    cmd = 'pdf2svg ' + os.path.join(OUTDIR, outname + '.pdf') + \
          ' ' + os.path.join(OUTDIR, outname + '.svg')
    print(cmd)
    os.system(cmd)
