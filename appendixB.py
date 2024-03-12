# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:09:11 2024

@author: qrb15201
"""

class MySubstance:
    
    def __init__(self,
        substance_name,
        cas_number,
        freezing_point,
        boiling_point,
        flash_point,
        lower_explosion_limit,
        upper_explosion_limit):
        
        self.name = substance_name
        self.cas_number = cas_number
        self.onto_object = None
        self.freezing_point = freezing_point
        self.boiling_point = boiling_point
        self.flash_point = flash_point
        self.lower_explosion_limit = lower_explosion_limit
        self.upper_explosion_limit = upper_explosion_limit
        self.task = []
        self.intended_state_of_aggregation = []
        self.hazard_class = []
        self.stability_reactivity_information = []
    
    def add_hazard_class(self, hazard_class):
        
        if hazard_class:
            for haz_c in hazard_class:
                self.hazard_class.append(haz_c(None))
    
    def add_stability_reactivity_information(self, stability_reactivity_information):
        if stability_reactivity_information:
            for sr_info in stability_reactivity_information:
                self.stability_reactivity_information.append(sr_info())
    
    def set_intended_state_of_aggregation(self, state_of_aggregation):
        if state_of_aggregation:
            self.intended_state_of_aggregation.append(state_of_aggregation())
    
    def set_substance_task(self, substance_task):
        self.task.append(substance_task())
    
    def assemble_onto_object(self, substance):
        self.onto_object = substance(hasSpecificTask=self.task,
            hasStabilityReactivityInformation=self.stability_reactivity_information,
            hasHazardClass=self.hazard_class,
            hasStateOfAggregation=self.intended_state_of_aggregation,
            hasBoilingPointInKelvin=self.boiling_point,
            hasFreezingPointInKelvin=self.freezing_point,
            hasFlashpointInKelvin=self.flash_point,
            hasUpperExplosionLimitInPercent=self.upper_explosion_limit,
            hasLowerExplosionLimitInPercent=self.lower_explosion_limit
        )