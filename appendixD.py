# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:14:58 2024

@author: qrb15201
"""

def source(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.SourceEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature )
    equipment_entity.set_intended_function(process_onto.NoIntendedFunction)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def sink(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.SinkEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_intended_function(process_onto.NoIntendedFunction)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def connection_pipe(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.ConnectionPipeEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_intended_function(process_onto.Transport)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def tank_truck(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume_of_enclosure):
    equipment = equipment_onto.TankTruckEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_volume_of_enclosure(volume_of_enclosure)
    equipment_entity.set_intended_function(process_onto.Loading)
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_piping(equipment_onto.TankTruckHose)
    equipment_entity.add_instrumentation((equipment_onto.ApiAdaptorValve, "{}-VA1".format(identifier)))
    equipment_entity.add_fixture(equipment_onto.Baffle)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def storage_tank_1(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.StorageTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.set_apparatus(equipment_onto.AtmosphericStorageTank)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def storage_tank_2(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume_of_enclosure):

    equipment = equipment_onto.StorageTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_volume_of_enclosure(volume_of_enclosure)
    equipment_entity.set_apparatus(equipment_onto.AtmosphericStorageTank)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.add_piping(equipment_onto.VentPipe)
    equipment_entity.add_instrumentation((equipment_onto.LevelIndicator, None))
    equipment_entity.add_instrumentation((equipment_onto.HighLevelAlarm, None))
    # equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)

    return equipment_entity

def cooled_storage_tank_1(identifier, circumstances, control_instance, transportable, operating_modes):

    equipment = equipment_onto.StorageTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.CoolingSystem)
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.set_apparatus(equipment_onto.AtmosphericStorageTank)
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_piping(equipment_onto.TubeCoil)
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def cooled_storage_tank_2(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    
    equipment = equipment_onto.StorageTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.CoolingSystem)
    equipment_entity.set_apparatus(equipment_onto.AtmosphericStorageTank)
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_fixture(equipment_onto.TubeCoil)
    equipment_entity.add_instrumentation((equipment_onto.LevelIndicatorController, None))
    equipment_entity.add_connected_plant_item(equipment_onto.FlowControlValve)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def reactor(identifier, circumstances, control_instance, transportable, operating_modes):
    
    equipment = equipment_onto.ReactorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Reaction)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity