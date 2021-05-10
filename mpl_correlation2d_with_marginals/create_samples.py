#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-04-11
# file: create_samples.py
# tested with python 3.7.6
##########################################################################################
# description:
# Creates (1) fully correlated and (2) fully independent normally distributed
# random samples using inverse transform sampling (ITS).
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

def inverseTransformSamplingJoint(n_samples, mu1, sigma1, mu2, sigma2):
    u = np.random.uniform(size = n_samples)
    x1 = norm.ppf(u, loc = mu1, scale = sigma1)
    x2 = norm.ppf(u, loc = mu2, scale = sigma2)
    return x1, x2

if __name__ == '__main__':

    print("using np.__version__ =", np.__version__)
    print("using scipy.__version__ =", scipy.__version__)

    # set parameters
    n_samples = 20000

    mu1, sigma1 = 87.25, 8.124
    mu2, sigma2 = 125.75, 11.25

    seed_value = 987654321

    ######################################################################################
    # 01 - Create fully correlated Gaussian samples using the inverse transform method
    samples = np.zeros((n_samples, 2))

    np.random.seed(seed_value)

    samples[:, 0], samples[:, 1] = \
        inverseTransformSamplingJoint(n_samples, mu1, sigma1, mu2, sigma2)
    outname = f'GaussianSamples_correlated_seed_{seed_value:d}.txt'
    np.savetxt(os.path.join(RAWDIR, outname), samples, fmt = '%.8f')

    ######################################################################################
    # 02 - Create two independent Gaussian random realizations

    np.random.seed(seed_value) # reset the seed value

    samples = np.zeros((n_samples, 2))
    samples[:, 0] = norm.rvs(loc = mu1, scale = sigma1, size = n_samples)
    samples[:, 1] = norm.rvs(loc = mu2, scale = sigma2, size = n_samples)
    outname = f'GaussianSamples_uncorrelated_seed_{seed_value:d}.txt'
    np.savetxt(os.path.join(RAWDIR, outname), samples, fmt = '%.8f')
