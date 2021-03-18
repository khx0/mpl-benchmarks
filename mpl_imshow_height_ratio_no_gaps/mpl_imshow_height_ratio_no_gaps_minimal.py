#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# adapted by: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-03-18
# file: mpl_multiple_imshows_without_gaps_demo.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.4
##########################################################################################

'''
Minimal demonstrator version using imshow with height_ratios.
This snippet was inspired by this Stackoverflow thread:
https://stackoverflow.com/questions/42675864/how-to-remove-gaps-between-images-in-matplotlib
last seen online on 2021-03-13
'''

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    # reproducibility
    np.random.seed(123456789)

    outname = 'mpl_imshow_height_ratio_no_gaps_minimal'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    n_rows = 3
    n_cols = 2

    data = [[np.random.rand(10, 10), np.random.rand(10, 10)],
            [np.random.rand(5, 10), np.random.rand(5, 10)],
            [np.random.rand(2, 10), np.random.rand(2, 10)]]

    cmaps = [['viridis', 'binary'],
             ['plasma', 'coolwarm'],
             ['Greens', 'copper']]

    '''
    Aussming an equal pixel size, we use the heights and widths of all
    the image matrices to set the figure size and use the height_ratios
    keyword, which can be passed to the pyplot.subplots constructor.
    '''

    heights = [a[0].shape[0] for a in data]
    widths = [a.shape[1] for a in data[0]]

    fig_width = 6.0 # in inches
    fig_height = fig_width * sum(heights) / sum(widths)

    dpi = 100

    f, axarr = plt.subplots(nrows = n_rows, ncols = n_cols,
        figsize = (fig_width, fig_height),
        gridspec_kw = {'height_ratios': heights},
        dpi = dpi
    )

    for i in range(n_rows):
        for j in range(n_cols):
            axarr[i, j].imshow(data[i][j], cmap = cmaps[i][j])
            axarr[i, j].axis('off')

    plt.subplots_adjust(
        wspace = 0.0, hspace = 0.0,
        left = 0.0, right = 1.0,
        bottom = 0.0, top = 1.0
    )

    # save plot to file
    f.savefig(os.path.join(OUTDIR, outname) + '.png',
              transparent = True)
    plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
