#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2018-09-18
# file: test_autoscale.py
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################

import os
import sys
import numpy as np
import unittest

sys.path.append('../')

from mplUtils import nextHigher

class AutoScaleTest(unittest.TestCase):
    
    """
    Test cases for the autoscaling functionality.
    """
    
    def test_nextHigher_01(self):
                    
        value = 22.75
        
        baseUnit = 5.0
        reference_cap = 25.0
        
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))

        baseUnit = 10.0
        reference_cap = 30.0
        
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))
        
        baseUnit = 50.0
        reference_cap = 50.0
        
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))
        
        baseUnit = 100.0
        reference_cap = 100.0
        
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))
        
        return None
        
    def test_nextHigher_02(self):
                    
        value = -0.375
        
        baseUnit = 1.0
        reference_cap = 0.0
        
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))
    
        baseUnit = 10.0
        reference_cap = 0.0
        
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))
        
        baseUnit = 50.0
        reference_cap = 0.0
        
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))
        
        baseUnit = 100.0
        reference_cap = 0.0
        
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))

        return None
        
if __name__ == '__main__':

    unittest.main()
    
    
    
    
    
