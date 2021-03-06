#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2021-02-14
# file: test_autoscale.py
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
    print("Running", __file__)
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Python Interpreter Version =", platform.python_version())
    print("/////////////////////////////////////////////////////////////////////////////")
    print("Start testing ...")
    print("/////////////////////////////////////////////////////////////////////////////")

    unittest.main()
