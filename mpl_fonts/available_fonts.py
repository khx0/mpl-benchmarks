#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-01-11
# file: available_fonts.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 3.0.2
##########################################################################################

import matplotlib as mpl
import matplotlib.font_manager

if __name__ == '__main__':

    print("mpl.matplotlib_fname():", mpl.matplotlib_fname())

    mpl.font_manager.findSystemFonts()
     
     
    # print fonts which are available for the given matplotlib installation
    flist = mpl.font_manager.get_fontconfig_fonts()    

    for i, fname in enumerate(flist):
        
        print(i, fname)