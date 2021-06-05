#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-06-05
# file: mpl_multiple_legends_minimal_mk3.py
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

def cleanFormatter(x, pos = None):
    '''
    will format 0.0 as 0 and
    will format 1.0 as 1
    '''
    return '{:g}'.format(x)

if __name__ == '__main__':

    outname = 'mpl_multiple_legends_minimal_mk3'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    # create synthetic data
    n_vispoints = 500
    xVals = np.linspace(0.0, 1.0, n_vispoints)

    yVals1 = [1.0 * x for x in xVals]
    yVals2 = [1.5 * x for x in xVals]
    yVals3 = [2.0 * x for x in xVals]

    X = np.zeros((n_vispoints, 4))
    X[:, 0] = xVals
    X[:, 1] = yVals1
    X[:, 2] = yVals2
    X[:, 3] = yVals3

    # minimal plot
    f, ax1 = plt.subplots(1)
    f.set_size_inches(3.0, 3.0)
    plt.subplots_adjust(left = 0.2, right = 0.95,
                        bottom = 0.15, top = 0.95)

    # labels as a list of lists
    labels = [[r'line 1'],
              [r'line 2'],
              [r'line 3']]

    pColors = ['C0', 'C1', 'C2']

    # legend locations as a list of lists
    locs = [[0.0, 1.0],
            [0.0, 0.5],
            [0.6, 0.25]]

    for i in range(len(labels)):

        p, = ax1.plot(X[:, 0], X[:, i + 1],
                      alpha = 1.0,
                      color = pColors[i],
                      zorder = 1)

        p = [p]

        pLeg = plt.legend(p, labels[i],
                          bbox_to_anchor = locs[i],
                          loc = 'upper left',
                          handlelength = 2.0,
                          fontsize = 10.0)
        pLeg.draw_frame(False)
        plt.gca().add_artist(pLeg)

    # tick label formatting
    from matplotlib.ticker import FormatStrFormatter
    majorFormatter = FormatStrFormatter('%g')
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax1.yaxis.set_major_formatter(majorFormatter)

    # labeling
    ax1.set_xlabel(r'$x$ label')
    ax1.set_ylabel(r'$y$ label')
    ax1.xaxis.labelpad = 3.5
    ax1.yaxis.labelpad = 5.5

    outname += '_' + today
    f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
              dpi = 300,
              transparent = True)
    # plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
