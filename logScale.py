 #!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-17
# file: logScale.py
# tested with python 2.7.15 in conjunction with mpl version 2.2.3
# tested with python 3.7.0  in conjunction with mpl version 2.2.3
##########################################################################################

import numpy as np

def getLogScalePadding(xminData, xmaxData, paddingFraction):
    """
    Input arguments:
    xminData: minimal data value along a given axis
    xmaxData: maximal data value along a given axis
    paddingFraction: Fraction of the data width, that is desired as the padding of this
                     axis. The paddingFraction is a floating point value in [0.0, 1.0].
    
    Return values:
    xmin, xmax
    
    xminData and xmaxData are the minimal and maximal data values in that axis direction.
    Assuming a logarithmic scaling in this direction, this function returns the
    xmin and xmax values, such that a desired padding of paddingFraction 
    to the left and to the right of the data width is adjusted.
    This assumes log base 10 and that you want to have an equal padding to the left
    as to the right.
    The returned xmin, xmax values can then for example be used by the
    ax.set_xlim(xmin, xmax) command, to achieve the desired effect.
    
    Example:
    A paddingFraction = 0.04 means
    that the padding between xmaxData and xmax will be 4 percent
    of the data extend (dataWidth). Likewise the padding between xmin and xminData will
    equally be 4 percent of the dataWidht (measured in log-10 decaeds).
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
    print(xmin, xmax)

