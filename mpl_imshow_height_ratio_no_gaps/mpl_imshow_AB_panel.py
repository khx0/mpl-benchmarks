#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-03-22
# file: mpl_imshow_AB_panel.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.4
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

# TODO add dimensions in cm
# TODO support non square matrix sizes
# TODO think about different A B matrix sizes, and how to handle things then

def plot_AB_panel(data, cmaps, outname, outdir,
    fig_width_img = 4.0, top_height_frac = 0.0, bottom_height_frac = 0.0, 
    left_width_frac = 0.0, right_width_frac = 0.0, wspace = 0.0,
    anno_dict = None, dpi = 100, savePNG = True, savePDF = False, datestamp = True):
    '''
    param list data: list containing the two image matrices to be plotted. 
        Assuming to be broadcasted into shape (2, matrix_height, matrix_width), where both the first and the second image matrix have
        shape (matrix_height, matrix_width).
    '''

    # The current AB panel plot function assumes a horizontal AB panel layout.
    n_rows = 1
    n_cols = 2

    data = np.array(data)
    matrix_height = data.shape[-2]
    matrix_width = data.shape[-1]
    # determine heights and widths to derive the image matrix aspect ratio
    heights = [matrix_height]
    widths = [matrix_width, matrix_width]

    ################################################################################################
    # figure size and margin control
    # Step 1 - Set desired figure width by user (in inches).
    # Here we use the width as a starting point from which all other measures are derived.
    # This could equally be done using the height as pivotal starting point.
    # This considerations are based on the aspect preserving ratio
    # fig_width_img / fig_height_img = cumulated_image_width / cumulated_image_height,
    # which in code reads
    # fig_width_img / fig_height_img = sum(widths) / sum(heights).
    # fig_width_img is set by the used via the function signature.

    # Step 2 - Set margin / padding fractions (here as fraction of the image width)
    # All fractions are set by the user via the function signature.
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

    # Step 4 -  Derive the true image figure height

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
    # end of figure size and margin control
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
    if anno_dict:

        if 'A_top_left' in anno_dict.keys():
            axs[0].annotate(
                anno_dict['A_top_left'],
                xy = (0.0, 1.03),
                xycoords = 'axes fraction',
                horizontalalignment = 'left',
                verticalalignment = 'center',
                fontsize = 6.0,
                zorder = 5
            )

        if 'A_top_center' in anno_dict.keys():
            axs[0].annotate(
                anno_dict['A_top_center'],
                xy = (0.5, 1.03),
                xycoords = 'axes fraction',
                horizontalalignment = 'center',
                verticalalignment = 'center',
                fontsize = 6.0,
                zorder = 5
            )

        if 'A_top_right' in anno_dict.keys():
            axs[0].annotate(
                anno_dict['A_top_right'],
                xy = (1.0, 1.03),
                xycoords = 'axes fraction',
                horizontalalignment = 'right',
                verticalalignment = 'center',
                fontsize = 6.0,
                zorder = 5)

        if 'A_bottom_left' in anno_dict.keys():
            axs[0].annotate(
                anno_dict['A_bottom_left'],
                xy = (0.0, -0.03),
                xycoords = 'axes fraction',
                horizontalalignment = 'left',
                verticalalignment = 'center',
                fontsize = 6.0,
                zorder = 5
            )

        if 'B_top_left' in anno_dict.keys():
            axs[1].annotate(
                anno_dict['B_top_left'],
                xy = (0.0, 1.03),
                xycoords = 'axes fraction',
                horizontalalignment = 'left',
                verticalalignment = 'center',
                fontsize = 6.0,
                zorder = 5
            )

        if 'B_top_center' in anno_dict.keys():
            axs[1].annotate(
                anno_dict['B_top_center'],
                xy = (0.5, 1.03),
                xycoords = 'axes fraction',
                horizontalalignment = 'center',
                verticalalignment = 'center',
                fontsize = 6.0,
                zorder = 5
            )

        if 'B_top_right' in anno_dict.keys():
            axs[1].annotate(
                anno_dict['B_top_right'],
                xy = (1.0, 1.03),
                xycoords = 'axes fraction',
                horizontalalignment = 'right',
                verticalalignment = 'center',
                fontsize = 6.0,
                zorder = 5
            )

        if 'B_bottom_left' in anno_dict.keys():
            axs[1].annotate(
                anno_dict['B_bottom_left'],
                xy = (0.0, -0.03),
                xycoords = 'axes fraction',
                horizontalalignment = 'left',
                verticalalignment = 'center',
                fontsize = 6.0,
                zorder = 5
            )

    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + today
    if savePDF: # save to file using pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = dpi, transparent = True)
    if savePNG:
        print("creating png figure with width, height:", fig_width, fig_height)
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = dpi, transparent = True)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return None

if __name__ == '__main__':

    # create plot data
    # fix prng seed for reproducibility
    np.random.seed(123456789)
    matrix_size = 128
    data = [np.random.rand(matrix_size, matrix_size), 
            np.random.rand(matrix_size, matrix_size)]

    # call plot function
    outname = 'mpl_imshow_AB_panel'
    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    image_size_label = f'image matrix {matrix_size}' + r'$\times$' + f'{matrix_size}'

    anno_dict = {
        'A_top_left': 'top left label',
        'A_top_center': 'top center label',
        'A_top_right': 'top right label',
        'A_bottom_left': image_size_label,
        'B_top_left': 'top left label',
        'B_top_center': 'top center label',
        'B_top_right': 'top right label',
        'B_bottom_left': image_size_label,
    }

    plot_AB_panel(
        data = data,
        cmaps = ['gray', 'viridis'],
        outname = outname,
        outdir = OUTDIR,
        fig_width_img = 4.0,
        top_height_frac = 0.1,
        bottom_height_frac = 0.1,
        left_width_frac = 0.02,
        right_width_frac = 0.02,
        wspace = 0.015,
        anno_dict = anno_dict,
        dpi = 300,
    )
