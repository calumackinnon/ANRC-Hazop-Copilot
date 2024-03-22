# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 10:08:23 2024

From an Anaconda command line interface set to the relevant environment, use
python -m unittest discover 
to find and run the unit tests specified in this test_*.py file.

These can be written in order to test specific parts of the code, to make sure
we get each smaller subcomponent working.

This is described at https://docs.python.org/3/library/unittest.html.

@author: qrb15201
"""

import unittest

#%% Appendix S - Unit Tests

class TestNewUnitTests(unittest.TestCase):
    
    def test_assertTrue(self):
        self.assertTrue('FOO'.isupper())

class TestUnderlyingCauses(unittest.TestCase):
    
    def test_solar_radiation_1(self):
        cause = causes_onto.AbnormalHeatInput()
        boundary_condition = [boundary_onto.LocatedOutside()]
        super_cause = causes_onto.SuperCause(isSupercauseOfCause=[cause],
        supercauseRequiresBoundaryCondition=boundary_condition)
        sync_reasoner()
        super_cause_ = pre_processing.stringify_cleanup_inferred_res(super_cause)
        super_cause_.sort()
        time.sleep(0.01)
        self.assertEqual(super_cause_, ['SolarRadiation'], "Should be ['SolarRadiation']")
 
    def test_blocked_piping_heat_input_1(self):
        cause = causes_onto.ThermalExpansion()
        unit = equipment_onto.ConnectionPipeEntity()
        boundary_condition = [boundary_onto.ExternalFirePossible()]
        super_cause = causes_onto.SuperCause(isSupercauseOfCause=[cause],
                                             supercauseInvolvesUnit=[unit],
                                             supercauseRequiresBoundaryCondition=boundary_condition)
        sync_reasoner()
        super_cause_ = pre_processing.stringify_cleanup_inferred_res(super_cause)
        super_cause_.sort()
        time.sleep(0.01)
        self.assertEqual(super_cause_, ['BlockedPipingAndHeatInput'],
                         "Should be ['BlockedPipingAndHeatInput']")

