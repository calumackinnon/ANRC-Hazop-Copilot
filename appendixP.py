# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:27:53 2024

@author: qrb15201
"""


class AddCorrosionInhibitor(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardOfDeviation.some(deviation_onto.HighCorrosion) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity))]
class OverFlowValveAndKickBackLine(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsEffect.some(effect_onto.FluidCirculatesInsidePump | effect_onto.Overheating)]
class ImplementQuickConnectSystem(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsCause.some(causes_onto.WrongTankLinedUp) &
 safeguardPreventsUnderlyingCause.some(causes_onto.OperationalError)]
class ImplementFrequentDrainingOff(Safeguard):
 equivalent_to = [Safeguard &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity) &
 safeguardPreventsEffect.some(effect_onto.PoorSeparation)]
class OverfillProtection(Safeguard):
 equivalent_to = [Safeguard &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.B | risk_assessment_onto.A) &
 safeguardPreventsEffect.some(effect_onto.Overfilling)]
class PressureReliefValve(Safeguard):
 equivalent_to = [Safeguard &
 ((safeguardInvolvesEquipmentEntity.some(equipment_onto.PressureVesselEntity | equipment_onto.PumpEntity |
 equipment_onto.ShellTubeHeatExchangerEntity) &
 safeguardPreventsEffect.some(effect_onto.Fracture))
 |
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.PressureVesselEntity |
 equipment_onto.CompressorEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.ShellTubeHeatExchangerEntity) &
 safeguardOfDeviation.some(deviation_onto.HighPressure))
 |
 (safeguardPreventsEffect.some(effect_onto.UnintendedExothermicPolymerization) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.PressureVesselEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.StorageTankEntity)))]
PressureReliefValve.comment = ["Must be certified for protecting pressure above 0.5 bar(g)"]
class AutomaticWaterDetectionSystem(Safeguard):
 equivalent_to = [Safeguard &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.A | risk_assessment_onto.B) &
 safeguardPreventsCause.some(causes_onto.ContaminationByWater)]
class ImplementVibrationDampener(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity | equipment_onto.CompressorEntity) &
 safeguardOfDeviation.some(deviation_onto.HighVibration))]
class ImplementNoFlowAlarm(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsEffect.some(effect_onto.InsufficientInertization) &
 safeguardPreventsCause.some(causes_onto.NoInertgasSupply | causes_onto.ValveIntactUnintentionallyClosed |
 causes_onto.ValveWronglyClosed) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.A | risk_assessment_onto.B)
 |
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 safeguardPreventsCause.some(causes_onto.MissingImpeller | causes_onto.DeadHeadingOfPump) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.A | risk_assessment_onto.B)))]
class ImplementNoFlowWarning(Safeguard):
 equivalent_to = [Safeguard &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 safeguardPreventsCause.some(causes_onto.MissingImpeller) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C | risk_assessment_onto.D)]
class PeriodicalSampleTaking(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsCause.some(causes_onto.ContaminationByWater |
 causes_onto.WrongTankLinedUp |
 causes_onto.InadvertentContamination |
 causes_onto.TooLittleStabilizer |
 causes_onto.TooLittleInhibitor)]
class PressureVacuumReliefValve(Safeguard):
 equivalent_to = [Safeguard &
 ((safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 safeguardPreventsEffect.some(effect_onto.LossOfMechanicalIntegrity))
 |
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank)) &
 safeguardPreventsCause.some(causes_onto.InsufficientThermalOutbreathing) &
 safeguardPreventsEffect.some(effect_onto.Fracture))
 |
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank)) &
 safeguardOfDeviation.some(deviation_onto.HighPressure) &
 safeguardPreventsEffect.some(effect_onto.Fracture)))]
PressureVacuumReliefValve.comment = ["also known as 'conservation vent valve'"]
class CollectingBasin(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardMitigatesConsequence.some(consequence_onto.LossOfPrimaryContainment) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.PressureVesselEntity | equipment_onto.PressureReceiverEntity))]
class ValveLockedClosed(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsCause.some(causes_onto.BypassOpened)
 |
 (safeguardPreventsCause.some(causes_onto.DrainValveInadvertentlyOpened) &
 safeguardPreventsEffect.some(effect_onto.PoolFormation)))]
class SwingCheckValve(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsCause.some(causes_onto.WaterHammer) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity))]
class SurgeReliefValve(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsCause.some(causes_onto.WaterHammer) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity |
 equipment_onto.PumpEntity))] 
 
 
class FlareSystem(Safeguard):
 equivalent_to = [Safeguard &
 safeguardInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel)) &
 impliesSafeguard.some(PressureReliefValve) &
 safeguardInvolvesSubstance.some(
 substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2 |
 substance_onto.FlammableLiquidCategory3 |
 substance_onto.FlammableGasCategory1 |
 substance_onto.FlammableGasCategory2 |
 substance_onto.PyrophoricGasCategory1 |
 substance_onto.AerosolCategory1 |
 substance_onto.AerosolCategory2
 ))]
class IncreaseClosingTimeOfValve(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsCause.some(causes_onto.WaterHammer)]
class PulsationDampener(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsCause.some(causes_onto.WaterHammer) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity))]
class ConsiderMaterialSelection(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsEffect.some(effect_onto.GenerationOfElectrostaticCharge) |
 safeguardOfDeviation.some(deviation_onto.HighCorrosion)]
class GasBalanceLine(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsCause.some(causes_onto.LiquidTransferWithoutCompensation) &
 safeguardInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank))]
class IncreaseSafetyIntegrityLevel(Safeguard):
 equivalent_to = [Safeguard &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C |
 risk_assessment_onto.B) &
 safeguardPreventsUnderlyingCause.some(causes_onto.LevelIndicatorControllerFailure)
 ]
class ThermalProtectionTrip(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity | equipment_onto.CompressorEntity) &
 (safeguardOfDeviation.some(deviation_onto.HighTemperature) |
 (safeguardPreventsEffect.some(effect_onto.Overheating |
 effect_onto.FluidCirculatesInsidePump))
 |
 (safeguardOfDeviation.some(deviation_onto.HighTemperature) &
 safeguardPreventsEffect.some(effect_onto.ExcessiveDischargeTemperature))))
 ]
class SoftStartStopControl(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 safeguardPreventsCause.some(causes_onto.WaterHammer))
 ]
class InstallHighLevelAlarm(Safeguard):
 equivalent_to = [Safeguard &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C |
 risk_assessment_onto.D) &
 safeguardPreventsEffect.some(effect_onto.Overfilling)]
class InstallHighTemperatureAlarm(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(
 equipment_onto.AtmosphericStorageTank |
 equipment_onto.PressureVessel)) &
 safeguardPreventsEffect.some(effect_onto.UnintendedExothermicPolymerization) &
 safeguardInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWhenExposedToHeat)))]
class ProvideLeakageMonitoring(Safeguard):
 equivalent_to = [Safeguard &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 safeguardPreventsEffect.some(effect_onto.PoolFormation)]
class ProvideAntiCorrosionCoating(Safeguard):
 equivalent_to = [Safeguard &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 safeguardOfDeviation.some(deviation_onto.HighCorrosion)]
class ImplementLowLevelAlarm(Safeguard):
 equivalent_to = [Safeguard &
 ((safeguardOfDeviation.some(deviation_onto.LowLevel) &
 safeguardInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank)) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.A | risk_assessment_onto.B))
 |
 (safeguardOfDeviation.some(deviation_onto.LowLevel) &
 safeguardPreventsCause.some(causes_onto.LossOfInflow |
 causes_onto.IncorrectFilling |
causes_onto.ClosedInletValve) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.A | risk_assessment_onto.B))
 |
 (safeguardPreventsEffect.some(effect_onto.EmptyingOfContainer) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.A | risk_assessment_onto.B)))]
class ImplementLowLevelWarning(Safeguard):
 equivalent_to = [Safeguard &
 ((safeguardOfDeviation.some(deviation_onto.LowLevel) &
 safeguardInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel | equipment_onto.AtmosphericStorageTank)) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C | risk_assessment_onto.D))
 |
 (safeguardOfDeviation.some(deviation_onto.LowLevel) &
 safeguardPreventsCause.some(causes_onto.LossOfInflow | causes_onto.IncorrectFilling | causes_onto.ClosedInletValve) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C | risk_assessment_onto.D))
 |
 (safeguardPreventsEffect.some(effect_onto.EmptyingOfContainer) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C | risk_assessment_onto.D)))
 ]
class ValveLockedOpen(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsCause.some(causes_onto.DeadHeadingOfPump | causes_onto.ClosedInletValve)]
 
 
class InstallPhysicalBarrierAroundTheEquipment(Safeguard):
 equivalent_to = [Safeguard &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 safeguardPreventsCause.some(causes_onto.PhysicalImpact)]
class InstallPressureLimitationValve(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsCause.some(causes_onto.IncorrectSetPointControlValve) &
 safeguardOfDeviation.some(deviation_onto.HighPressure))
 |
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity) &
 safeguardOfDeviation.some(deviation_onto.HighPressure))]
class InstallRestrictiveFlowOrifice(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsCause.some(causes_onto.ExcessiveInflow) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity))]
class InstallCheckValve(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardOfDeviation.some(deviation_onto.ReverseFlow)
 |
 (safeguardOfDeviation.some(deviation_onto.ElsewhereFlow) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity)))]
class QuenchSystem(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsEffect.some(effect_onto.UnintendedExothermicPolymerization) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.PressureVesselEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.ReactorEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.StorageTankEntity))]
class VacuumProofDesign(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.PressureReceiverEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity) &
 safeguardOfDeviation.some(deviation_onto.LowPressure) &
 safeguardPreventsEffect.some(effect_onto.LossOfMechanicalIntegrity) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.A | risk_assessment_onto.B))]
class HighPointVent(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 safeguardOfDeviation.some(deviation_onto.OtherThanComposition | deviation_onto.NoFlow | deviation_onto.LowFlow) &
 safeguardPreventsCause.some(causes_onto.EntrainedAir))]
class CheckIfFreeBlowOffPossible(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 safeguardOfDeviation.some(deviation_onto.OtherThanComposition | deviation_onto.NoFlow | deviation_onto.LowFlow) &
 safeguardPreventsCause.some(causes_onto.EntrainedAir))]
CheckIfFreeBlowOffPossible.comment = ["Depends directly on HighPointVent"]
class UseSealingCaps(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsCause.some(causes_onto.ContaminationInUnloadingLines)]
class DetermineSafetyRelatedOperatingInstructions(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsEffect.some(effect_onto.PotentialViolentReactionWithOxidizers)
 |
 safeguardPreventsUnderlyingCause.some(causes_onto.HoseIncorrectlyConnected |
 causes_onto.IncorrectSetPointControlValve |
 causes_onto.IncorrectPressureAdjustment))]
class EmergencyPressureReliefValve(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsEffect.some(effect_onto.Fracture) &
 safeguardPreventsUnderlyingCause.some(causes_onto.ExternalFire) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(
 equipment_onto.AtmosphericStorageTank |
 equipment_onto.OpenVessel)))]
EmergencyPressureReliefValve = ["Located on low pressure storage tanks"]
class AddStabilizer(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsEffect.some(effect_onto.UnintendedExothermicPolymerization)]
class FailsafeFeedStop(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsEffect.some(effect_onto.InsufficientInertization)]
class FlameArrestor(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity) &
 safeguardMitigatesConsequence.some(consequence_onto.RiskOfExplosiveAtmosphere) &
 safeguardInvolvesSubstance.some(substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2 |
 substance_onto.FlammableLiquidCategory3)))]
FlameArrestor.comment = [
 "methanol tank, should be protected with flame arrestor and nitrogen blanketing (more than 3000 m³, API2000)"]
class RegularPlantInspection(Safeguard):
 equivalent_to = [Safeguard &
 ((safeguardPreventsCause.some(causes_onto.ExternalLeakage) | safeguardPreventsEffect.some(effect_onto.PoolFormation))
 |
 safeguardMitigatesConsequence.some(consequence_onto.LossOfPrimaryContainment))
 ]
class ElaborationOfMaintenanceConcept(Safeguard):
 equivalent_to = [Safeguard &
 ((safeguardPreventsCause.some(causes_onto.PumpSealFailure) & safeguardPreventsEffect.some(effect_onto.PoolFormation))
 |
 (safeguardPreventsUnderlyingCause.some(causes_onto.LossOfLeakTightness | causes_onto.BrokenHose) &
 safeguardPreventsCause.some(causes_onto.ExternalLeakage))
 |
 (safeguardPreventsUnderlyingCause.some(causes_onto.ControlValveFailsClosed |
 causes_onto.ControlValveFailsOpen) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C | risk_assessment_onto.D))
 )]
class LimitationOfTheFlowVelocity(Safeguard):
 equivalent_to = [Safeguard &
 safeguardPreventsEffect.some(effect_onto.GenerationOfElectrostaticCharge)
 ] 


class ConsiderMinimumTankDistance(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 safeguardMitigatesConsequence.some(consequence_onto.LossOfPrimaryContainment) &
 safeguardPreventsEffect.some(effect_onto.LossOfMechanicalIntegrity | effect_onto.Fracture) &
 safeguardInvolvesSubstance.some(substance_onto.hasFlashpointInKelvin <= 273.15 + 55.0))]
ConsiderMinimumTankDistance.comment = ["TRGS 509, pp. 37, <= 55 °C"]
class CheckPressureClassPiping(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsEffect.some(effect_onto.Fracture) &
 safeguardInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity | equipment_onto.ValveEntity) &
 safeguardOfDeviation.some(deviation_onto.HighPressure))]
class UseNormallyOpenValve(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsCause.some(causes_onto.ValveWronglyClosed) & safeguardPreventsEffect.some(effect_onto.EmptyingOfContainer))]
class AvoidingBlockedLiquids(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity) &
 safeguardPreventsCause.some(causes_onto.AbnormalHeatInput))]
class InstallHeatTracingSystem(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsEffect.some(effect_onto.DrainlineFracture) &
 safeguardPreventsCause.some(causes_onto.ContaminationByWaterAndTemperatureFallsBelowFreezingPoint))]
class InstallThermalExpansionReliefValve(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsEffect.some(effect_onto.PressureExceedingDesignPressure) &
 safeguardPreventsCause.some(causes_onto.ThermalExpansion) &
 safeguardPreventsUnderlyingCause.some(causes_onto.BlockedPipingAndHeatInput))]
class StandardOperationProcedure(Safeguard):
 equivalent_to = [Safeguard &
 (safeguardPreventsCause.some(causes_onto.DrainValveInadvertentlyOpened | causes_onto.OperationBelowMinimumFlowRate)
 |
 (safeguardPreventsUnderlyingCause.some(causes_onto.OperationalError) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C | risk_assessment_onto.D))
 |
 (safeguardPreventsUnderlyingCause.some(causes_onto.MaintenanceError) &
 safeguardDependsOnRiskCategory.some(risk_assessment_onto.C | risk_assessment_onto.D)))]
class ProvideGroundingOfPlant(Safeguard):
 equivalent_to = [Safeguard & safeguardPreventsEffect.some(effect_onto.GenerationOfElectrostaticCharge)]
class PeriodicInspection(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard & safeguard_onto.safeguardPreventsCause.some(MalfunctionLubricationSystem)]
class ImprovedOilSeparation(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard & safeguard_onto.safeguardPreventsEffect.some(IncreasedOilDischarge)]
class QuickActionStopValve(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 safeguard_onto.safeguardInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 safeguard_onto.safeguardOfDeviation.some(deviation_onto.ElsewhereFlow)
 ]
class PurgerUnit(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 safeguard_onto.safeguardPreventsCause.some(causes_onto.NonCondensables)]
class OverflowValve(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 ((safeguard_onto.safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity |
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump |
 equipment_onto.ReciprocatingPump)))
 & safeguard_onto.safeguardPreventsEffect.some(effect_onto.FluidCirculatesInsidePump) &
 safeguard_onto.safeguardPreventsCause.some(DeadHeadingOfPump | causes_onto.ValveIntactUnintentionallyClosed))]
class MinimumFlowProtectionSystem(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardPreventsCause.some(OperationBelowMinimumFlowRate) &
 safeguard_onto.safeguardDependsOnRiskCategory.some(risk_assessment_onto.A | risk_assessment_onto.B) &
 safeguard_onto.safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity))]
MinimumFlowProtectionSystem.comment = ["e.g. continues bypass, automatic recirculation valve"]
class LowFlowProtectionTrip(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardPreventsCause.some(OperationBelowMinimumFlowRate) &
 safeguard_onto.safeguardOfDeviation.some(deviation_onto.LowFlow))]
class DryRunProtection(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 safeguard_onto.safeguardPreventsEffect.some(PumpRunningDry))]
class InstallPumpInducer(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardPreventsEffect.some(Cavitation) &
 safeguard_onto.safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity))]
class IncreaseSuctionPressure(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardPreventsEffect.some(Cavitation) &
 safeguard_onto.safeguardPreventsCause.some(InsufficientNPSH) &
 safeguard_onto.safeguardInvolvesEquipmentEntity.some(equipment_onto.PumpEntity))]
class DefineMaximumFillLevel(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 safeguard_onto.safeguardPreventsEffect.some(effect_onto.Overfilling))]
class TemperatureControllerHighAlarm(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardPreventsCause.some(causes_onto.AbnormallyHotIntake | CoolingFailure) &
 safeguard_onto.safeguardOfDeviation.some(deviation_onto.HighTemperature))]
class EmergencyCooling(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardPreventsCause.some(CoolingFailure) &
 safeguard_onto.safeguardOfDeviation.some(deviation_onto.HighTemperature))]
class EmergencyStabilization(safeguard_onto.Safeguard):
 equivalent_to = [safeguard_onto.Safeguard &
 (safeguard_onto.safeguardInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.ReactorEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.PressureReceiverEntity) &
 safeguard_onto.safeguardPreventsEffect.some(effect_onto.UnintendedExothermicPolymerization))]
 
 
