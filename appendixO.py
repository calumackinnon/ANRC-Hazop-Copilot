# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:26:24 2024

@author: qrb15201
"""



class Likelihood(Thing):
 pass
class likelihoodInvolvesCause(Likelihood >> causes_onto.Cause):
 pass
class likelihoodInvolvesUnderlyingcause(Likelihood >> causes_onto.UnderlyingCause):
 pass
class likelihoodInvolvesEquipment(Likelihood >> equipment_onto.EquipmentEntity):
 pass
class likelihoodInvolvesDeviation(Likelihood >> deviation_onto.Deviation):
 pass
class likelihoodRequiresBoundaryCondition(Likelihood >> boundary_onto.BoundaryCondition):
 pass
class likelihoodInvolvesSiteInformation(Likelihood >> site_information.AmbientInformation):
 pass
class SeverityCategory(Thing):
 pass
class isSeverityOfConsequence(SeverityCategory >> consequence_onto.Consequence):
 pass
class severityInvolvesSubstance(SeverityCategory >> substance_onto.Substance):
 pass
class severityInvolvesEquipment(SeverityCategory >> equipment_onto.EquipmentEntity):
 pass
class severityRequiresBoundaryCondition(SeverityCategory >> boundary_onto.BoundaryCondition):
 pass
class RiskCategory(Thing):
 pass
class involvesSeverity(RiskCategory >> SeverityCategory):
 pass
class involvesLikelihood(RiskCategory >> Likelihood):
 pass
class VeryUnlikely(Likelihood):
 pass
VeryUnlikely.comment = ["corresponds to category F5", "10^-6 - 10^-4"]
class Unlikely(Likelihood):
 equivalent_to = [Likelihood &
 (
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.ValveFailure) &
 likelihoodInvolvesCause.some(causes_onto.ClosedInletValve))
 |
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.ValveFailure) &
 likelihoodInvolvesCause.some(causes_onto.ClosedOutletValve))
 |
 likelihoodInvolvesCause.some(causes_onto.BlockedOutflowLine)
 |
 (likelihoodInvolvesCause.some(causes_onto.MechanicalFailureOfSupport) &
 likelihoodInvolvesEquipment.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank)))
 |
 likelihoodInvolvesUnderlyingcause.some(causes_onto.AbnormallyHotIntake)
 |
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.SolarRadiation) &
 likelihoodInvolvesCause.some(causes_onto.ThermalExpansion |
 causes_onto.AbnormalHeatInput) &
 likelihoodInvolvesDeviation.some(deviation_onto.HighPressure) &
 likelihoodInvolvesEquipment.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel))))]
Unlikely.comment = ["corresponds to category F4", "10^-4 - 10^-3"]
class Possible(Likelihood):
 equivalent_to = [Likelihood &
 (
  (
     (likelihoodInvolvesEquipment.some(
     equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.ScrewCompressor | equipment_onto.PistonCompressor)) &
     likelihoodInvolvesCause.some(causes_onto.MalfunctionLubricationSystem))
     |
     (likelihoodInvolvesEquipment.some(
     equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.PistonCompressor | equipment_onto.ScrewCompressor |
     equipment_onto.CentrifugalPump | equipment_onto.ReciprocatingPump)) &
     likelihoodInvolvesDeviation.some(deviation_onto.HighTemperature))
     |
     (likelihoodInvolvesEquipment.some(
     equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump | equipment_onto.ReciprocatingPump)) &
     likelihoodInvolvesCause.some(causes_onto.DeadHeadingOfPump | causes_onto.OperationBelowMinimumFlowRate))
     |
     (likelihoodInvolvesCause.some(causes_onto.ExcessiveInflow | causes_onto.PumpIncorrectlySet) &
     likelihoodInvolvesEquipment.some(
     equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank | equipment_onto.PressureVessel |
     equipment_onto.OpenVessel)))
     |
     likelihoodInvolvesCause.some(causes_onto.PhysicalImpact | causes_onto.ControlValveFailsOpen | causes_onto.LossOfInflow |
     causes_onto.WrongTankLinedUp | causes_onto.LeakingDrainValve |
     causes_onto.ContaminationByWaterAndTemperatureFallsBelowFreezingPoint |
     causes_onto.PumpingAgainstPolymerizedLine)
     |
     (likelihoodInvolvesCause.some(causes_onto.MechanicalFailureOfSupport) &
     likelihoodInvolvesEquipment.some(equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank)) &
     likelihoodInvolvesSiteInformation.some(site_information.DangerOfSeismicActivity))
     |
     (likelihoodInvolvesDeviation.some(deviation_onto.HighCorrosion) &
     likelihoodInvolvesUnderlyingcause.some(causes_onto.CondensationAirHumidity) &
     likelihoodInvolvesEquipment.some(equipment_onto.StorageTankEntity))
     |
     (likelihoodInvolvesCause.some(causes_onto.BlockedInflowLine) &
     likelihoodInvolvesUnderlyingcause.some(causes_onto.DepositionOfImpurities))
     |
     (likelihoodInvolvesCause.some(causes_onto.ThermalExpansion) &
     likelihoodInvolvesUnderlyingcause.some(causes_onto.BlockedPipingAndHeatInput))
     |
     (likelihoodInvolvesCause.some(causes_onto.AbnormalHeatInput) &
     likelihoodInvolvesUnderlyingcause.some(causes_onto.SolarRadiation))
     |
     (likelihoodInvolvesDeviation.some(deviation_onto.OtherThanComposition) &
     likelihoodInvolvesCause.some(causes_onto.OtherSubstanceFromUpstream))
   )
  ]
Possible.comment = ["corresponds to category F3", "10^-3 - 10^-2"]



class Occasional(Likelihood):
 equivalent_to = [Likelihood &
 (likelihoodInvolvesCause.some(causes_onto.PumpSealFailure)
 |
 (likelihoodInvolvesEquipment.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank |
 equipment_onto.OpenVessel |
 equipment_onto.PressureVessel)) &
 likelihoodInvolvesCause.some(causes_onto.ExcessiveInflow |
 causes_onto.IncorrectIndicationOfFillingLevel))
 |
 (likelihoodInvolvesEquipment.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump)) &
 likelihoodInvolvesDeviation.some(deviation_onto.HighVibration))
 |
 (likelihoodInvolvesCause.some(causes_onto.WaterHammer) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.RapidlyClosingValve))
 |
 (likelihoodInvolvesEquipment.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump)) &
 likelihoodInvolvesCause.some(causes_onto.EntrainedAir |
 causes_onto.ImpellerFault))
 |
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.ExternalFire))
 |
 (likelihoodInvolvesCause.some(causes_onto.MissingImpeller) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.MaintenanceError))
 |
 (likelihoodInvolvesCause.some(causes_onto.PumpIncorrectlySet) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.OperationalError))
 |
 (likelihoodInvolvesEquipment.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump)) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.SuddenlyStoppingPump | causes_onto.SuddenStartingPump))
 |
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.CondensationAirHumidity) &
 likelihoodInvolvesCause.some(causes_onto.ContaminationByWater) &
 likelihoodInvolvesEquipment.some(equipment_onto.StorageTankEntity))
 |
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.LongStorageTimeOfStabilizer) &
 likelihoodInvolvesCause.some(causes_onto.TooLittleStabilizer))
 |
 likelihoodInvolvesCause.some(causes_onto.ValveIntactUnintentionallyClosed |
 causes_onto.InsufficientNPSH |
 causes_onto.ReducedDwellTime)
 |
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.OperationalError) &
 likelihoodInvolvesCause.some(causes_onto.DrainValveInadvertentlyOpened))
 |
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.OperationalError) &
 likelihoodInvolvesEquipment.some(equipment_onto.PumpEntity) &
 likelihoodInvolvesCause.some(causes_onto.ClosedInletValve))
 |
 (likelihoodInvolvesCause.some(causes_onto.ValveWronglyOpened) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.OperationalError))
 |
 likelihoodInvolvesCause.some(causes_onto.DeadHeadingOfPump)
 |
 (likelihoodInvolvesCause.some(causes_onto.InadvertentContamination) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.IntroductionOfRainwater | causes_onto.ContaminationInTankTruck))
 |
 likelihoodInvolvesCause.some(causes_onto.InadvertentContamination)
 |
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.IntroductionOfRainwater) &
 likelihoodInvolvesCause.some(causes_onto.ContaminationInUnloadingLines)))]
Occasional.comment = ["corresponds to category F2", "10^-2 - 10^-1"]
class Likely(Likelihood):
 equivalent_to = [Likelihood &
 ((likelihoodInvolvesCause.some(causes_onto.ExternalLeakage) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.HoseIncorrectlyConnected |
 causes_onto.BrokenHose |
 causes_onto.MaintenanceError |
 causes_onto.LossOfLeakTightness))
 |
 likelihoodInvolvesUnderlyingcause.some(causes_onto.FailureControlLoop |
 causes_onto.MalfunctionPressureController |
 causes_onto.PressureIndicatorControllerFailure |
 causes_onto.FlowIndicatorControllerFailure |
 causes_onto.MalfunctionFlowController |
 causes_onto.MalfunctionControlAir |
 causes_onto.LevelIndicatorControllerFailure |
 causes_onto.PowerFailure)
 |
 likelihoodInvolvesCause.some(causes_onto.NoInertgasSupply |
 causes_onto.ExcessiveFluidWithdrawal |
 causes_onto.PumpOperationFailure)
 |
 (likelihoodInvolvesCause.some(causes_onto.IncorrectSetPointControlValve) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.OperationalError))
 |
 (likelihoodInvolvesCause.some(causes_onto.ValveClosedPressureBuildUpInPiping) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.OperationalError))
 |
 (likelihoodInvolvesCause.some(causes_onto.ExcessiveInflow) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.OperationalError))
 |
 (likelihoodInvolvesCause.some(causes_onto.BypassOpened) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.OperationalError))
 |
 (likelihoodRequiresBoundaryCondition.some(boundary_onto.LocatedOutside) &
 likelihoodInvolvesUnderlyingcause.some(causes_onto.SolarRadiation) &
 likelihoodInvolvesEquipment.some(equipment_onto.StorageTankEntity) &
 likelihoodInvolvesCause.some(causes_onto.ThermalExpansion)))]
Likely.comment = ["corresponds to category F1", "10^-1 - 1^0"]
class VeryLikely(Likelihood):
 equivalent_to = [Likelihood &
 (
 (likelihoodInvolvesUnderlyingcause.some(causes_onto.AmbientTemperatureChange))
 |
 (likelihoodInvolvesCause.some(causes_onto.InsufficientThermalOutbreathing) &
 likelihoodInvolvesEquipment.some(equipment_onto.hasApparatus.some(
 equipment_onto.AtmosphericStorageTank)))
 |
 (likelihoodInvolvesCause.some(causes_onto.LiquidTransferWithoutCompensation) &
 likelihoodInvolvesEquipment.some(equipment_onto.hasApparatus.some(
 equipment_onto.AtmosphericStorageTank))))]
VeryLikely.comment = ["corresponds to category F0", "> 1 p.a."] 


class Catastrophic(SeverityCategory):
 equivalent_to = [SeverityCategory &
 ((isSeverityOfConsequence.some(consequence_onto.LossOfPrimaryContainment) &
 severityRequiresBoundaryCondition.some(
 boundary_onto.SeveralPeoplePresentInTheNearField))
 |
 (isSeverityOfConsequence.some(consequence_onto.LossOfPrimaryContainment) &
 severityRequiresBoundaryCondition.some(
 boundary_onto.SeveralPeoplePresentInTheNearField))
 |
 (isSeverityOfConsequence.some(consequence_onto.LossOfPrimaryContainment) &
 severityRequiresBoundaryCondition.some(
 boundary_onto.SeveralPeoplePresentInTheNearField) &
 severityInvolvesSubstance.some(substance_onto.hasHazardClass.some(
 substance_onto.PyrophoricGasCategory1))
 ))]
Catastrophic.comment = ["corresponds to category S0"]
class Severe(SeverityCategory):
 equivalent_to = [SeverityCategory &
 ((isSeverityOfConsequence.some(consequence_onto.DangerOfBleve) &
 severityInvolvesEquipment.some(equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump)) &
 severityRequiresBoundaryCondition.some(boundary_onto.PersonnelPresentInTheNearField))
 |
 (severityRequiresBoundaryCondition.some(boundary_onto.PersonnelPresentInTheNearField) &
 severityInvolvesSubstance.some(substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2)) &
 isSeverityOfConsequence.some(consequence_onto.LossOfPrimaryContainment))
 |
 (severityInvolvesEquipment.some(equipment_onto.StorageTankEntity) &
 severityRequiresBoundaryCondition.some(boundary_onto.PersonnelPresentInTheNearField) &
 isSeverityOfConsequence.some(consequence_onto.LossOfPrimaryContainment) &
 severityInvolvesSubstance.some(substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2)))
 |
 (severityRequiresBoundaryCondition.some(boundary_onto.PersonnelPresentInTheNearField) &
 isSeverityOfConsequence.some(consequence_onto.EmergenceOfIgnitionSource) &
 severityInvolvesSubstance.some(substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2
 )))
 |
 (isSeverityOfConsequence.some(consequence_onto.LossOfPrimaryContainment) &
 severityRequiresBoundaryCondition.some(boundary_onto.PersonnelPresentInTheNearField) &
 severityInvolvesSubstance.some(substance_onto.hasHazardClass.some(
 substance_onto.SpecificTargetOrganToxicitySingleExposureCategory1 |
 substance_onto.SpecificTargetOrganToxicityRepeatedExposureCategory1 |
 substance_onto.AspirationHazardCategory1 |
 substance_onto.ReproductiveToxicityCategory1 |
 substance_onto.SkinCorrosionIrritationCategory1
 )))
 |
 (severityRequiresBoundaryCondition.some(boundary_onto.PersonnelPresentInTheNearField) &
 isSeverityOfConsequence.some(consequence_onto.RiskOfExplosiveAtmosphere) &
 severityInvolvesSubstance.some(substance_onto.hasHazardClass.some(
 substance_onto.FlammableLiquidCategory1 |
 substance_onto.FlammableLiquidCategory2 |
 substance_onto.FlammableGasCategory1 |
 substance_onto.FlammableGasCategory2
 ))))]
Severe.comment = ["corresponds to category S1"]
class Serious(SeverityCategory):
 equivalent_to = [SeverityCategory &
 (isSeverityOfConsequence.some(consequence_onto.LossOfPrimaryContainment) &
 severityInvolvesSubstance.some(substance_onto.hasHazardClass.some(
 substance_onto.SpecificTargetOrganToxicitySingleExposureCategory3 |
 substance_onto.SpecificTargetOrganToxicityRepeatedExposureCategory2 |
 substance_onto.SpecificTargetOrganToxicitySingleExposureCategory2 |
 substance_onto.SpecificTargetOrganToxicityRepeatedExposureCategory3 |
 substance_onto.ReproductiveToxicityCategory2 |
 substance_onto.FlammableLiquidCategory3 |
 substance_onto.SkinCorrosionIrritationCategory2 |
 substance_onto.SkinCorrosionIrritationCategory3
 )))]
Serious.comment = ["corresponds to category S2"]
class Significant(SeverityCategory):
 pass
Significant.comment = ["corresponds to category S3"]
class Minor(SeverityCategory):
 equivalent_to = [SeverityCategory &
 (
 (isSeverityOfConsequence.some(consequence_onto.ProductionDowntime) |
 isSeverityOfConsequence.some(consequence_onto.PoorProductQuality) |
 isSeverityOfConsequence.some(consequence_onto.PumpBreakdown) |
 isSeverityOfConsequence.some(consequence_onto.CompressorBreakdown))
 )]
Minor.comment = ["corresponds to category S4"]

# === Risk category definitions
class A(RiskCategory):
 equivalent_to = [RiskCategory &
 ((involvesLikelihood.some(VeryLikely) &
 involvesSeverity.some(Catastrophic))
 |
 (involvesLikelihood.some(Likely) &
 involvesSeverity.some(Catastrophic))
 |
 (involvesLikelihood.some(VeryLikely) &
 involvesSeverity.some(Severe))
 )]
class B(RiskCategory):
 equivalent_to = [RiskCategory &
 ((involvesLikelihood.some(VeryLikely) &
 involvesSeverity.some(Serious))
 |
 (involvesLikelihood.some(VeryLikely) &
 involvesSeverity.some(Significant))
 |
 (involvesLikelihood.some(Likely) &
 involvesSeverity.some(Serious))
 |
 (involvesLikelihood.some(Likely) &
 involvesSeverity.some(Severe))
 |
 (involvesLikelihood.some(Occasional) &
 involvesSeverity.some(Serious))
 |
 (involvesLikelihood.some(Occasional) &
 involvesSeverity.some(Severe))
 |
 (involvesLikelihood.some(Occasional) &
 involvesSeverity.some(Catastrophic))
 |
 (involvesLikelihood.some(Possible) &
 involvesSeverity.some(Catastrophic))
 |
 (involvesLikelihood.some(Possible) &
 involvesSeverity.some(Severe))
 |
 (involvesLikelihood.some(Unlikely) &
 involvesSeverity.some(Catastrophic))
 )]
class C(RiskCategory):
 equivalent_to = [RiskCategory &
 ((involvesLikelihood.some(VeryLikely) &
 involvesSeverity.some(Minor))
 |
 (involvesLikelihood.some(Likely) &
 involvesSeverity.some(Minor))
 |
 (involvesLikelihood.some(Likely) &
 involvesSeverity.some(Significant))
 |
 (involvesLikelihood.some(Occasional) &
 involvesSeverity.some(Significant))
 |
 (involvesLikelihood.some(Possible) &
 involvesSeverity.some(Serious))
 |
 (involvesLikelihood.some(Unlikely) &
 involvesSeverity.some(Serious))
 |
 (involvesLikelihood.some(Unlikely) &
 involvesSeverity.some(Severe))
 |
 (involvesLikelihood.some(VeryUnlikely) &
 involvesSeverity.some(Catastrophic))
 |
 (involvesLikelihood.some(VeryUnlikely) &
 involvesSeverity.some(Severe))
 )]
class D(RiskCategory):
 equivalent_to = [RiskCategory &
 ((involvesLikelihood.some(Occasional) &
 involvesSeverity.some(Minor))
 |
 (involvesLikelihood.some(Possible) &
 involvesSeverity.some(Minor))
 |
 (involvesLikelihood.some(Possible) &
 involvesSeverity.some(Significant))
 |
 (involvesLikelihood.some(Unlikely) &
 involvesSeverity.some(Minor))
 |
 (involvesLikelihood.some(Unlikely) &
 involvesSeverity.some(Significant))
 |
 (involvesLikelihood.some(VeryUnlikely) &
 involvesSeverity.some(Serious))
 |
 (involvesLikelihood.some(VeryUnlikely) &
 involvesSeverity.some(Significant))
 |
 (involvesLikelihood.some(VeryUnlikely) &
 involvesSeverity.some(Minor))
 )] 



