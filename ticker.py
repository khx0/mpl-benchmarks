#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-18
# file: ticker.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import numpy as np

def getLogTicksBase10(min, max, comb = np.arange(1, 10)):
    '''
    Returns logarithmic base 10 ticks between min and max (inclusive at both ends).
    '''
    if (min > max):
        min, max = max, min
    
    ticks = np.array([])
    
    expMin = int(np.floor(np.log10(min)))
    expMax = int(np.floor(np.log10(max)))
    
    tmp = comb * 10.0 ** expMin
    
    ticks = np.concatenate((ticks, tmp[tmp >= min]), axis = 0)
    
    for exp in np.arange(expMin + 1, expMax, 1).astype(int):
        tmp = comb * 10.0 ** exp
        ticks = np.concatenate((ticks, tmp), axis = 0)
    
    tmp = comb * 10.0 ** (expMax)
    ticks = np.concatenate((ticks, tmp[tmp <= max]), axis = 0)
    
    return ticks

if __name__ == '__main__':
    
    pass