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


def shell_tube_heat_exchanger(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.ShellTubeHeatExchangerEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    # TODO: wieso nur 2 Anschlüsse
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_fixture(equipment_onto.Baffle)
    equipment_entity.add_piping(equipment_onto.TubeBundle)
    equipment_entity.set_intended_function(process_onto.HeatTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def reboiler(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.SteamDrivenReboilerEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_fixture(equipment_onto.Baffle)
    equipment_entity.add_piping(equipment_onto.TubeBundle)
    equipment_entity.add_subunit(equipment_onto.SteamSupply)
    equipment_entity.set_intended_function(process_onto.HeatTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity


def settling_tank(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume_of_enclosure):

    equipment = equipment_onto.SettlingTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    # equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_instrumentation((equipment_onto.LevelIndicatorController, None))
    equipment_entity.add_instrumentation((equipment_onto.PressureIndicatorController, None))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Separation)
    equipment_entity.assemble_ontology_object(equipment)
    equipment_entity.set_control_instance(control_instance)
    
    return equipment_entity

def inertgas_blanketing(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):

    equipment = equipment_onto.InertgasBlanketingEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.PressureControlValve, "{}-VA1".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.InertgasSupply)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.add_subunit(equipment_onto.NonReturnValve)
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_connected_plant_item(equipment_onto.PressureIndicatorController)
    equipment_entity.set_intended_function(process_onto.Inertization)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def pressure_vessel(identifier, circumstances, control_instance, transportable, operating_modes):

    equipment = equipment_onto.PressureVesselEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def pressure_receiver(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume):
    equipment = equipment_onto.PressureReceiverEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.set_volume_of_enclosure(volume)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def plate_heat_exchanger(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.PlateHeatExchangerEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.add_fixture(equipment_onto.PlatePackage)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.set_intended_function(process_onto.HeatTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def centrifugal_pump_1(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.PumpEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.set_material_transfer_equipment(equipment_onto.CentrifugalPump)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.set_apparatus(equipment_onto.PumpCasing)
    equipment_entity.set_intended_function(process_onto.MaterialTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity 


def centrifugal_pump_2(identifier,
    circumstances,
    control_instance,
    transportable,
    operating_modes,
    max_pressure,
    max_temperature,
    volume_flow):
    equipment = equipment_onto.PumpEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_volume_flow_of_transfer_equipment(volume_flow)
    equipment_entity.set_apparatus(equipment_onto.PumpCasing)
    equipment_entity.set_intended_function(process_onto.MaterialTransfer)
    equipment_entity.set_material_transfer_equipment(equipment_onto.CentrifugalPump)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.add_fixture(equipment_onto.Impeller)
    # equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.add_subunit(equipment_onto.NonReturnValve)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity
def screw_compressor(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume_flow):
    equipment = equipment_onto.CompressorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.add_subunit(equipment_onto.LubricationSystem)
    equipment_entity.set_material_transfer_equipment(equipment_onto.ScrewCompressor)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_apparatus(equipment_onto.CompressorCasing)
    equipment_entity.set_intended_function(process_onto.MaterialTransfer)
    equipment_entity.set_volume_flow_of_transfer_equipment(volume_flow)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity
def piston_compressor(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.CompressorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.add_subunit(equipment_onto.LubricationSystem)
    equipment_entity.set_material_transfer_equipment(equipment_onto.PistonCompressor)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_apparatus(equipment_onto.CompressorCasing)
    equipment_entity.set_intended_function(process_onto.MaterialTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def pneumatically_flow_control_valve_1(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.FluidControl)
    equipment_entity.add_instrumentation((equipment_onto.PneumaticActuator, None))
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.add_subunit(equipment_onto.CompressedAirSupply)
    equipment_entity.add_subunit(equipment_onto.Bypass)
    equipment_entity.add_instrumentation((equipment_onto.FlowControlValve, "{}-VA1".format(identifier)))
    equipment_entity.add_connected_plant_item(equipment_onto.LevelIndicatorController)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def pneumatically_pressure_control_valve_1(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.PressureControl)
    equipment_entity.add_instrumentation((equipment_onto.PneumaticActuator, None))
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.add_subunit(equipment_onto.CompressedAirSupply)
    equipment_entity.add_instrumentation((equipment_onto.PressureControlValve, "{}-VA1".format(identifier)))
    equipment_entity.add_connected_plant_item(equipment_onto.PressureIndicatorController)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def manual_three_way_valve(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.ThreeWayValve, "{}-VA1".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.FluidControl)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def throttling_valve(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.ThrottlingValve, "{}-VA1".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.FluidControl)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity 



def manual_valve(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.ShutOffValve, "{}-VA1".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.FluidControl)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity
def air_cooled_condenser(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.AirCooledCondenserEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.set_apparatus(equipment_onto.Casing)
    equipment_entity.add_fixture(equipment_onto.FinnedCoil)
    equipment_entity.set_material_transfer_equipment(equipment_onto.Fan)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_intended_function(process_onto.Condensation)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity
def shell_tube_evaporator(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume):
    equipment = equipment_onto.ShellTubeEvaporatorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_fixture(equipment_onto.Baffle)
    equipment_entity.add_fixture(equipment_onto.TubeBundle)
    equipment_entity.set_volume_of_enclosure(volume)
    equipment_entity.set_intended_function(process_onto.Evaporation)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity
def fin_tube_evaporator(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.FinTubeEvaporatorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.set_apparatus(equipment_onto.Casing)
    equipment_entity.add_fixture(equipment_onto.FinnedCoil)
    equipment_entity.set_material_transfer_equipment(equipment_onto.Fan)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_intended_function(process_onto.Evaporation)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def wet_scrubber(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.WetScrubberEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_fixture(equipment_onto.LiquidDistributor)
    equipment_entity.add_fixture(equipment_onto.PackedBed)
    equipment_entity.set_intended_function(process_onto.Purification)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def cooling_tower(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.CoolingTowerEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.set_apparatus(equipment_onto.OpenVessel)
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_fixture(equipment_onto.LiquidDistributor)
    equipment_entity.add_fixture(equipment_onto.PackedBed)
    equipment_entity.add_fixture(equipment_onto.Basin)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_intended_function(process_onto.HeatTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity

def crude_stabilizer_column(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.StabilizerColumnEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Stabilization)
    equipment_entity.add_fixture(equipment_onto.Tray)
    equipment_entity.add_fixture(equipment_onto.ChimneyTray)
    equipment_entity.add_instrumentation((equipment_onto.LevelIndicatorController, None))
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    return equipment_entity 
