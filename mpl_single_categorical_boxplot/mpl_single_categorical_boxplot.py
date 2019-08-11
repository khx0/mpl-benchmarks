#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-08-11
# file: mpl_single_categorical_boxplot.py
# tested with python 3.7.2
##########################################################################################

import os
import datetime
import platform
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)
os.makedirs(OUTDIR, exist_ok = True)

def create_boxplot(X):
    '''
    cretaes a single categorical (x - axis) boxplot using the given data sample X
    :params X: numpy.ndarray
    '''

    f, ax1 = plt.subplots()

    ax1.boxplot(X)

    # plt.show()
    
    return None

if __name__ == '__main__':

    print("running on python", platform.python_version())
    print("using mpl.__version__ =", mpl.__version__)

    filename = r'normal_samples_np_seed_987654321.npy'

    data = np.load(os.path.join(RAWDIR, filename))
    print(data.shape)
    
    create_boxplot(X = data)
    
    
