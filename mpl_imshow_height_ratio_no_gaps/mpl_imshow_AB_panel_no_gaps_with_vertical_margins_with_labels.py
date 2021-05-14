#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-05-14
# file: mpl_imshow_AB_panel_no_gaps_with_vertical_margins_with_labels.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
##########################################################################################

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

    outname = 'mpl_imshow_AB_panel_no_gaps_with_vertical_margins_with_labels'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    dpi = 150

    n_rows = 1
    n_cols = 2

    matrix_size = 512

    data = [np.random.rand(matrix_size, matrix_size), 
            np.random.rand(matrix_size, matrix_size)]

    cmaps = ['viridis', 'gray']

    heights = [matrix_size]
    widths = [matrix_size, matrix_size]

    ################################################################################################
    # figure size and margin control
    # Step 1 - Set desired figure width by user (in inches).
    # Here we use the width as a starting point from which all other measures are derived.
    # This could equally be done using the height as pivotal starting point.
    # And is based on the aspect preserving ratio
    # fig_width_img / fig_height_img = cumulated_image_width / cumulated_image_height,
    # which in code reads
    # fig_width_img / fig_height_img = sum(widths) / sum(heights).

    fig_width = 6.0

    # Step 2 - Derive image figure width (assuming no white space margin)
    # from image content size ratios.
    fig_height_img = fig_width * sum(heights) / sum(widths)

    # Step 3 - Set top margin in percent of the already set figure height.
    top_height_frac = 0.1    # fraction
    bottom_height_frac = 0.1 # fraction
    top_margin = top_height_frac * fig_height_img       # in inches
    bottom_margin = bottom_height_frac * fig_height_img # in inches
    fig_height = np.round(fig_height_img + top_margin + bottom_margin, 2)

    # Step 4 - Compute figure margins from set lenghts.
    bottom_frac = top_margin / fig_height
    top_frac = 1.0 - bottom_margin / fig_height
    ################################################################################################

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
        bottom = bottom_frac, top = top_frac
    )

    axs[0].annotate('A top left label ',
        xy = (0.0, 1.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'left',
        verticalalignment = 'center',
        zorder = 5)

    axs[1].annotate('B top left label ',
        xy = (0.0, 1.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'left',
        verticalalignment = 'center',
        zorder = 5)

    image_size_label = f'image matrix {matrix_size}' + r'$\times$' + f'{matrix_size}'

    axs[0].annotate(image_size_label,
        xy = (0.0, -0.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'left',
        verticalalignment = 'center',
        fontsize = 8.0,
        zorder = 5)

    axs[1].annotate(image_size_label,
        xy = (0.0, -0.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'left',
        verticalalignment = 'center',
        fontsize = 8.0,
        zorder = 5)

    # save plot to file
    f.savefig(os.path.join(OUTDIR, outname) + '.png',
              transparent = True)
    plt.show()

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
