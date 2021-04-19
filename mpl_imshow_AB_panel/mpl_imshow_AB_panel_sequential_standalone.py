#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-04-19
# file: mpl_imshow_AB_panel_sequential_standalone.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.1
#
# This sequential script is intended to be a standalone python script which presents
# the code in a plain top to bottom (sequential) manner.
# Hence, this script is not trying to hide anything away or factorize parts which 
# might not be necessary for all use cases, but therewith allows maximal tunability
# with direct access to all plot parameters in a very explicit way.
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

    outname = 'mpl_imshow_AB_panel_sequential_standalone'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    outname += '_' + today

    dpi = 300

    n_rows = 1
    n_cols = 2

    matrix_size = 128

    data = [np.random.rand(matrix_size, matrix_size), 
            np.random.rand(matrix_size, matrix_size)]

    cmaps = ['gray', 'viridis']

    heights = [matrix_size]
    widths = [matrix_size, matrix_size]

    ################################################################################################
    # figure size and margin control
    # Step 1 - Set desired figure width by user (in inches).
    # Here we use the width as a starting point from which all other measures are derived.
    # This could equally be done using the height as pivotal starting point.
    # These considerations are based on the aspect preserving ratio
    # fig_width_img / fig_height_img = cumulated_image_width / cumulated_image_height,
    # which in code reads
    # fig_width_img / fig_height_img = sum(widths) / sum(heights).

    fig_width_img = 4.0

    # Step 2 - Set margin / padding fractions (here as fraction of the true image width)
    top_height_frac = 0.1    # fraction
    bottom_height_frac = 0.1 # fraction
    left_width_frac = 0.02   # fraction
    right_width_frac = 0.02  # fraction

    wspace = 0.015 # fraction of the average axes width
    #####################################################################################
    # wspace float, optional
    # The width of the padding between subplots, as a fraction of the average axes width.
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
    #####################################################################################

    # Step 3 - Derive true image figure width
    left_margin = left_width_frac * fig_width_img       # in inches
    right_margin = right_width_frac * fig_width_img     # in inches
    middle_margin = wspace * fig_width_img              # in inches

    fig_width = np.round(fig_width_img + left_margin + middle_margin + right_margin, 2)

    # Step 4 -  Dreive true image figure height

    # fig_height_img is here determined by the image matrix aspect ratio
    fig_height_img = fig_width_img * sum(heights) / sum(widths)
    top_margin = top_height_frac * fig_height_img       # in inches
    bottom_margin = bottom_height_frac * fig_height_img # in inches

    fig_height = np.round(fig_height_img + top_margin + bottom_margin, 2)

    # Step 5 - Compute final figure margins from the specified dimensions.
    bottom_frac = top_margin / fig_height
    top_frac = 1.0 - bottom_margin / fig_height
    left_frac = left_margin / fig_width
    right_frac = 1.0 - right_margin / fig_width
    ################################################################################################

    f, axs = plt.subplots(nrows = n_rows, ncols = n_cols,
        figsize = (fig_width, fig_height),
        gridspec_kw = {'height_ratios': heights},
        dpi = dpi
    )

    for j in range(n_cols):

        axs[j].imshow(data[j], cmap = cmaps[j],
            interpolation = None)
        # for png export use interpolation = None

        axs[j].axis('off')

    plt.subplots_adjust(
        wspace = wspace, hspace = 0.0,
        left = left_frac, right = right_frac,
        bottom = bottom_frac, top = top_frac
    )

    # annotations
    axs[0].annotate('top left label',
        xy = (0.0, 1.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'left',
        verticalalignment = 'center',
        fontsize = 6.0,
        zorder = 5)

    axs[0].annotate('top center label',
        xy = (0.5, 1.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'center',
        verticalalignment = 'center',
        fontsize = 6.0,
        zorder = 5)

    axs[0].annotate('top right label',
        xy = (1.0, 1.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'right',
        verticalalignment = 'center',
        fontsize = 6.0,
        zorder = 5)

    axs[1].annotate('top left label',
        xy = (0.0, 1.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'left',
        verticalalignment = 'center',
        fontsize = 6.0,
        zorder = 5)

    axs[1].annotate('top center label',
        xy = (0.5, 1.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'center',
        verticalalignment = 'center',
        fontsize = 6.0,
        zorder = 5)

    axs[1].annotate('top right label',
        xy = (1.0, 1.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'right',
        verticalalignment = 'center',
        fontsize = 6.0,
        zorder = 5)

    image_size_label = f'image matrix {matrix_size}' + r'$\times$' + f'{matrix_size}'

    axs[0].annotate(image_size_label,
        xy = (0.0, -0.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'left',
        verticalalignment = 'center',
        fontsize = 6.0,
        zorder = 5)

    axs[1].annotate(image_size_label,
        xy = (0.0, -0.03),
        xycoords = 'axes fraction',
        horizontalalignment = 'left',
        verticalalignment = 'center',
        fontsize = 6.0,
        zorder = 5)

    print("creating png figure with width, height: ",  fig_width, fig_height)
    # save plot to file
    f.savefig(os.path.join(OUTDIR, outname) + '.png',
              transparent = True)

    ####################################################
    # uncomment to save as pdf
    # f.savefig(os.path.join(OUTDIR, outname) + '.pdf',
    #           transparent = True)
    ####################################################

    #####################################
    # uncomment to get interactive prompt
    # plt.show()
    #####################################

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
