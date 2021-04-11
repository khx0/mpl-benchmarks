#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-04-11
# file: create_samples.py
# tested with python 3.7.6 and numpy 1.20.2
##########################################################################################
# description:
# Creates 1d normal random samples and saves them to the disk as *.dat and *.npy files.
##########################################################################################

import os
import datetime
import platform
import numpy as np

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)

CREATE_TXT = False

if __name__ == '__main__':

    print("running python", platform.python_version())
    print("using np.__version__ =", np.__version__)

    # set parameters
    n_samples = 200

    # fixing random state for reproducibility of results
    seed_value = 987654321
    np.random.seed(seed_value)

    # create samples
    sample_A = np.random.normal(loc = 2.0, scale = 1.0, size = n_samples)
    print("sample_A.shape =", sample_A.shape)

    # save samples to file
    outname = f'normal_samples_np_seed_{seed_value}'
    np.save(os.path.join(RAWDIR, outname), sample_A)
    if CREATE_TXT:
        np.savetxt(os.path.join(RAWDIR, outname + '.txt'), sample_A, fmt = '%.8f')

    sample_B = np.random.normal(loc = 1.4, scale = 0.45, size = n_samples)
    print("sample_B.shape =", sample_B.shape)

    data = np.zeros((n_samples, 2))
    data[:, 0] = sample_A
    data[:, 1] = sample_B

    # save samples to file
    outname = f'normal_samples_AB_np_seed_{seed_value}'
    np.save(os.path.join(RAWDIR, outname), data)
    if CREATE_TXT:
        np.savetxt(os.path.join(RAWDIR, outname + '.txt'), data, fmt = '%.8f')
