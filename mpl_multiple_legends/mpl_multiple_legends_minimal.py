#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-06-05
# file: mpl_multiple_legends_minimal.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
##########################################################################################

import os
import datetime
import platform
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    outname = 'mpl_multiple_legends_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    # create synthetic data
    n_vispoints = 500
    n_scatterpoints = 20
    xVals = np.linspace(0.0, 1.0, n_vispoints)
    xValsScatter = np.linspace(0.0, 1.0, n_scatterpoints)

    yVals = [x * (1.0 - x) for x in xVals]
    yValsScatter = [x * (1.0 - x) for x in xValsScatter]

    X = np.zeros((n_vispoints, 2))
    Xs = np.zeros((n_scatterpoints, 2))
    X[:, 0], X[:, 1] = xVals, yVals
    Xs[:, 0], Xs[:, 1] = xValsScatter, yValsScatter

    # minimal plot
    f, ax1 = plt.subplots(1)

    ######################################################################################
    # plot using the mpl default legend
    ax1.scatter(Xs[:, 0], Xs[:, 1],
                marker = 'o',
                s = 50,
                facecolors = 'None',
                alpha = 1.0,
                linewidth = 1.0,
                edgecolors = 'k',
                zorder = 2,
                label = r'scatter 1')

    # legend
    leg = ax1.legend(loc = 'upper right',
                     handlelength = 0.1,
                     scatterpoints = 1,
                     fontsize = 9.0,
                     ncol = 1)
    leg.draw_frame(False)
    plt.gca().add_artist(leg)
    ######################################################################################

    ######################################################################################
    # plot with additional 2nd custom legend
    pHandles = []

    p, = ax1.plot(X[:, 0], X[:, 1],
                  alpha = 1.0,
                  color = 'k',
                  zorder = 1)

    pHandles.append(p)

    labels = [r'line 1']

    legLeft = plt.legend(pHandles, labels,
                         loc = 'upper left',
                         handlelength = 3.0,
                         fontsize = 10.0)
    legLeft.draw_frame(False)
    plt.gca().add_artist(legLeft)
    ######################################################################################
    # labeling
    ax1.set_xlabel(r'$x$ label')
    ax1.set_ylabel(r'$y$ label')
    ax1.xaxis.labelpad = 3.5
    ax1.yaxis.labelpad = 5.5

    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
