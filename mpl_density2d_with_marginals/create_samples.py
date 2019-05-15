#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-05-15
# file: create_samples.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.2  in conjunction with mpl version 3.0.3
##########################################################################################

import os
import datetime
import numpy as np
import scipy
from scipy.stats import norm

now = datetime.datetime.now()
now = "{}-{}-{}".format(str(now.year), str(now.month).zfill(2), str(now.day).zfill(2))

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)

def inverseTransformSamplingJoint(mu1, sigma1, mu2, sigma2):
    u = np.random.uniform()    
    x1 = norm.ppf(u, loc = mu1, scale = sigma1)
    x2 = norm.ppf(u, loc = mu2, scale = sigma2)
    return x1, x2

if __name__ == '__main__':

    print("using scipy.__version__ =", scipy.__version__)

    # set parameters
    nSamples = 20000
    
    mu1, sigma1 = 87.25, 8.124
    mu2, sigma2 = 125.75, 11.25

    seedValue = 987654321

    #####################################################################################
    # 01 - Create fully correlated Gaussian samples using the inverse transform method
    samples = np.zeros((nSamples, 2))
    
    np.random.seed(seedValue)

    for i in range(nSamples):
    
        x1, x2 = inverseTransformSamplingJoint(mu1, sigma1, mu2, sigma2)
        samples[i, 0] = x1
        samples[i, 1] = x2

    np.savetxt(os.path.join(RAWDIR, 'GaussianSamples_correlated.txt'), samples, fmt = '%.8f')

    #####################################################################################
    # 02 - Create two independent Gaussian random realizations

    np.random.seed(seedValue)

    samples = np.zeros((nSamples, 2))
    samples[:, 0] = norm.rvs(loc = mu1, scale = sigma1, size = nSamples)
    samples[:, 1] = norm.rvs(loc = mu2, scale = sigma2, size = nSamples)

    np.savetxt(os.path.join(RAWDIR, 'GaussianSamples_uncorrelated.txt'), samples, fmt = '%.8f')
