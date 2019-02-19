#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2019-02-18
# file: test_ticker.py
# tested with python 2.7.15
# tested with python 3.7.2
##########################################################################################

import sys
import platform
import numpy as np
import unittest

sys.path.append('../')

from ticker import getLogTicksBase10

class TickerTest(unittest.TestCase):
    '''
    Test cases for the ticker module.
    '''
    
    def test_log_ticks_01(self):
        
        min = 1.0e-12
        max = 1.0e-10
        
        ticks_ref = np.array([
            1.0e-12, 2.0e-12, 3.0e-12, 4.0e-12, 5.0e-12,\
            6.0e-12, 7.0e-12, 8.0e-12, 9.0e-12,\
            1.0e-11, 2.0e-11, 3.0e-11, 4.0e-11, 5.0e-11, \
            6.0e-11, 7.0e-11, 8.0e-11, 9.0e-11, \
            1.0e-10])
        
        ticks = getLogTicksBase10(min, max)
        
        self.assertTrue(len(ticks) == 19)
        self.assertTrue(np.allclose(ticks, ticks_ref))
        
        #####################################################
        # ToDo item added [2019-02-18]
        # self.assertTrue(np.array_equal(ticks, ticks_ref))
        # np.array_equal will return False due to
        # numerical round off issues.
        # Try to make the ticker module robust against these
        # numerical machine precision effects.
        #####################################################
        
        return None

    def test_log_ticks_02(self):
        
        min = 2.0e-12
        max = 1.0e-10
        
        ticks_ref = np.array([
            2.0e-12, 3.0e-12, 4.0e-12, 5.0e-12,\
            6.0e-12, 7.0e-12, 8.0e-12, 9.0e-12,\
            1.0e-11, 2.0e-11, 3.0e-11, 4.0e-11, 5.0e-11, \
            6.0e-11, 7.0e-11, 8.0e-11, 9.0e-11, \
            1.0e-10])
        
        ticks = getLogTicksBase10(min, max)
        
        self.assertTrue(len(ticks) == 18)
        self.assertTrue(np.allclose(ticks, ticks_ref))
                
        return None
     
    def test_log_ticks_03(self):
        
        min = 2.0e-12
        max = 7.0e-11
        
        ticks_ref = np.array([
            2.0e-12, 3.0e-12, 4.0e-12, 5.0e-12,\
            6.0e-12, 7.0e-12, 8.0e-12, 9.0e-12,\
            1.0e-11, 2.0e-11, 3.0e-11, 4.0e-11, 5.0e-11, \
            6.0e-11, 7.0e-11])
        
        ticks = getLogTicksBase10(min, max)
        
        self.assertTrue(len(ticks) == 15)
        self.assertTrue(np.allclose(ticks, ticks_ref))
                
        return None
        
    def test_log_ticks_04(self):
        
        min = 1.0e2
        max = 1.0e3
        
        ticks_ref = np.array([
            1.0e2, 2.0e2, 3.0e2, 4.0e2, 5.0e2,\
            6.0e2, 7.0e2, 8.0e2, 9.0e2,\
            1.0e3])
        
        ticks = getLogTicksBase10(min, max)
        
        self.assertTrue(len(ticks) == 10)
        self.assertTrue(np.allclose(ticks, ticks_ref))
                
        return None
        
    def test_log_ticks_05(self):
        
        min = 8.0e2
        max = 1.0e3
        
        ticks_ref = np.array([8.0e2, 9.0e2, 1.0e3])
        
        ticks = getLogTicksBase10(min, max)
        
        self.assertTrue(len(ticks) == 3)
        self.assertTrue(np.allclose(ticks, ticks_ref))
                
        return None

if __name__ == '__main__':
    
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running ", __file__)
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Python Interpreter Version =", platform.python_version())
    print("/////////////////////////////////////////////////////////////////////////////")
    print("/////////////////////////////////////////////////////////////////////////////")
    
    unittest.main()
