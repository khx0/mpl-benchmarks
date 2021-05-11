#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-05-11
# file: available_fonts.py
# tested with python 3.7.6 in conjunction with mpl version 3.4.2
##########################################################################################

import platform
import matplotlib as mpl
import matplotlib.font_manager
import numpy as np

def number_of_digits(n: int) -> int:
    '''
    Returns the number of digits of a given integer n.
    '''
    return int(np.floor(np.log10(np.abs(n)) + 1))

if __name__ == '__main__':

    print("python version =", platform.python_version())
    print("matplotlib version =", mpl.__version__)

    print("mpl.matplotlib_fname() =", mpl.matplotlib_fname())
    print("mpl.get_configdir() =", mpl.get_configdir())

    mpl.font_manager.findSystemFonts()

    # print fonts which are available for the given matplotlib installation
    flist = mpl.font_manager.get_fontconfig_fonts()

    n_digits = number_of_digits(len(flist))

    for i, fname in enumerate(flist):

        print("font #", str(i + 1).zfill(n_digits), "-->", fname)

    print(f'{len(flist)} fonts detected in total')
