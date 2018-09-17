#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-17
# file: test_filter.py
##########################################################################################

import os
import sys
import numpy as np
import unittest

sys.path.append('../')

from logScale import getLogScalePadding

class LogScaleTest(unittest.TestCase):
    
    """
    Test cases for the logScale module.
    """
    
    def test_logScale_01(self):
    
        xminData = 1.0e-11
        xmaxData = 1.0e-9
        paddingFraction = 0.04
        
        xmin_reference = 8.317637711026709e-12
        xmax_reference = 1.202264434617413e-09
        
        xmin, xmax = getLogScalePadding(xminData, xmaxData, paddingFraction)
        
        self.assertTrue(np.isclose(xmin, xmin_reference))
        self.assertTrue(np.isclose(xmax, xmax_reference))
        
        return None
        
if __name__ == '__main__':

    unittest.main()
    
    
    
    
    
