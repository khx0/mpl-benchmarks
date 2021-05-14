#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# adapted by: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-05-14
# file: mpl_imshow_ABC_panel_no_gaps.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
##########################################################################################

'''
Minimal demonstrator version for an ABC panel using imshow with height_ratios and no gaps
between the different images.
This snippet was inspired by this Stackoverflow thread:
https://stackoverflow.com/questions/42675864/how-to-remove-gaps-between-images-in-matplotlib
last seen online on 2021-03-14
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

    outname = 'mpl_imshow_ABC_panel_no_gaps'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    dpi = 100

    n_rows = 1
    n_cols = 3

    matrix_size = 512

    data = [np.random.rand(matrix_size, matrix_size), 
            np.random.rand(matrix_size, matrix_size),
            np.random.rand(matrix_size, matrix_size)]

    cmaps = ['viridis', 'gray', 'plasma']

    '''
    Aussming an equal pixel size, we use the heights and widths of all
    the image matrices to set the figure size and use the height_ratios
    keyword, which can be passed to the pyplot.subplots constructor.
    '''

    heights = [matrix_size]
    widths = [matrix_size, matrix_size, matrix_size]

    fig_width = 6.0 # in inches
    fig_height = fig_width * sum(heights) / sum(widths)

    print("widths: ", widths)
    print("heights: ", heights)
    print("fig_width: ", fig_width)
    print("fig_height: ", fig_height)

    f, axs = plt.subplots(nrows = n_rows, ncols = n_cols,
        figsize = (fig_width, fig_height),
        gridspec_kw = {'height_ratios': heights},
        dpi = dpi
    )

    for j in range(n_cols):
        axs[j].imshow(data[j], cmap = cmaps[j])
        axs[j].axis('off')

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
