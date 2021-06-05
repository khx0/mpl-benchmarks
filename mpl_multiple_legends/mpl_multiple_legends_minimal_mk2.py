#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-06-05
# file: mpl_multiple_legends_minimal_mk2.py
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

    outname = 'mpl_multiple_legends_minimal_mk2'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

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

    p1, = ax1.plot(X[:, 0], X[:, 1],
                   alpha = 1.0,
                   color = 'C0',
                   zorder = 1)
    p1 = [p1]

    p2, = ax1.plot(X[:, 0], X[:, 2],
                   alpha = 1.0,
                   color = 'C1',
                   zorder = 1)
    p2 = [p2]

    p3, = ax1.plot(X[:, 0], X[:, 3],
                   alpha = 1.0,
                   color = 'C2',
                   zorder = 1)
    p3 = [p3]

    label1 = [r'line 1']
    label2 = [r'line 2']
    label3 = [r'line 3']

    leg1 = plt.legend(p1, label1,
                      loc = 'upper left',
                      handlelength = 2.0,
                      fontsize = 10.0)
    leg1.draw_frame(False)
    plt.gca().add_artist(leg1)

    leg2 = plt.legend(p2, label2,
                      loc = 'lower right',
                      handlelength = 2.0,
                      fontsize = 10.0)
    leg2.draw_frame(False)
    plt.gca().add_artist(leg2)

    leg3 = plt.legend(p3, label3,
                      bbox_to_anchor = [0.0, 0.5],
                      loc = 'upper left',
                      handlelength = 2.0,
                      fontsize = 10.0)
    leg3.draw_frame(False)
    plt.gca().add_artist(leg3)

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
