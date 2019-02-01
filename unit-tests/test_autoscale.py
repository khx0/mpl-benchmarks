#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-01
# file: test_autoscale.py
# tested with python 2.7.15
# tested with python 3.7.0
##########################################################################################

import sys
import platform
import numpy as np
import unittest

sys.path.append('../')

from mplUtils import nextHigher

class AutoScaleTest(unittest.TestCase):
    
    """
    Test cases for the autoscaling functionality.
    """
    
    """
    nextHigher(value, baseUnit)
    returns a float, where value is rounded to the next higher value in
    units of the specified baseUnit.
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

    def test_nextHigher_03(self):
                    
        value = -0.37561842
        
        baseUnit = 0.5
        reference_cap = 0.0
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))

        baseUnit = 0.25
        reference_cap = -0.25
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))

        baseUnit = 0.1
        reference_cap = -0.3
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))

        baseUnit = 0.05
        reference_cap = -0.35
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))

        baseUnit = 0.01
        reference_cap = -0.37
        cap = nextHigher(value, baseUnit)
        self.assertTrue(np.isclose(cap, reference_cap))
        
        return None
        
if __name__ == '__main__':
    
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    print("RUNNING ", __file__)
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Python Interpreter Version =", platform.python_version())
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    
    unittest.main()
