# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 12:36:13 2024

A set of unit tests for the simple kettle scenario.

For 
    python -m unittest discover
to work, this must be saved in a file entitled test*.py.
 
@author: CM
"""

import unittest
import simpleKettle

class SimpleKettle(unittest.TestCase):
    
    def testTheNameOfThis(self):
        self.assertTrue(True) # Check this test is run without an underscore.
        
    def checkAnotherTestWillRun(self):
        self.assertTrue(True) # This does not run without a title like 'test*'.
        
    
