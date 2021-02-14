#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-02-14
# file: test_getPcolorBoxCoordinates.py
# tested with python 3.7.6
##########################################################################################

'''
--- Example invocations ---
Cd to the directory containing this script and there invoke
$python -m pytest (-v)
where python is your chosen python interpreter or alternatively only call
$pytest
or
$pytest -v
using the default python interpreter on your system.
The -v flag (equal to --verbose) sets the pytest mode to 'verbose'.
-------------------------------------------------------------------------------
To only run the tests in this test file use
$python -m pytest (-v) test_*.py
where test_*.py is the considered unit test script.
-------------------------------------------------------------------------------
plain unittest invocation
$python test_*.py
-------------------------------------------------------------------------------
Tested with pytest version 6.2.2.
'''

import sys
import platform
import numpy as np
import unittest

sys.path.append('../')

from mplUtils import getPcolorBoxCoordinates

class PColorBoxCoordinatesTest(unittest.TestCase):

    """
    Test cases for the getPcolorBoxCoordinates function
    """

    def test_01(self):

        xVals = np.array([0.0])
        pixelWidth = 1.0
        res = np.array([-0.5, 0.5])

        xBoxCoords = getPcolorBoxCoordinates(xVals, unitWidth = pixelWidth)

        self.assertTrue(np.array_equal(xBoxCoords, res))
        self.assertTrue(np.allclose(xBoxCoords, res))

        return None

    def test_02(self):

        xVals = np.array([0.0])
        pixelWidth = 12.0
        res = np.array([-6.0, 6.0])

        xBoxCoords = getPcolorBoxCoordinates(xVals, unitWidth = pixelWidth)

        self.assertTrue(np.array_equal(xBoxCoords, res))
        self.assertTrue(np.allclose(xBoxCoords, res))

        return None

    def test_03(self):

        xVals = np.array([0.0])
        res = None

        xBoxCoords = getPcolorBoxCoordinates(xVals)

        self.assertTrue(res == xBoxCoords)

        xVals = np.array([9876.1234])
        res = None

        xBoxCoords = getPcolorBoxCoordinates(xVals)

        self.assertTrue(res == xBoxCoords)

        return None

    def test_04(self):

        xVals = np.array([0.0, 1.0, 2.0])
        res = np.array([-0.5, 0.5, 1.5, 2.5])

        xBoxCoords = getPcolorBoxCoordinates(xVals)

        self.assertTrue(np.array_equal(xBoxCoords, res))
        self.assertTrue(np.allclose(xBoxCoords, res))
        self.assertTrue(res.shape == xBoxCoords.shape)
        self.assertTrue(len(xVals) + 1 == len(xBoxCoords))

        return None

    def test_05(self):

        xVals = np.array([0.2, 0.4, 0.6])
        res = np.array([0.1, 0.3, 0.5, 0.7])

        xBoxCoords = getPcolorBoxCoordinates(xVals)

        self.assertTrue(np.array_equal(xBoxCoords, res))
        self.assertTrue(np.allclose(xBoxCoords, res))
        self.assertTrue(res.shape == xBoxCoords.shape)
        self.assertTrue(len(xVals) + 1 == len(xBoxCoords))

        return None
        
    def test_06(self):

        xVals = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        res = np.array([0.05, 0.15, 0.25, 0.35, 0.45, 0.55])

        xBoxCoords = getPcolorBoxCoordinates(xVals)

        self.assertTrue(np.allclose(xBoxCoords, res))
        self.assertTrue(res.shape == xBoxCoords.shape)
        self.assertTrue(len(xVals) + 1 == len(xBoxCoords))

        return None

if __name__ == '__main__':

    print("/////////////////////////////////////////////////////////////////////////////")
    print("Running", __file__)
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Python Interpreter Version =", platform.python_version())
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Start testing ...")
    print("/////////////////////////////////////////////////////////////////////////////")

    unittest.main()
