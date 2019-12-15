#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-12-15
# file: create_test_03_svg_files.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.2
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm

from mpl_pcolormesh_with_fixed_size_and_relative_border_margins \
    import plot_pcolor

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def test_03_with_svg_output(cMaps = [cm.viridis]):

    for n in np.arange(1, 10 + 1, 1): # (from, to (excluding), increment)

        nPxs_x = n
        nPxs_y = n
        pixelWidth = 1.0
        pixelHeight = 1.0

        xmin, xmax = 0.0, pixelWidth  * (nPxs_x - 1)
        ymin, ymax = 0.0, pixelHeight * (nPxs_y - 1)

        xVals = np.linspace(xmin, xmax, nPxs_x)
        yVals = np.linspace(ymin, ymax, nPxs_y)

        width_X = nPxs_x * pixelWidth
        height_Y = nPxs_y * pixelHeight

        # fill matrix
        zVals = np.zeros((nPxs_x, nPxs_y))

        for j in range(nPxs_y):     # iterate over y values
            for i in range(nPxs_x): # iterate over x values
                zVals[i, j] = 0.2 * xVals[i]

        assert xVals.shape == yVals.shape, "Error: Shape assertion failed."
        assert zVals.shape == (nPxs_x, nPxs_y), "Error: Shape assertion failed."

        zmin = np.min(zVals)
        zmax = np.max(zVals)

        # plot settings

        fProps = (4.0, 4.0, 0.16, 0.80, 0.16, 0.88)
        relativePaddingFrac = 0.015 # relative padding fraction

        xlim_left  = xmin - pixelWidth  / 2.0 - relativePaddingFrac * width_X
        xlim_right = xmax + pixelWidth  / 2.0 + relativePaddingFrac * width_X
        ylim_left  = ymin - pixelHeight / 2.0 - relativePaddingFrac * height_Y
        ylim_right = ymax + pixelHeight / 2.0 + relativePaddingFrac * height_Y

        if n == 1: # pathological handling of n == 1 case
            xFormat = ('linear', xlim_left, xlim_right, 0.0, 1.02 * xmax + 0.01, 1.0, 1.0, r'x axis label')
            yFormat = ('linear', ylim_left, ylim_right, 0.0, 1.02 * ymax + 0.01, 1.0, 1.0, r'y axis label')
        else:
            xFormat = ('linear', xlim_left, xlim_right, 0.0, 1.02 * xmax, 1.0, 1.0, r'x axis label')
            yFormat = ('linear', ylim_left, ylim_right, 0.0, 1.02 * ymax, 1.0, 1.0, r'y axis label')

        zFormat = ('linear', -0.4, 1.85, 0.20)

        # loop over color maps
        for cMap in cMaps:

            zColor = (cMap, zmin, zmax, r'z label (cbar)')

            # assemble outname string
            outname = 'mpl_imshow_autowindow_test_03_nPxs_{}'.format(str(n).zfill(2))
            outname += '_cmap_' + cMap.name
            outname += '_Python_' + platform.python_version() + \
                       '_mpl_' + mpl.__version__

            # call plot function
            outname = plot_pcolor(X = xVals,
                                  Y = yVals,
                                  Z = zVals,
                                  params = [width_X, height_Y],
                                  titlestr = '',
                                  fProps = fProps,
                                  xFormat = xFormat,
                                  yFormat = yFormat,
                                  zFormat = zFormat,
                                  zColor = zColor,
                                  show_cBar = True,
                                  outname = outname,
                                  outdir = OUTDIR,
                                  showlabels = True,
                                  grid = False,
                                  savePDF = True,
                                  saveSVG = True)

    return None

if __name__ == '__main__':

    test_03_with_svg_output()
