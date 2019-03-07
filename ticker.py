#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-07
# file: ticker.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import numpy as np

def getLogTicksBase10(min, max, comb = np.arange(1, 10)):
    '''
    Returns logarithmic base 10 ticks between min and max (inclusive at both ends).
    [min, max]
    
    The default comb for base 10 logarithmic ticks is comb = [1, 2, 3, 4, 5, 6, 7, 8, 9],
    which kan be changed by overwriting the default keyword argument.
    
    Example:
    using 
    min = 3.0e2 
    and
    max = 8.0e4
    will return a 1d (numpy) tick array with
    ticks =               [3.0e2, 4.0e2, 5.0e2, 6.0e2, 7.0e2, 8.0e2, 9.0e2,
             1.0e3, 2.0e3, 3.0e3, 4.0e3, 5.0e3, 6.0e3, 7.0e3, 8.0e3, 9.0e3,
             1.0e4, 2.0e4, 3.0e4, 4.0e4, 5.0e4, 6.0e4, 7.0e4, 8.0e4] 
    
    Example usage:
    Here the minor ticks have no labels (NullFormatter).
    ****************************************************************
    ...
    ax.set_xscale('log')
    xMinorTicks = getLogTicksBase10(1.0e-12, 1.0e-6)
    ax.xaxis.set_minor_locator(ticker.FixedLocator((xMinorTicks)))
    ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    ...
    ****************************************************************
    '''
    if (min > max):
        min, max = max, min
    
    expMin = int(np.floor(np.log10(min)))
    expMax = int(np.floor(np.log10(max)))
    
    if np.isclose(expMin, expMax):
    	tmp = comb * 10.0 ** expMin
    	tmp = tmp[tmp >= min]
    	return tmp[tmp <= max]

    ticks = np.array([])

    tmp = comb * 10.0 ** expMin
    
    ticks = np.concatenate((ticks, tmp[tmp >= min]), axis = 0)
    
    for exp in np.arange(expMin + 1, expMax, 1).astype(int):
        tmp = comb * 10.0 ** exp
        ticks = np.concatenate((ticks, tmp), axis = 0)
    
    tmp = comb * 10.0 ** (expMax)
    ticks = np.concatenate((ticks, tmp[tmp <= max]), axis = 0)
    
    return ticks
    
def cleanFormatter(x, pos):
    '''
    will format 0.0 as 0 and
    will format 1.0 as 1
    '''
    return '{:g}'.format(x)

if __name__ == '__main__':
    
    pass
