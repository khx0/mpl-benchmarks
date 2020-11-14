#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-11-14
# file: mpl_array_plot.py
# tested with python 3.7.6 in conjunction with mpl version 3.3.3
##########################################################################################

import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def plot_patch_array(X, nrows, ncols, outname, outdir, cmap,
                     transparent = True, savePNG = True, datestamp = True):

    f, axs = plt.subplots(nrows = nrows,
                          ncols = ncols,
                          figsize = (5, 5),
                          subplot_kw = {'xticks': [], 'yticks': []})

    plt.subplots_adjust(wspace = 0.1, hspace = 0.005,
                        left = 0.01, right = 0.99,
                        bottom = 0.01, top = 0.99)

    for i, ax in enumerate(axs.flat):
        ax.imshow(X[i], cmap = cmap)

    # save to file
    outname += '_cmap_' + cmap
    if transparent:
        outname += '_transparent_background'
    else:
        outname += '_white_background'

    outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__

    if datestamp:
        outname += '_' + today         
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png',
                  dpi = 600,
                  transparent = transparent)

    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return None

if __name__ == '__main__':

    # (pseudo) random number handling
    random_seed = 123456789
    # fix random state for reproducibility
    np.random.seed(random_seed)

    # create synthetic data
    patch_shape = (5, 5)

    n_patches = 25
    patches = []
    for idx in range(n_patches):
        tmp = np.random.rand(patch_shape[0], patch_shape[1])
        # print(idx, tmp.shape)
        patches.append(tmp)
    print("len(patches) =", len(patches))

    # call plotting function
    outname = 'array_plot_seed_' + str(random_seed).zfill(2)

    plot_patch_array(patches, 5, 5, outname, OUTDIR, cmap = 'gray')
    plot_patch_array(patches, 5, 5, outname, OUTDIR, cmap = 'gray', transparent = False)
    plot_patch_array(patches, 5, 5, outname, OUTDIR, cmap = 'viridis')
