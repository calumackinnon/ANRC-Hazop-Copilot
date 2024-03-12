# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:53:23 2024

@author: qrb15201
"""

class OverallModel:
    
    pass



class SiteInformation():
    
    pass

    def __init__():
        
        pass

class HexaneTankModel(OverallModel):
    
    siteInfo = None
    
    def __init__(self):
        
        self.siteInfo = SiteInformation()

class Ports:
    
    def __init__(self):
        
        pass

class BoundaryCondition:
    
    def __init__(self):
        
        pass

class Substance:
    
    def __init__(self):
        
        pass
    

class EquipmentEntity:
    
    ports = None
    boundaryCondition = None
    substance = None
    

class TankTruck(EquipmentEntity):
    
    def __init__(self):
        
        pass

class Pump(EquipmentEntity):
    
    def __init__(self):
        
        pass


class ConnectionPipe(EquipmentEntity):
    
    def __init__(self):
        
        pass


class StorageTank(EquipmentEntity):
    
    def __init__(self):
        
        pass


def create_process_plant_hexane_storage_tank():
    
    hazard_classes = [substance_onto.FlammableLiquidCategory2, 
                      substance_onto.SkinCorrosionIrritationCategory2,
                      substance_onto.ReproductiveToxicityCategory2, 
                      substance_onto.SpecificTargetOrganToxicityRepeatedExposureCategory2,
                      substance_onto.SpecificTargetOrganToxicitySingleExposureCategory3, 
                      substance_onto.AspirationHazardCategory1
                      ]
    
    stability_reactivity_information = [
        substance_onto.FormsExplosiveMixtureWithAir,
        substance_onto.ReactsViolentlyWithOxidizer
        ]
    
    
