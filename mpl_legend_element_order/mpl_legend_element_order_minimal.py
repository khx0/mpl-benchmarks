#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-04-09
# file: mpl_legend_element_order_minimal.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.2  in conjunction with mpl version 3.0.3
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend

now = datetime.datetime.now()
now = "{}-{}-{}".format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    outname = 'mpl_legend_element_order_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__ + '_' + now

    # create synthetic data
    nVisPoints = 500
    xVals = np.linspace(-0.25, 1.25, nVisPoints)
    yVals = np.sin(2.0 * np.pi * xVals)
    X = np.zeros((nVisPoints, 2))
    X[:, 0] = xVals
    X[:, 1] = yVals

    # fix random number seed for reproducibility
    np.random.seed(123456789)
    mu = 0.0
    sigma = 0.3
    nDatapoints = 30
    data = np.zeros((nDatapoints, 2))
    data[:, 0] = np.linspace(0.0, 1.0, nDatapoints)
    data[:, 1] = np.sin(2.0 * np.pi * data[:, 0]) + np.random.normal(mu, sigma, nDatapoints)

    # minimal plot
    f, ax1 = plt.subplots(1)

    ax1.set_xlabel(r'$x$ label')
    ax1.set_ylabel(r'$y$ label')

    p1, = ax1.plot(X[:, 0], X[:, 1],
              color = 'k',
              alpha = 1.0,
              zorder = 2,
              label = r"p1 handle's label")

    p2 = ax1.scatter(data[:, 0], data[:, 1],
                facecolor = 'None',
                edgecolor = 'k',
                zorder = 3,
                label = r"p2 handle's label")

    error = 0.5
    p3 = ax1.fill_between(X[:, 0], X[:, 1] - error, X[:, 1] + error,
                          color = 'k',
                          alpha = 0.15,
                          lw = 0.0,
                          zorder = 2,
                          label = r"p3 handle's label")

    print("Plot handle data types:")
    print("type(p1) =", type(p1))
    print("type(p2) =", type(p2))
    print("type(p3) =", type(p3))
    '''
    The order of the plot handles in the pHandles list determines their
    oder in the figure's legend.
    '''

    pHandles = [p3, p2, p1]
    pLabels = [handle.get_label() for handle in pHandles]

    leg = ax1.legend(pHandles,
                     pLabels,
                     # bbox_to_anchor = [0.07, 0.02],
                     loc = 'upper right',
                     handlelength = 1.5,
                     scatterpoints = 1,
                     markerscale = 1.0,
                     ncol = 1)
    leg.draw_frame(False)
    plt.gca().add_artist(leg)

    # set plot range and scale
    ax1.set_xlim(-0.05, 1.05)

    # save plot to file
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
