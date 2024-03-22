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
# from appendicesAll import create_process_plant_hexane_storage_tank
import boundary_onto

class TestNewUnitTests(unittest.TestCase):
    
    def test_UnitTestsCanAssertTrue(self):
        """
        Test the ability to run unit tests using
        python -m unittest discover

        Returns
        -------
        None.

        """
        self.assertTrue('FOO'.isupper()) # Test the ability to run unit tests.
        
    def testTheNameOfThis(self):
        self.assertTrue(True) # Check this test is run without an underscore.
        
    def checkAnotherTestWillRun(self):
        self.assertTrue(True) # This does not run without a title like 'test*'.
        
    def testAnObjectCanBeMade(self):
        
        someNewCause = boundary_onto.UpstreamProcessInvolved()
        self.assertIsNotNone(someNewCause) # Can an object be created?

class TestTheGivenMainFunction(unittest.TestCase):
    
    processModel = None
    
    def setUp(self): # Called before every test* method.
        pass
    
    def tearDown(self): # Called after every test* method.
        pass
    
    def testModelCreation(self):
        
        # process_plant_model = model.create_hazid_benchmark_1()
        process_plant_model = appendicesAll.create_process_plant_hexane_storage_tank()
        self.assertNotNone(process_plant_model)
        
    def testCreateOlefinModel(self):
        
        process_plant_model = appendicesAll.create_olefin_feed_section()
        self.assertNotNone(process_plant_model)
        
    def testGraphType(self):
        
        process_plant_model = appendicesAll.create_hazid_benchmark_1()
        graphType = appendicesAll.findTypeOf(process_plant_model)
        self.assertIsInstance(graphType, appendicesAll.GraphType)



#%% Appendix S - Unit Tests

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

