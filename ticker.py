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
    
    expMin, expMax = np.log10(min), np.log10(max)
    
    tmp = comb * 10.0 ** expMin
    ticks = np.concatenate((ticks, tmp[tmp >= min]), axis = 0)
    
    for exp in np.arange(expMin + 1, expMax, 1).astype(int):
        tmp = comb * 10.0 ** exp
        ticks = np.concatenate((ticks, tmp), axis = 0)
    
    tmp = comb * 10 ** (expMax)
    ticks = np.concatenate((ticks, tmp[tmp <= max]), axis = 0)
    
    return ticks

if __name__ == '__main__':
        
    # make this the first unit test
    min = 1.0e-12
    max = 1.0e-10
    
    ticks = getLogTicksBase10(min, max)
    
    assert len(ticks) == 19, "len(ticks) assertion failed."
    
    print("ticks =", ticks)
    
    