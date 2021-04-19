#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-04-19
# file: call_AB_panel.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.1
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl

from mpl_imshow_AB_panel import plot_AB_panel

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    # create plot data
    # fix prng seed for reproducibility
    np.random.seed(123456789)
    matrix_size = 128
    data = [np.random.rand(matrix_size, matrix_size), 
            np.random.rand(matrix_size, matrix_size)]

    wspace_values = [0.0, 0.015, 0.025, 0.05]

    for i, wspace in enumerate(wspace_values):
        print(i, wspace)
        # call plot function
        outname = f'mpl_imshow_AB_panel_{i:02d}_wspace_{wspace:0.2}'
        outname += '_Python_' + platform.python_version() + \
                '_mpl_' + mpl.__version__

        image_size_label = f'image matrix {matrix_size}' + r'$\times$' + f'{matrix_size}'

        anno_dict = {
            'A_top_left': 'varying wspace between the A and B image',
            'A_bottom_left': image_size_label,
            'B_top_left': f'wspace {wspace:0.2}',
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
            wspace = wspace,
            anno_dict = anno_dict,
            dpi = 300,
        )
 