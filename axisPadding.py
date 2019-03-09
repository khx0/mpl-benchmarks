 #!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-03-09
# file: axisPadding.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import numpy as np

def getLinearAxisPadding(xminData, xmaxData, paddingFraction):
    """
    Input arguments:
    xminData: minimal data value along a given axis
    xmaxData: maximal data value along a given axis
    paddingFraction: Fraction of the data width, that is desired as the padding of this
                     axis. The paddingFraction is a floating point value in [0.0, 1.0].
    
    Return values:
    xmin, xmax
    """
    dataWidth = xmaxData - xminData
    xmax = xmaxData + dataWidth * paddingFraction
    xmin = xminData - dataWidth * paddingFraction
    return xmin, xmax

def getLogAxisPadding(xminData, xmaxData, paddingFraction):
    """
    Input arguments:
    xminData: minimal data value along a given axis
    xmaxData: maximal data value along a given axis
    paddingFraction: Fraction of the data width, that is desired as the padding of this
                     axis. The paddingFraction is a floating point value in [0.0, 1.0].
    
    Return values:
    xmin, xmax
    
    Same as getLinearAxisPadding taylored for logarithmic axis scaling.
    
    xminData and xmaxData are the minimal and maximal data values in that axis direction.
    Assuming a logarithmic axis scaling in this direction, this function returns a
    xmin and xmax value pair, such that a desired padding of paddingFraction 
    to the left and to the right of the data width along this axis is set.
    This assumes base 10 logarithms and that you want to have an equal padding to the left
    as to the right.
    The returned xmin, xmax values can then for example be used by the
    ax.set_xlim(xmin, xmax) command, to achieve the desired effect.
    Or alternatively by ax.set_ylim(xmin, xmax) for a given y-axis.
    
    Example:
    A paddingFraction = 0.04 means
    that the padding between xmaxData and xmax will be 4 percent
    of the data extend (dataWidth). Likewise the padding between xmin and xminData will
    equally be 4 percent of the dataWidth (measured in log-10 decades).

	### Math description
	Given the minimal and maximal data extend, we define the data width (extent of the data)
	as
	$\Delta w = \log_{10}(xmaxData / xminData) = \log_{10}(xmaxData) - log_{10}(xminData)$
	For the padding along a given axis to the right, we want the following equation to hold
	$\log_{10}(xmax) - \log_{10}(xmaxData) = pF * \Delta w$, where pF is the padding Fraction, and
	xmax the yet unknown maximal value, that we wish to determine. Isolating this last
	equation for xmax simply gives:
	$xmax = xmaxData \cdot 10^{pF * \Delta w}$
	Similarly for the left padding, the governing equation reads
	$\log_{10}(xminData) - \log_{10}(xmin) = pF * \Delta w$,
	assuming an equal padding fraction to the left and to the right. Isolating this equation
	for xmin simply gives
	$xmin = xminData * 10^{-pF * \Delta w}$. 
    """
    
    # data width measured in log-10 decades
    dataWidth = np.log10(xmaxData / xminData) 
    xmin = xminData * 10.0 ** (- paddingFraction * dataWidth) 
    xmax = xmaxData * 10.0 ** (+ paddingFraction * dataWidth)
    
    return xmin, xmax

if __name__ == '__main__':
    
    pass
