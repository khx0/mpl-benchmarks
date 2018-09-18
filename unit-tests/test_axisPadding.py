#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-17
# file: test_logScale.py
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################

import os
import sys
import numpy as np
import unittest

sys.path.append('../')

from axisPadding import getLinearAxisPadding
from axisPadding import getLogAxisPadding

class AxisPaddingTest(unittest.TestCase):
    
    """
    Test cases for the axisPadding module.
    """
    
    def test_linearScale_01(self):
        
        xminData = 0.0
        xmaxData = 2.0
        paddingFraction = 0.05
        
        xmin_reference = -0.1
        xmax_reference = 2.1
        
        xmin, xmax = getLinearAxisPadding(xminData, xmaxData, paddingFraction)
        
        self.assertTrue(np.isclose(xmin, xmin_reference))
        self.assertTrue(np.isclose(xmax, xmax_reference))

    def test_linearScale_02(self):
        
        xminData = -99.0
        xmaxData = 53.0
        paddingFraction = 0.03
        
        xmin_reference = -99.0 - 4.56
        xmax_reference = 53.0 + 4.56
        
        xmin, xmax = getLinearAxisPadding(xminData, xmaxData, paddingFraction)
        
        self.assertTrue(np.isclose(xmin, xmin_reference))
        self.assertTrue(np.isclose(xmax, xmax_reference))
    
    def test_logScale_01(self):
    
        xminData = 1.0e-11
        xmaxData = 1.0e-9
        paddingFraction = 0.04
        
        xmin_reference = 8.317637711026709e-12
        xmax_reference = 1.202264434617413e-09
        
        xmin, xmax = getLogAxisPadding(xminData, xmaxData, paddingFraction)
        
        self.assertTrue(np.isclose(xmin, xmin_reference))
        self.assertTrue(np.isclose(xmax, xmax_reference))
        
        return None
        
if __name__ == '__main__':

    unittest.main()
    
    
    
    
    
