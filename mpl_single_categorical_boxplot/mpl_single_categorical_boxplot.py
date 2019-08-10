#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-08-10
# file: mpl_single_categorical_boxplot.py
# tested with python 3.7.2
##########################################################################################

import os
import datetime
import platform
import numpy as np
import matplotlib as mpl

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)
os.makedirs(OUTDIR, exist_ok = True)

if __name__ == '__main__':

    print("running on python", platform.python_version())
    print("using mpl.__version__ =", mpl.__version__)

#     set parameters
#     nSamples = 200
# 
#     seedValue = 987654321
# 
#     np.random.seed(seedValue)
# 
#     create samples
#     samples = np.random.normal(loc = 2.0, scale = 1.0, size = nSamples)
#     print("samples.shape =", samples.shape)
# 
#     save samples to file
#     outname = 'normal_samples_np_seed_{:d}'.format(seedValue)
#     np.savetxt(os.path.join(RAWDIR, outname + '.dat'), samples, fmt = '%.8f')
#     np.save(os.path.join(RAWDIR, outname), samples)
