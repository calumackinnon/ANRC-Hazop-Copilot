# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:20:16 2024

@author: qrb15201
"""

class BackContaminationOfSupply(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 isEffectOfDeviation.some(deviation_onto.ReverseFlow)))]
class InsufficientFilling(Effect):
 equivalent_to = [Effect & (
 (effectImpliedByCause.some(causes_onto.BlockedInflowLine | causes_onto.LossOfInflow) &
 isEffectOfDeviation.some(deviation_onto.NoFlow | deviation_onto.LowLevel) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)))
 |
 (isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectOfPropagatedCause.value(True) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)))]
class UnintendedExothermicPolymerization(Effect):
 equivalent_to = [Effect &
 (
 (effectInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWithoutInhibitor) &
 effectImpliedByCause.some(causes_onto.TooLittleStabilizer |
 causes_onto.TooLittleInhibitor |
 causes_onto.InadvertentContamination) &
 effectInvolvesEquipmentEntity.some((equipment_onto.ConnectionPipeEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)
 )))
 |
 (effectInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWhenExposedToHeat)) &
 effectImpliedByCause.some(causes_onto.AbnormalHeatInput) &
 effectImpliedByUnderlyingcause.some(causes_onto.ExternalFire) &
 effectInvolvesEquipmentEntity.some((equipment_onto.ConnectionPipeEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent))
 )
 |
 (effectInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWithoutInhibitor)) &
 isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 effectImpliedByCause.some(causes_onto.TooLittleInhibitor)
 )
 )]
class PotentialViolentReactionWithOxidizers(Effect):
 equivalent_to = [Effect &
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.ReactsViolentlyWithOxidizer |
 substance_onto.IncompatibleToStrongOxidizers)) &
 isEffectOfDeviation.some(deviation_onto.OtherThanComposition) &
 effectImpliedByCause.some(causes_onto.WrongTankLinedUp |
 causes_onto.ConfusionOfSubstances))]
class AbnormalEvaporation(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase) &
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ) &
 effectImpliedByUnderlyingcause.some(causes_onto.ExternalFire) &
 isEffectOfDeviation.some(deviation_onto.HighTemperature))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling |
 process_onto.Storing)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectImpliedByCause.some(causes_onto.AbnormalHeatInput))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.PressureVessel &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling |
 process_onto.Storing)) &
 effectInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectImpliedByCause.some(causes_onto.AbnormalHeatInput))
 |
 (isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effectInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity) &
 effectImpliedByCause.some(causes_onto.MoreSteamFlow))
 |
 (effectImpliedByCause.some(causes_onto.DeliveryOfHighVolatilityComponents) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))
 )]


class AccumulationOfImpurities(Effect):
 equivalent_to = [Effect &
 (effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)) &
 effectImpliedByCause.some(causes_onto.ContaminationInUnloadingLines |
 causes_onto.InadvertentContamination) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectOfPropagatedCause.value(True) &
 isEffectOfDeviation.some(deviation_onto.OtherThanComposition))]
class BacteriaGrowth(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectImpliedByCause.some(causes_onto.ContaminationByWater) &
 isEffectOfDeviation.some(deviation_onto.OtherThanComposition)
 )
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 effectImpliedByCause.some(causes_onto.ContaminationInUnloadingLines |
 causes_onto.InadvertentContamination) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectOfPropagatedCause.value(True) &
 isEffectOfDeviation.some(deviation_onto.OtherThanComposition)))]
class GenerationOfElectrostaticCharge(Effect):
 equivalent_to = [Effect &
 (effectInvolvesEquipmentEntity.some((equipment_onto.TankTruckEntity |
 equipment_onto.ConnectionPipeEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading |
 process_onto.ModeIndependent)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isEffectOfDeviation.some(deviation_onto.HighFlow))]
class Overfilling(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isEffectOfDeviation.some(deviation_onto.HighLevel))
 |
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasPiping.some(equipment_onto.VentPipe) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling |
 process_onto.ModeIndependent)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isEffectOfDeviation.some(deviation_onto.HighLevel))
 |
 (isEffectOfDeviation.some(deviation_onto.HighFlow) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank |
 equipment_onto.OpenVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)) &
 effectImpliedByCause.some(causes_onto.BypassOpened |
 causes_onto.IncorrectSetPointControlValve |
 causes_onto.WrongImpeller |
 causes_onto.IncorrectFilling) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)))
 |
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank)) &
 effectImpliedByCause.some(causes_onto.IncorrectIndicationOfFillingLevel) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase))
 ))]

class PressureExceedingDesignPressure(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.HighPressure) &
 effectInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity |
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel)))
 |
 (effectInvolvesEquipmentEntity.some((equipment_onto.AirCooledCondenserEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.SteamDrivenReboilerEntity |
 equipment_onto.FinTubeEvaporatorEntity |
 equipment_onto.CompressorEntity) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 effectImpliedByCause.some(causes_onto.BlockedOutflowLine))
 |
 (effectOfPropagatedCause.value(True) &
 isEffectOfDeviation.some(deviation_onto.HighPressure) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling | process_onto.Storing | process_onto.ModeIndependent)))
 |
 (isEffectOfDeviation.some(deviation_onto.HighPressure) &
 effectImpliedByCause.some(causes_onto.ThermalExpansion | causes_onto.InsufficientThermalOutbreathing) &
 effectInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity |
 equipment_onto.hasApparatus.some(
 equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank)))
 |
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.ReciprocatingPump)) &
 effectImpliedByCause.some(causes_onto.DeadHeadingOfPump |
 causes_onto.PumpingAgainstPolymerizedLine))
 |
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl | process_onto.ModeIndependent)) &
 effectImpliedByCause.some(causes_onto.ValveClosedPressureBuildUpInPiping))
 |
 PotentialViolentReactionWithOxidizers)] 
 
 
 class Fracture(Effect):
 equivalent_to = [Effect &
 (
 (effectImpliedByCause.some(causes_onto.PhysicalImpact) &
 isEffectOfDeviation.some(deviation_onto.ElsewhereFlow) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))
 |
 PressureExceedingDesignPressure)]
class FatigueFracture(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.HighVibration) &
 effectImpliedByCause.some(causes_onto.MaterialDegradation))
 |
 (isEffectOfDeviation.some(deviation_onto.HighVibration) &
 effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity))
 |
 (isEffectOfDeviation.some(deviation_onto.HighVibration) &
 effectInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity)))]
class BrittleFracture(Effect):
 equivalent_to = [Effect &
 isEffectOfDeviation.some(deviation_onto.LowTemperature) &
 effectImpliedByCause.some(causes_onto.MaterialDegradation)]
BrittleFracture.comment = ["Source: Managing Cold Temperature and Brittle Fracture Hazards in Pressure "
 "Vessels by Daniel J. Benac, Nicholas Cherolis & David Wood",
 "Requires crack in high stress region",
"sudden and unexpected failure",
"https://www.psenterprise.com/sectors/oil-and-gas/brittle-fracture"]
class DrainlineFracture(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.OtherThanComposition) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 effectRequiresBoundaryCondition.some(
 boundary_onto.AmbientTemperatureCanDropBelowFreezingPoint))
 |
 (isEffectOfDeviation.some(deviation_onto.LowTemperature) &
 effectInvolvesSecondDeviation.some(deviation_onto.OtherThanComposition) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Multiphase |
 substance_onto.Liquid)) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.Storing | process_onto.ModeIndependent)))
 |
 (effectImpliedByCause.some(causes_onto.FreezeUp))
 |
 (isEffectOfDeviation.some(deviation_onto.LowTemperature) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve)) &
 effectRequiresBoundaryCondition.some(boundary_onto.IntroductionOfWater) &
 effectInvolvesSiteInformation.some(
 site_information.hasMinimumAmbientTemperatureInKelvin <= 273.15)))]
DrainlineFracture.comment = ["second part of definition accomplishes for double jeopardy, T_low and X_other"]
class InsufficientInertization(Effect):
 equivalent_to = [Effect &
 (effectInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity) &
 isEffectOfDeviation.some(deviation_onto.NoFlow |
 deviation_onto.OtherThanComposition) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.InertGas)))
 |
 (isEffectOfDeviation.some(deviation_onto.OtherThanComposition |
 deviation_onto.NoFlow) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasPiping.some(equipment_onto.BlanketingGasline) &
 equipment_onto.hasIntendedFunction.some(process_onto.Inerting)) &
 effectImpliedByCause.some(causes_onto.NoInertgasSupply |
 causes_onto.OtherSubstanceFromUpstream))]
class PoorSeparation(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.OtherThanComposition) &
 effectImpliedByCause.some(causes_onto.ConfusionOfSubstances |
 causes_onto.OtherSubstanceFromUpstream) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Separating)))
 |
 (isEffectOfDeviation.some(deviation_onto.OtherThanComposition) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectImpliedByCause.some(causes_onto.ReducedDwellTime) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Separating)))
 |
 (effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectImpliedByCause.some(causes_onto.BypassOpened |
 causes_onto.ValveWronglyOpened |
 causes_onto.IncorrectSetPointControlValve) &
 isEffectOfDeviation.some(deviation_onto.HighFlow) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating | process_onto.ModeIndependent)))
 )]
class PoolFormation(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 (effectImpliedByCause.some(causes_onto.ExternalLeakage |
 causes_onto.PumpSealFailure |
 causes_onto.DrainValveInadvertentlyOpened |
 causes_onto.HoseIncorrectlyConnected)))
 |
 (isEffectOfDeviation.some(deviation_onto.HighCorrosion) &
 effectOfPropagatedCause.value(True)))
 ] 
 
 
class EmptyingOfContainer(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Emptying)) &
 isEffectOfDeviation.some(deviation_onto.LowLevel | deviation_onto.NoFlow | deviation_onto.LowFlow) &
 effectImpliedByCause.some(causes_onto.LossOfInflow |
 causes_onto.IncorrectFilling |
 causes_onto.ClosedInletValve))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating)) &
 isEffectOfDeviation.some(deviation_onto.LowLevel | deviation_onto.NoFlow | deviation_onto.LowFlow) &
 effectImpliedByCause.some(causes_onto.LossOfInflow | causes_onto.ValveWronglyClosed |
 causes_onto.IncorrectFilling | causes_onto.ClosedInletValve))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Emptying)) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectOfPropagatedCause.value(True))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectOfPropagatedCause.value(True)))]
class LossOfMechanicalIntegrity(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ReactorEntity) &
 effectImpliedByCause.some(
 causes_onto.InsufficientThermalInbreathing |
 causes_onto.DrainValveInadvertentlyOpened))
 |
 (effectImpliedByCause.some(causes_onto.MechanicalFailureOfSupport) &
 isEffectOfDeviation.some(deviation_onto.ElsewhereFlow) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))
 |
 ((effectInvolvesEquipmentEntity.some((equipment_onto.StorageTankEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Emptying |
 process_onto.Storing))) &
 isEffectOfDeviation.some(deviation_onto.LowPressure))
 |
 ((effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating |
 process_onto.ModeIndependent))) &
 isEffectOfDeviation.some(deviation_onto.LowPressure)))]
LossOfMechanicalIntegrity.comment = ["Underpressure", "Armospheric Tank Failures: Mechanisms and an Unexpected Case Study"]
class GasDispersion(Effect):
 equivalent_to = [Effect &
 (effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 effectImpliedByCause.some(causes_onto.ExternalLeakage))]
class FluidCirculatesInsidePump(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow)) &
 effectImpliedByCause.some(causes_onto.PumpingAgainstPolymerizedLine |
 causes_onto.DeadHeadingOfPump))
 |
 (isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump) &
 equipment_onto.hasOperationMode.some(equipment_onto.StartUpOperation)) &
 effectImpliedByCause.some(causes_onto.WrongMountingOfNonReturnValve)))]
class Overheating(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 isEffectOfDeviation.some(deviation_onto.HighTemperature))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 effectImpliedByCause.some(causes_onto.MalfunctionLubricationSystem))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effectOfPropagatedCause.value(True))
 |
 FluidCirculatesInsidePump)]
class HeatBuildUp(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 effect_onto.effectImpliedByCause.some(BlockedReboilerLines)
 ]
class ColumnFlooded(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.isEffectOfDeviation.some(deviation_onto.HighLevel) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity))
 |
 (effect_onto.effectImpliedByCause.some(causes_onto.ExcessiveInflow) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity)
 ))]


class LiquidSlugging(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.PistonCompressor | equipment_onto.ScrewCompressor)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)) &
 (effect_onto.effectImpliedByCause.some(causes_onto.ContaminationByWater |
 causes_onto.OtherSubstanceFromUpstream)
 |
 effect_onto.isEffectOfDeviation.some(deviation_onto.OtherThanComposition)))]
LiquidSlugging.comment = ["Screw compressors have a higher tolerance to liquid slugging"]
class ExcessiveDischargeTemperature(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity))
 |
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 effect_onto.effectImpliedByCause.some(causes_onto.MalfunctionLubricationSystem)))]
class IncreasedOilDischarge(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighFlow) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity &
 equipment_onto.hasSubunit.some(equipment_onto.LubricationSystem))]
class IncompleteEvaporation(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((
 effect_onto.effectInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighFlow |
 deviation_onto.LowTemperature) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.FinTubeEvaporatorEntity |
 equipment_onto.ShellTubeEvaporatorEntity))
 |
 (effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.LowTemperature) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.ShellTubeEvaporatorEntity)))]
class IncompleteCondensation(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (
 effect_onto.effectInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighFlow |
 deviation_onto.HighTemperature) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity))]
class LossOfHeatTransfer(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.ShellTubeHeatExchangerEntity) &
 effect_onto.effectImpliedByCause.some(causes_onto.Fouling))
 |
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effect_onto.effectImpliedByCause.some(causes_onto.WrongRotatingSpeed |
 causes_onto.Fouling |
 causes_onto.HighAmbientTemperature |
 causes_onto.NonCondensables))
 |
 (effect_onto.effectImpliedByCause.some(NoSteamFlow)))]
class ReducedHeatingCapacity(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.LowTemperature))]
class IncreasedHeatingCapacity(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity) &
 effect_onto.effectImpliedByCause.some(causes_onto.MoreSteamFlow))]
class IncreasedWear(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 effect_onto.effectImpliedByCause.some(OperationBelowMinimumFlowRate)))]
class PumpRunningDry(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 effect_onto.effectImpliedByCause.some(causes_onto.ClosedInletValve |
 causes_onto.LossOfInflow |
 causes_onto.BlockedInflowLine)))]
PumpRunningDry.comment = [
 "https://www.worldpumps.com/operating-design/features/how-to-overcome-the-challenge-of-dry-running/"]
class PumpDeliversNoLiquid(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 effect_onto.effectImpliedByCause.some(causes_onto.MissingImpeller |
 causes_onto.EntrainedAir) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.NoFlow))
 ]
class Cavitation(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectImpliedByCause.some(InsufficientNPSH) &
 effect_onto.effectInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow)))
 |
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow)) &
 effect_onto.effectOfPropagatedCause.some(True) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighTemperature)))]
class PoorPumpPerformance(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectImpliedByCause.some(EntrainedAir | causes_onto.ImpellerFault) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.LowFlow))
 ]



class RunawayReaction(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.ReactorEntity) &
 (effect_onto.effectImpliedByCause.some(causes_onto.CoolingFailure |
 causes_onto.ConfusionOfSubstances |
 causes_onto.NoFeed |
 causes_onto.Pollution |
 ChargingFailure |
 DosingFailure
 ))
 |
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.ReactorEntity) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.ReverseFlow))
 ))]
class InsufficientAmountOfLiquidRefrigerant(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.isEffectOfDeviation.some(deviation_onto.OtherThanComposition |
 deviation_onto.LowLevel) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PressureReceiverEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.Refrigerant))
 )
 ]
class ScrubberAgentNotAvailable(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ScrubbingAgent)) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasFixture.some(
 equipment_onto.LiquidDistributor) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.NoFlow))
 |
 ((effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ScrubbingAgent)) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectImpliedByCause.some(LossOfInflow |
 BlockedInflowLine) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)))))
 ]
class InsufficientGasPurification(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.OtherThanComposition))
 ]
class FloodedPackedBed(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighLevel))
 ]
class AbnormalOperationCondition(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighTemperature |
 deviation_onto.LowTemperature |
 deviation_onto.LowPressure |
 deviation_onto.HighPressure |
 deviation_onto.HighFlow |
 deviation_onto.LowFlow |
 deviation_onto.HighLevel |
 deviation_onto.OtherThanComposition))
 ] 
