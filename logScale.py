 #!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-17
# file: logScale.py
##########################################################################################

import numpy as np

def getLogScalePadding(xminData, xmaxData, paddingFraction):
    """
    xminData and xmaxData are the minimal and maximal data values in that axis direction.
    Assuming a logarithmic scaling in this direction, this function returns the
    xmin and xmax values, such that a desired padding of paddingFraction 
    to the left and to the right of the data width is adjusted.
    This assumes log base 10 and that you want to have an equal padding to the left
    as to the right.
    
    paddingFraction is in [0.0, 1.0]
    E.g. a paddingFraction = 0.04 means
    that the padding between xmaxData and xmax will be 4 percent
    of the dataWidht. Likewise the padding between xmin and xminData will
    equally be 4 percent of the dataWidht (measured in log-10 decaeds).
    
    Returns the xmin, xmax pair,
    which then can for example be used by the
    ax.set_xlim(xmin, xmax) command.
    """
    
    # data width measured in log-10 decades
    dataWidth = np.log10(xmaxData / xminData) 
    xmin = xminData * 10.0 ** (- paddingFraction * dataWidth) 
    xmax = xmaxData * 10.0 ** (+ paddingFraction * dataWidth)
    
    return xmin, xmax
    
if __name__ == '__main__':

    xminData = 1.0e-11
    xmaxData = 1.0e-9
    paddingFraction = 0.04
    xmin, xmax = getLogScalePadding(xminData, xmaxData, paddingFraction)
    print xmin, xmax

