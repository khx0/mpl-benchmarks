#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-09-15
# file: available_fonts.py
# tested with python 3.7.2 in conjunction with mpl version 3.1.1
##########################################################################################

import platform
import matplotlib as mpl
import matplotlib.font_manager

if __name__ == '__main__':

    print("python version =", platform.python_version())
    print("matplotlib version =", mpl.__version__)

    print("mpl.matplotlib_fname():", mpl.matplotlib_fname())
    print("mpl.get_configdir() =", mpl.get_configdir())

    mpl.font_manager.findSystemFonts()

    # print fonts which are available for the given matplotlib installation
    flist = mpl.font_manager.get_fontconfig_fonts()

    for i, fname in enumerate(flist):

        print("font no.", i, "==>", fname)

