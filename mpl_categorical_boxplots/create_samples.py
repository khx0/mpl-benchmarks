#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-08-14
# file: create_samples.py
# tested with python 3.7.2
##########################################################################################
# description:
# Creates a 1d normal random sample and saves it to the disk as *.dat and *.npy file.
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

if __name__ == '__main__':

    print("running on python", platform.python_version())
    print("using np.__version__ =", np.__version__)

    # set parameters
    nSamples = 200

    # fixing random state for reproducibility of results
    seedValue = 987654321
    np.random.seed(seedValue)

    # create samples
    samples = np.random.normal(loc = 2.0, scale = 1.0, size = nSamples)
    print("samples.shape =", samples.shape)

    # save samples to file
    outname = 'normal_samples_np_seed_{:d}'.format(seedValue)
    np.savetxt(os.path.join(RAWDIR, outname + '.dat'), samples, fmt = '%.8f')
    np.save(os.path.join(RAWDIR, outname), samples)

    sample_B = np.random.normal(loc = 1.4, scale = 1.25, size = nSamples)
    print("sample_B.shape =", sample_B.shape)

    data = np.zeros((nSamples, 2))
    data[:, 0] = samples
    data[:, 1] = sample_B

    # save samples to file
    outname = 'normal_samples_np_seed_{:d}'.format(seedValue)
    np.savetxt(os.path.join(RAWDIR, outname + '.dat'), samples, fmt = '%.8f')
    np.save(os.path.join(RAWDIR, outname), samples)

