# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:17:50 2024

@author: qrb15201
"""

class ReducedFlowArea(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity) &
 isCauseOfDeviation.some(deviation_onto.LowFlow))]
class HosePipeBlocked(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causeInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity &
 equipment_onto.hasPiping.some(equipment_onto.TankTruckHose)))]
class PhysicalImpact(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.ElsewhereFlow) &
 causeInvolvesSiteInformation.some(
 site_information.involvesPlantAmbientInformation.some(site_information.VehicleTraffic |
 site_information.CranePresent)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))]
class MechanicalFailureOfSupport(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.ElsewhereFlow) &
 causeRequiresBoundaryCondition.some(boundary_onto.FoundationCanBeAffected) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))]
class Pollution(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities) &
 causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank |
 equipment_onto.PressureVessel)))]
class NoFeed(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity |
 equipment_onto.ReactorEntity))]
class WrongMountingOfNonReturnValve(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.NonReturnValve))
 )]
# Unit tests conducted @200414 [TestFreezeUp] in unit_tests\overarching_phenomena.py
class FreezeUp(Cause):
 equivalent_to = [Cause &
 (causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid) &
 (substance_onto.hasFreezingPointInKelvin >= upper_onto.lowest_ambient_temperature)
 )
 &
 causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity) &
 isCauseOfDeviation.some(deviation_onto.LowTemperature))]
FreezeUp.comment = ["[FreezeUp] is seen as a cause for no flow.",
 "It can also be modeled as an [Effect] (T_low & pipe -> [FreezeUp])",
"The modelling is consequence-oriented, thus (T_low & pipe -> [PipeFracture])"]
class ValveClosedPressureBuildUpInPiping(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.ShutOffValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))
 |
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))
 |
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.PressureControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.PressureControl)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))]
class DrainValveInadvertentlyOpened(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow |
 equipment_onto.NormalOperation)) &
 causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow)))]
class LiquidTransferWithoutCompensation(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Emptying)) &
 causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.LowPressure))
 ]
class InsufficientThermalInbreathing(Cause):
 equivalent_to = [Cause &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 isCauseOfDeviation.some(deviation_onto.LowPressure)
 ]



class InsufficientThermalOutbreathing(Cause):
 equivalent_to = [Cause &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure)]
class NoInertgasSupply(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causeInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Inerting)) &
 causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.InertGas)))]
class IncreasedInletPressure(Cause):
 equivalent_to = [Cause &
 ((isCauseOfDeviation.some(deviation_onto.HighFlow) &
 causeInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Inerting)) &
 causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.InertGas))))]
class IncorrectPressureAdjustment(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.LowPressure) &
 causeInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent) &
 equipment_onto.hasPiping.some(equipment_onto.BlanketingGasline) &
 equipment_onto.hasInstrumentation.some(equipment_onto.PressureIndicatorController)))]
class BlockedOutflowLine(Cause):
 equivalent_to = [Cause &
 (
 (causeInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity |
 equipment_onto.AirCooledCondenserEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.FinTubeEvaporatorEntity) &
 isCauseOfDeviation.some(deviation_onto.NoFlow |
 deviation_onto.HighPressure))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 isCauseOfDeviation.some(deviation_onto.NoFlow |
 deviation_onto.HighPressure) &
 causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 isCauseOfDeviation.some(deviation_onto.HighLevel) &
 causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium))))]
class TooLittleStabilizer(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causeInvolvesEquipmentEntity.some((equipment_onto.ConnectionPipeEntity |
 equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.FinTubeEvaporatorEntity)) &
 causeRequiresBoundaryCondition.some(boundary_onto.SubstanceContainsStabilizer) &
 causeInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(substance_onto.PolymerizesExothermicallyWithoutInhibitor)))]
class TooLittleInhibitor(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causeInvolvesEquipmentEntity.some((equipment_onto.ConnectionPipeEntity |
 equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.FinTubeEvaporatorEntity)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(substance_onto.PolymerizesExothermicallyWithoutInhibitor)))]
class ExcessiveFluidWithdrawal(Cause):
 equivalent_to = [Cause &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 isCauseOfDeviation.some(deviation_onto.LowPressure)]
ExcessiveFluidWithdrawal.comment = ["The issue of depressurization and collapse of vessel is addressed",
 "https://www.aiche.org/resources/publications/cep/2019/december/protect-tanks-overpressure-and-vacuum",
"API 2000"]
class WaterHammer(Cause):
 equivalent_to = [Cause &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid) &
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure) &
 causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling |
 process_onto.ModeIndependent))]
WaterHammer.comment = ["Synonyms: hydraulic shock, fluid hammer"]
class ThermalExpansion(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase |
 substance_onto.Gaseous) &
substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causeRequiresBoundaryCondition.some(boundary_onto.ExternalFirePossible |
 boundary_onto.LocatedOutside) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))
 |
 (causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase |
 substance_onto.Gaseous) &
substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)
 ) &
 causeRequiresBoundaryCondition.some(boundary_onto.ExternalFirePossible |
 boundary_onto.LocatedOutside) &
 isCauseOfDeviation.some(deviation_onto.HighPressure)))]



class HighAmbientTemperature(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 isCauseOfDeviation.some(deviation_onto.HighTemperature |
 deviation_onto.HighPressure) &
 causeRequiresBoundaryCondition.some(boundary_onto.LocatedOutside))]
class WrongRotatingSpeed(Cause):
 equivalent_to = [Cause &
 (
 (isCauseOfDeviation.some(deviation_onto.HighFlow |
 deviation_onto.LowFlow) &
 causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)) &
 causeInvolvesEquipmentEntity.some((equipment_onto.CompressorEntity |
 equipment_onto.PumpEntity) &
 equipment_onto.hasInstrumentation.some(equipment_onto.FrequencyConverter) &
 equipment_onto.hasInstrumentation.some(equipment_onto.SpeedController) &
 equipment_onto.hasInstrumentation.some(equipment_onto.ElectricMotor)))
 |
 (isCauseOfDeviation.some(
 deviation_onto.HighPressure | deviation_onto.HighTemperature) &
 causeInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity &
 equipment_onto.hasInstrumentation.some(equipment_onto.ElectricMotor) &
 equipment_onto.hasInstrumentation.some(equipment_onto.SpeedController) &
 equipment_onto.hasInstrumentation.some(equipment_onto.FrequencyConverter))
 ))]
class ConfusionOfSubstances(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesEquipmentEntity.some(equipment_onto.SourceEntity &
 equipment_onto.entityControlledBy.some(equipment_onto.Operator)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition)))]
class WrongTankLinedUp(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))]
class OtherSubstanceFromUpstream(Cause):
 equivalent_to = [Cause &
 ((causeRequiresBoundaryCondition.some(boundary_onto.UpstreamProcessInvolved) &
 causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.SourceEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))
 |
 ((causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.InertGas)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Inerting)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))))]
class ReducedDwellTime(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causeInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating)))]
class ContaminationInUnloadingLines(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some((equipment_onto.hasPiping.some(
 equipment_onto.TankTruckHose)) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading)) &
 causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities |
 boundary_onto.IntroductionOfWater) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))]
class InadvertentContamination(Cause):
 equivalent_to = [Cause &
 ((causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities) &
 causeInvolvesEquipmentEntity.some((equipment_onto.SourceEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureReceiverEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))
 |
 (causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities) &
 causeInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition)))]
class ContaminationByWaterAndTemperatureFallsBelowFreezingPoint(Cause):
 equivalent_to = [Cause &
 (causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfWater) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(
 equipment_onto.AtmosphericStorageTank |
 equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing | process_onto.ModeIndependent)) &
 causeInvolvesSecondDeviation.some(deviation_onto.OtherThanComposition) &
 isCauseOfDeviation.some(deviation_onto.LowTemperature))]
class ContaminationByWater(Cause):
 equivalent_to = [Cause &
 ((causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfWater) &
 causeInvolvesEquipmentEntity.some((equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.FinTubeEvaporatorEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent |
 process_onto.Filling)
 ) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))
 |
 (causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfWater) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing |
 process_onto.Filling)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition)))]
 
 
class MaterialDegradation(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.HighVibration) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(
 equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank |
 equipment_onto.Piping)))]
class ExternalLeakage(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Gaseous)) & # liquid: because lubricant
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (isCauseOfDeviation.some(deviation_onto.HighCorrosion) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))
 |
 (causeInvolvesEquipmentEntity.some((equipment_onto.PressureReceiverEntity |
 equipment_onto.FinTubeEvaporatorEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.AirCooledCondenserEntity |
 equipment_onto.WetScrubberEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Gaseous |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve |
 equipment_onto.ThreeWayValve |
 equipment_onto.ShutOffValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Gaseous |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Gaseous |
 substance_onto.Multiphase) &
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow)))]
class InternalLeakage(Cause):
 equivalent_to = [Cause &
 ((isCauseOfDeviation.some(deviation_onto.ElsewhereFlow |
 deviation_onto.OtherThanComposition) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasFixture.some(equipment_onto.HalfPipeCoilJacket |
 equipment_onto.Jacket |
 equipment_onto.PlatePackage) |
 equipment_onto.hasPiping.some(equipment_onto.TubeCoil |
 equipment_onto.TubeBundle)))
 |
 (isCauseOfDeviation.some(deviation_onto.ElsewhereFlow) &
 causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity |
 equipment_onto.SteamDrivenReboilerEntity)))]
class ClosedOutletValve(Cause):
 equivalent_to = [Cause &
 (
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.OutletValve) &
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.OutletValve) &
 equipment_onto.hasApparatus.some(equipment_onto.Compressor)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 isCauseOfDeviation.some(deviation_onto.NoFlow | deviation_onto.HighPressure))))]
ClosedOutletValve.comment = ["Pump specific details are covered in pump ontology"]
class ClosedInletValve(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.InletValve) &
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank)) &
 causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 isCauseOfDeviation.some(deviation_onto.LowLevel | deviation_onto.NoFlow))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.InletValve) &
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 isCauseOfDeviation.some(deviation_onto.LowPressure))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity &
 equipment_onto.hasInstrumentation.some(equipment_onto.InletValve)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 isCauseOfDeviation.some(deviation_onto.NoFlow |
 deviation_onto.LowPressure))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasInstrumentation.some(equipment_onto.InletValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow)) &
 isCauseOfDeviation.some(deviation_onto.NoFlow)))]
ClosedInletValve.comment = ["Pump specific details are covered in pump ontology"] 



class LossOfCooling(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasSubunit.some(equipment_onto.CoolingSystem)) &
 isCauseOfDeviation.some(deviation_onto.HighTemperature))]
class DeliveryOfHighVolatilityComponents(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 causes_onto.causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)))]
class BlockedReboilerLines(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)))]
class MalfunctionLubricationSystem(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.Lubricant)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity &
 equipment_onto.hasSubunit.some(equipment_onto.LubricationSystem)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))]
MalfunctionLubricationSystem.comment = ["Issues described in 'How to limit fire and explosion hazards with oil-flooded rotary screw compressors' by
Steven J. Luzik"]
class InsufficientVentilation(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))]
class NoSteamFlow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))]
class LessSteamFlow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.LowFlow) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))]
class MoreSteamFlow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow) &
 causes_onto.causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))]
class NonCondensables(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 causes_onto.causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfAir) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition))]
NonCondensables.comment = ["Eigentlich wird hier noch high pressure benötigt"]
class Fouling(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 causes_onto.causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature |
 deviation_onto.OtherThanComposition)))]
class IncorrectSetPointControlValve(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow |
 deviation_onto.NoFlow |
 deviation_onto.LowFlow))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.PressureControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.PressureControl)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighPressure |
 deviation_onto.LowPressure)))]
class BypassOpened(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasSubunit.some(equipment_onto.Bypass) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow))
 ]
class ValveIntactUnintentionallyClosed(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some((equipment_onto.ValveEntity |
 equipment_onto.InertgasBlanketingEntity) &
 equipment_onto.hasInstrumentation.some(
 equipment_onto.FlowControlValve |
 equipment_onto.PressureControlValve |
 equipment_onto.ShutOffValve |
 equipment_onto.ThreeWayValve) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 (equipment_onto.hasInstrumentation.some(equipment_onto.OutletValve) |
 equipment_onto.hasInstrumentation.some(equipment_onto.InletValve)) &
 causes_onto.isCauseOfDeviation.some(
 deviation_onto.NoFlow |
 deviation_onto.HighTemperature))
 ))]


class ValveStuckOpen(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ValveEntity &
 equipment_onto.hasInstrumentation.some(
 equipment_onto.FlowControlValve |
 equipment_onto.PressureControlValve) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.FlowControl |
 process_onto.PressureControl)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel)))]
class ValvePartiallyOpened(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ValveEntity &
 equipment_onto.hasInstrumentation.some(
 equipment_onto.ShutOffValve)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowFlow))]
class PluggedRestrictionOrifice(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.Orifice) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow))]
class ValveWronglyClosed(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow))]
class ValveWronglyOpened(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl |
 process_onto.ModeIndependent)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow))]
class PumpingAgainstPolymerizedLine(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWhenExposedToLight |
 substance_onto.PolymerizesExothermicallyWhenExposedToHeat |
 substance_onto.PolymerizesExothermicallyWithoutInhibitor)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)))]
class ImpellerFault(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowFlow))]
class WrongImpeller(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow))]
class MissingImpeller(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasFixture.some(
 equipment_onto.Impeller) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow))]
class PumpOperationFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.ReverseFlow)))]
class PumpIncorrectlySet(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow)]
class OperationBelowMinimumFlowRate(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)
 ) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowFlow))]
class EntrainedAir(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfAir) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition))] 


class DeadHeadingOfPump(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasInstrumentation.some(
 equipment_onto.OutletValve) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow |
 equipment_onto.NormalOperation)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow)))]
DeadHeadingOfPump.comment = ["Occurs when the pump's discharge is closed (blockage or closed valve)"]
class InsufficientNPSH(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowPressure))]
class PumpSealFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.ElsewhereFlow)))]
class ChargingFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition |
 deviation_onto.OtherSequence) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ReactorEntity))]
class DosingFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition |
 deviation_onto.OtherSequence) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ReactorEntity))]
class AbnormalHeatInput(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some((equipment_onto.PressureVesselEntity |
 equipment_onto.PlateHeatExchangerEntity |
 equipment_onto.AirCooledCondenserEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ConnectionPipeEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent |
 process_onto.Storing)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling |
 process_onto.Storing)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasSubunit.some(equipment_onto.HeatingSystem)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature)))]
class LeakingDrainValve(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))]
class AbruptReliefOfContent(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity |
 equipment_onto.hasApparatus.some(
 equipment_onto.PressureVessel))) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowTemperature))]
AbruptReliefOfContent.comment = ["Abrupt relief can lead to ignition of flammable mixture"]
class CoolingFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasSubunit.some(equipment_onto.CoolingSystem)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))]
class BlockedInflowLine(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowPressure) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow | deviation_onto.LowFlow |
 deviation_onto.LowLevel | deviation_onto.LowPressure))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causes_onto.causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow)))]

class ExcessiveInflow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous |
 substance_onto.Multiphase |
 substance_onto.Liquid)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(
 substance_onto.Liquid | substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank |
 equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling))
 )
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Inerting)
 )
 )
 )
 ]
class LossOfInflow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)
 ))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ))
 )
 ]
class IncorrectIndicationOfFillingLevel(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)))
 )
 ]
class IncorrectFilling(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank) &
 equipment_onto.entityControlledBy.some(equipment_onto.Operator) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel |
 deviation_onto.HighLevel |
 deviation_onto.LowFlow |
 deviation_onto.HighFlow))]



