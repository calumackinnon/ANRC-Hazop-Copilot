# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:23:34 2024

@author: qrb15201
"""

class PumpBreakdown(Consequence):
 equivalent_to = [Consequence &
 ((isConsequenceOfEffect.some(effect_onto.IncreasedWear |
 effect_onto.Cavitation |
 effect_onto.PumpRunningDry))
 |
 # Because of this restriction DangerOfBleve and PumpBreakdown do not occur simulatenously
 (isConsequenceOfEffect.some(effect_onto.Overheating) & isConsequenceOfDeviation.some(deviation_onto.HighTemperature)))]
PumpBreakdown.comment = ["'Failure' when equipment condition reaches an unacceptable level but still operating",
 "'Breakdown' not functioning anymore",
"There is also specific definition of the concept in the compressor_onto"]
class CompressorBreakdown(Consequence):
 equivalent_to = [Consequence &
 (consequenceInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 isConsequenceOfEffect.some(effect_onto.Overheating | effect_onto.ExcessiveDischargeTemperature |
 effect_onto.IncreasedOilDischarge | effect_onto.LiquidSlugging))]
class ProductionDowntime(Consequence):
 equivalent_to = [Consequence &
 (isConsequenceOfEffect.some(effect_onto.CompressorNotOperating | effect_onto.PumpDeliversNoLiquid |
 effect_onto.InsufficientFilling | effect_onto.EmptyingOfContainer)
 |
 (isConsequenceOfDeviation.some(deviation_onto.NoFlow) & consequenceInvolvesEquipmentEntity.some(equipment_onto.SinkEntity))
 |
 ((isConsequenceOfDeviation.some(deviation_onto.LowLevel) &
 consequenceInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank | equipment_onto.PressureVessel))
 ) &
 isSubsequentConsequence.some(PumpBreakdown))
 |
 isSubsequentConsequence.some(PumpBreakdown | CompressorBreakdown)
 |
 (consequenceImpliedByCause.some(causes_onto.BlockedOutflowLine) &
 isConsequenceOfDeviation.some(deviation_onto.NoFlow) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity))
 |
 (consequenceImpliedByCause.some(causes_onto.LossOfInflow | causes_onto.ValveWronglyClosed |
 causes_onto.IncorrectFilling | causes_onto.ClosedInletValve) &
 isConsequenceOfEffect.some(effect_onto.EmptyingOfContainer))
 |
 (isConsequenceOfEffect.some(effect_onto.LossOfHeatTransfer) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity)))]
ProductionDowntime.comment = ["There is also specific definition of the concept in compressor_onto"]
class ReductionOfCoolingCapacity(Consequence):
 equivalent_to = [Consequence &
 (isConsequenceOfEffect.some(effect_onto.LossOfHeatTransfer) &
 consequenceInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)))]
class PROPAGATED_CONSEQUENCE(Consequence):
 equivalent_to = [Consequence &
 ((consequenceImpliedByCause.some(causes_onto.IncorrectSetPointControlValve | causes_onto.ConfusionOfSubstances |
 causes_onto.ValveWronglyOpened | causes_onto.InadvertentContamination | causes_onto.BypassOpened |
 causes_onto.ReducedFlowArea))
 |
 (consequenceImpliedByCause.some(causes_onto.ExcessiveInflow) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity))
 |
 (isConsequenceOfDeviation.some(deviation_onto.HighPressure | deviation_onto.LowFlow | deviation_onto.HighFlow |
 deviation_onto.NoFlow | deviation_onto.OtherThanComposition) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity))
 |
 (consequenceImpliedByCause.some(causes_onto.WrongTankLinedUp) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity))
 |
 (isConsequenceOfEffect.some(effect_onto.IncompleteEvaporation | effect_onto.AbnormalEvaporation) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))
 |
 (isConsequenceOfDeviation.some(deviation_onto.LowTemperature) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))
 |
 (isConsequenceOfDeviation.some(deviation_onto.HighPressure) & consequenceImpliedByCause.some(causes_onto.InternalLeakage))
 |
 (consequenceImpliedByCause.some(causes_onto.IncreasedInletPressure) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity))
 |
 (isConsequenceOfEffect.some(effect_onto.InsufficientInertization) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity))
 |
 (consequenceInvolvesEquipmentEntity.some(equipment_onto.hasPiping.some(equipment_onto.TankTruckHose)) &
 consequenceImpliedByCause.some(causes_onto.ContaminationInUnloadingLines))
 |
 (consequenceInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 consequenceImpliedByCause.some(causes_onto.PumpIncorrectlySet | causes_onto.WrongImpeller))
 |
 (consequenceInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity) &
 isConsequenceOfEffect.some(effect_onto.IncreasedHeatingCapacity))
 |
 (isConsequenceOfDeviation.some(deviation_onto.NoFlow) &
 consequenceImpliedByCause.some(causes_onto.ValveWronglyClosed | causes_onto.ValveIntactUnintentionallyClosed |
 causes_onto.ClosedInletValve | causes_onto.MissingImpeller |
 causes_onto.ImpellerFault | causes_onto.EntrainedAir))
 |
 (isConsequenceOfDeviation.some(deviation_onto.OtherThanComposition) &
 consequenceImpliedByCause.some(causes_onto.EntrainedAir))
 |
 (isConsequenceOfDeviation.some(deviation_onto.NoFlow | deviation_onto.LowFlow) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.SourceEntity | equipment_onto.ConnectionPipeEntity))
 |
 (isConsequenceOfDeviation.some(deviation_onto.HighPressure | deviation_onto.HighTemperature) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))
 |
 (isConsequenceOfDeviation.some(deviation_onto.NoFlow) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.ValveEntity) &
 consequenceImpliedByCause.some(causes_onto.WrongMountingOfNonReturnValve)))
 |
 (consequenceInvolvesEquipmentEntity.some(equipment_onto.SourceEntity) &
 isConsequenceOfDeviation.some(deviation_onto.OtherThanComposition) &
 consequenceImpliedByCause.some(causes_onto.InadvertentContamination |
 causes_onto.OtherSubstanceFromUpstream))
 ]



class PoorProductQuality(Consequence):
 equivalent_to = [Consequence &
 ((consequenceInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 consequenceInvolvesEquipmentEntity.some((equipment_onto.StorageTankEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.StabilizerColumnEntity |
 equipment_onto.DistillationColumnEntity |
 equipment_onto.PlateHeatExchangerEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 consequenceImpliedByCause.some(causes_onto.InadvertentContamination))
 |
 (isConsequenceOfEffect.some(effect_onto.BacteriaGrowth) &
 consequenceInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.Storing)))
 |
 (consequenceImpliedByCause.some(causes_onto.InadvertentContamination) &
 consequenceInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)))
 |
 (isConsequenceOfEffect.some(effect_onto.AccumulationOfImpurities) &
 consequenceInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.Filling |
 process_onto.ModeIndependent)))
 |
 (consequenceInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating)) &
 isConsequenceOfEffect.some(effect_onto.PoorSeparation))
 |
 (isConsequenceOfDeviation.some(deviation_onto.OtherThanComposition) &
 consequenceImpliedByCause.some(causes_onto.InternalLeakage))
 )]
class EmergenceOfIgnitionSource(Consequence):
 equivalent_to = [Consequence &
 isConsequenceOfEffect.some(effect_onto.GenerationOfElectrostaticCharge)]
class LossOfPrimaryContainment(Consequence):
 equivalent_to = [Consequence &
 ((isConsequenceOfEffect.some(effect_onto.FatigueFracture |
 effect_onto.Fracture |
 effect_onto.LossOfMechanicalIntegrity |
 effect_onto.PotentialViolentReactionWithOxidizers |
 effect_onto.BrittleFracture |
 effect_onto.DrainlineFracture |
 effect_onto.GasDispersion |
 effect_onto.PoolFormation)
 )
 |
 (isConsequenceOfEffect.some(effect_onto.Overfilling) &
 consequenceInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank))))
 ]
LossOfPrimaryContainment.comment = ["LOPC is defined in API Guide to Reporting Process Safety Events, Version 3.0"]
class FireHazard(Consequence):
 equivalent_to = [Consequence &
 (consequenceRequiresBoundaryCondition.some(boundary_onto.SufficientOxygenAvailable) &
 consequenceRequiresBoundaryCondition.some(boundary_onto.DirectIgnition) &
 isSubsequentConsequence.some(LossOfPrimaryContainment) &
 consequenceInvolvesSubstance.some(
 substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2 |
 substance_onto.FlammableLiquidCategory3
 )))]
class RiskOfExplosiveAtmosphere(Consequence):
 equivalent_to = [Consequence &
 (
 (consequenceRequiresBoundaryCondition.some(boundary_onto.LocatedOutside |
 boundary_onto.SufficientOxygenAvailable) &
 consequenceRequiresBoundaryCondition.some(boundary_onto.DelayedIgnition) &
 isSubsequentConsequence.some(LossOfPrimaryContainment) &
 consequenceInvolvesSubstance.some(
 substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2 |
 substance_onto.FlammableLiquidCategory3 |
 substance_onto.FlammableGasCategory1 |
 substance_onto.FlammableGasCategory2 |
 substance_onto.PyrophoricGasCategory1 |
 substance_onto.AerosolCategory1 |
 substance_onto.AerosolCategory2
 )
 ))
 |
 (consequenceRequiresBoundaryCondition.some(boundary_onto.LocatedOutside |
 boundary_onto.SufficientOxygenAvailable) &
 isSubsequentConsequence.some(LossOfPrimaryContainment) &
 consequenceRequiresBoundaryCondition.some(boundary_onto.DelayedIgnition) &
 consequenceInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.FormsExplosiveMixtureWithAir
 )))
 |
 (isConsequenceOfEffect.some(effect_onto.InsufficientInertization) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.AtmosphericStorageTank | equipment_onto.SettlingTankEntity) &
 consequenceRequiresBoundaryCondition.some(boundary_onto.IntroductionOfAir) &
 consequenceInvolvesSubstance.some(
 substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2 |
 substance_onto.FlammableLiquidCategory3 |
 substance_onto.FlammableGasCategory1 |
 substance_onto.FlammableGasCategory2 |
 substance_onto.PyrophoricGasCategory1 |
 substance_onto.AerosolCategory1 |
 substance_onto.AerosolCategory2)))
 |
 (consequenceImpliedByCause.some(causes_onto.InternalLeakage) &
 consequenceInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(substance_onto.FormsExplosiveMixturesWithOxidizingAgents))))]
RiskOfExplosiveAtmosphere.comment = ["Eindringen luft, und betriebsdruck kleiner umgebungsdruck",
 "https://www.ketopumps.com/media/1342/keto-green-paper-centrifugal-pump-explosions.pdf"]

class DangerOfBleve(Consequence):
 equivalent_to = [Consequence &
 (isConsequenceOfEffect.some(effect_onto.FluidCirculatesInsidePump) &
 consequenceImpliedByCause.some(causes_onto.DeadHeadingOfPump) &
 consequenceInvolvesEquipmentEntity.some(equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump)))]
DangerOfBleve.comment = ["physical explosion"]
class NoStabilization(consequence_onto.Consequence):
 equivalent_to = [consequence_onto.Consequence &
 consequence_onto.consequenceInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 consequence_onto.isConsequenceOfEffect.some(effect_onto.LossOfHeatTransfer)]
class PoorStripping(consequence_onto.Consequence):
 equivalent_to = [consequence_onto.Consequence & consequence_onto.isConsequenceOfEffect.some(ColumnFlooded)]
class PoorStabilization(consequence_onto.Consequence):
 equivalent_to = [consequence_onto.Consequence &
 (consequence_onto.consequenceInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 consequence_onto.isConsequenceOfEffect.some(effect_onto.ReducedHeatingCapacity |
 effect_onto.LossOfHeatTransfer |
 effect_onto.IncompleteEvaporation)
 )]
class ReductionOfCoolingCapacity(consequence_onto.Consequence):
 equivalent_to = [consequence_onto.Consequence &
 ((consequence_onto.isConsequenceOfEffect.some(LossOfHeatTransfer |
 IncompleteEvaporation) &
 consequence_onto.consequenceInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)))
 |
 (
 consequence_onto.consequenceInvolvesEquipmentEntity.some(equipment_onto.PressureReceiverEntity) &
 consequence_onto.consequenceInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)) &
 consequence_onto.isConsequenceOfEffect.some(effect_onto.AbnormalEvaporation))
 )] 

