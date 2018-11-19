
#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-08-30
# file: mpl_annotate_alignment_minimal.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 2.2.3
##########################################################################################

import time
import datetime
import sys
import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import legend

import matplotlib.font_manager

if __name__ == '__main__':

    print("mpl.matplotlib_fname():", mpl.matplotlib_fname())
    
    mpl.font_manager.findSystemFonts()
    
    flist = mpl.font_manager.get_fontconfig_fonts()
    
    print(flist)
    
    for fname in flist:
        print(fname)
    
    #names = [mpl.font_manager.FontProperties(fname = fname).get_name() for fname in flist]