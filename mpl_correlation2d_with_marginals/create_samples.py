#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-02-23
# file: create_samples.py
# tested with python 3.7.6
##########################################################################################
# description:
# Creates fully correlated (1) and fully independent (2) normally distributed
# random samples using inverse transform sampling.
##########################################################################################

import os
import datetime
import numpy as np
import scipy
from scipy.stats import norm

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)

def inverseTransformSamplingJoint(nSamples, mu1, sigma1, mu2, sigma2):
    u = np.random.uniform(size = nSamples)    
    x1 = norm.ppf(u, loc = mu1, scale = sigma1)
    x2 = norm.ppf(u, loc = mu2, scale = sigma2)
    return x1, x2

if __name__ == '__main__':

    print("using np.__version__ =", np.__version__)
    print("using scipy.__version__ =", scipy.__version__)

    # set parameters
    nSamples = 20000
    
    mu1, sigma1 = 87.25, 8.124
    mu2, sigma2 = 125.75, 11.25

    seedValue = 987654321

    ######################################################################################
    # 01 - Create fully correlated Gaussian samples using the inverse transform method
    samples = np.zeros((nSamples, 2))
    
    np.random.seed(seedValue)
    
    samples[:, 0], samples[:, 1] = \
        inverseTransformSamplingJoint(nSamples, mu1, sigma1, mu2, sigma2)
    outname = 'GaussianSamples_correlated_seed_{:d}.txt'.format(seedValue)
    np.savetxt(os.path.join(RAWDIR, outname), samples, fmt = '%.8f')

    ######################################################################################
    # 02 - Create two independent Gaussian random realizations

    np.random.seed(seedValue)

    samples = np.zeros((nSamples, 2))
    samples[:, 0] = norm.rvs(loc = mu1, scale = sigma1, size = nSamples)
    samples[:, 1] = norm.rvs(loc = mu2, scale = sigma2, size = nSamples)
    outname = 'GaussianSamples_uncorrelated_seed_{:d}.txt'.format(seedValue)
    np.savetxt(os.path.join(RAWDIR, outname), samples, fmt = '%.8f')
