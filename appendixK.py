# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:15:53 2024

@author: qrb15201
"""

class UtilityFailure(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(NoInertgasSupply | NoSteamFlow)
 ]
class MalfunctionUpstreamProcess(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(DeliveryOfHighVolatilityComponents)
 ]
class IntroductionOfRainwater(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ContaminationInUnloadingLines) &
 underlyingcauseRequiresBoundaryCondition.some(boundary_onto.LocatedOutside))
 ]
class MalfunctionFlowController(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ExcessiveInflow |
 LossOfInflow) &
 underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) |
 equipment_onto.hasInstrumentation.some(
 equipment_onto.LevelIndicatorController |
 equipment_onto.FlowIndicatorController)))]
class MalfunctionPressureController(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(IncreasedInletPressure |
 IncorrectPressureAdjustment) &
 underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.PressureControlValve)))]
class AmbientTemperatureChange(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(InsufficientThermalInbreathing)]
class VehicleCollision(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(PhysicalImpact)]
class IncorrectCrossConnection(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(AbnormalVaporIntake)]
class ImproperProcessHeatInput(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ThermalExpansion) &
 underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasSubunit.some(equipment_onto.HeatingSystem)))]
class FastGasRelaxation(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(AbruptReliefOfContent)]
class ExternalFire(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 ((isUnderlyingcauseOfCause.some(AbnormalHeatInput) &
 underlyingcauseRequiresBoundaryCondition.some(boundary_onto.ExternalFirePossible))
 |
 (underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel)) &
 isUnderlyingcauseOfCause.some(ThermalExpansion) &
 underlyingcauseRequiresBoundaryCondition.some(boundary_onto.ExternalFirePossible)
 )
 |
 (isUnderlyingcauseOfCause.some(AbnormalHeatInput) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 underlyingcauseRequiresBoundaryCondition.some(boundary_onto.ExternalFirePossible)))
 ]
class SolarRadiation(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 ((isUnderlyingcauseOfCause.some(AbnormalHeatInput) &
 underlyingcauseInvolvesSubstance.some(
 (substance_onto.hasFlashpointInKelvin <= 348.15) &
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 underlyingcauseRequiresBoundaryCondition.some(boundary_onto.LocatedOutside))
 |
 (isUnderlyingcauseOfCause.some(InsufficientThermalOutbreathing) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 underlyingcauseRequiresBoundaryCondition.some(boundary_onto.LocatedOutside))
 )
 ]
SolarRadiation.comment = ["Assumption behind surface temperature of tank/vessel can rise to 75 °C, flash point is compared to it"]
class RapidlyClosingValve(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(WaterHammer) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity))
 ]
class BlockedPipingAndHeatInput(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ThermalExpansion) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity) &
 underlyingcauseRequiresBoundaryCondition.some(boundary_onto.ExternalFirePossible |
 boundary_onto.LocatedOutside)
 )
 ]
BlockedPipingAndHeatInput.comment = ["Requires external heat, therefore the boundary conditions"]
class AbnormallyHotIntake(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 ((isUnderlyingcauseOfCause.some(AbnormalHeatInput |
 ThermalExpansion) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.SteamReceiverEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ReactorEntity))
 |
 (isUnderlyingcauseOfCause.some(AbnormalHeatInput) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)))
 )] 
 
 
class DepositionOfImpurities(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(BlockedInflowLine |
 ReducedFlowArea)]
class LevelIndicatorControllerFailure(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ValveWronglyClosed |
 ValveWronglyOpened |
 IncorrectSetPointControlValve) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.LevelIndicatorController) |
 equipment_onto.hasConnectionToAdjacentPlantItem.some(equipment_onto.LevelIndicatorController)))]
class ControlValveFailsOpen(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ValveWronglyOpened) &
 underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve |
 equipment_onto.PressureControlValve)))
 ]
class ControlValveFailsClosed(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ValveWronglyClosed) &
 underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve |
 equipment_onto.PressureControlValve)))
 ]
class PressureIndicatorControllerFailure(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ValveWronglyClosed |
 ValveWronglyOpened |
 IncorrectPressureAdjustment |
 IncorrectSetPointControlValve) &
 underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.PressureIndicatorController) |
 equipment_onto.hasConnectionToAdjacentPlantItem.some(equipment_onto.PressureIndicatorController)))
 ]
class FlowIndicatorControllerFailure(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ValveWronglyClosed |
 ValveWronglyOpened |
 IncorrectSetPointControlValve) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity &
 (equipment_onto.hasInstrumentation.some(
 equipment_onto.PressureIndicatorController) |
equipment_onto.hasConnectionToAdjacentPlantItem.some(
 equipment_onto.PressureIndicatorController)))
 )]
class AbnormalHeatRemoval(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(FreezeUp)]
class LowAmbientTemperature(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (underlyingcauseRequiresBoundaryCondition.some(boundary_onto.LocatedOutside) &
 isUnderlyingcauseOfCause.some(FreezeUp))]
class DefectiveSeal(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.hasSubunit.some(equipment_onto.SealingSystem)) &
 isUnderlyingcauseOfCause.some(ExternalLeakage))]
DefectiveSeal.comment = ["Called 'seal failure' in Lees' Loss Prevention ... pp. 12/40"]
class DepositionOfImpurities(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(BlockedOutflowLine)]
class MechanicalDamage(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(EquipmentFailure |
 HeatInputByRecirculationPump)]
class WearDown(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(PumpSealFailure) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.PumpEntity))
 |
 (isUnderlyingcauseOfCause.some(InternalLeakage) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))
 ]
class LossOfLeakTightness(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(ExternalLeakage | LeakingDrainValve)
 ]
class SuddenStartingPump(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.ReciprocatingPump)) &
 isUnderlyingcauseOfCause.some(WaterHammer))]
class SuddenlyStoppingPump(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.ReciprocatingPump)) &
 isUnderlyingcauseOfCause.some(WaterHammer))]
class PowerFailure(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 ((underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.hasSubunit.some(equipment_onto.ElectricalEnergySupply)) &
 isUnderlyingcauseOfCause.some(EquipmentFailure))
 |
 (isUnderlyingcauseOfCause.some(WaterHammer) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.ValveEntity &
 equipment_onto.hasSubunit.some(equipment_onto.ElectricalEnergySupply))
 )
 |
 (isUnderlyingcauseOfCause.some(WaterHammer) &
 underlyingcauseInvolvesEquipmentEntity.some(
 (equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.ReciprocatingPump)) &
 equipment_onto.hasSubunit.some(equipment_onto.ElectricalEnergySupply))
 ))]
class MalfunctionSpeedControl(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.SpeedController)) &
 isUnderlyingcauseOfCause.some(WrongRotatingSpeed |
 EquipmentFailure))]
 
 
class BreakdownOfActuator(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.ElectricalActuator |
 equipment_onto.ManualActuator |
 equipment_onto.HydraulicActuator |
 equipment_onto.PneumaticActuator)) &
 (isUnderlyingcauseOfCause.some(EquipmentFailure)))]
class FailureControlLoop(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 ((underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.Controller) &
 equipment_onto.entityControlledBy.some(equipment_onto.ProgrammableLogicController)) &
 isUnderlyingcauseOfCause.some(EquipmentFailure |
 DeadHeadingOfPump))
 |
 (underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.Controller) &
 equipment_onto.entityControlledBy.some(equipment_onto.ProgrammableLogicController)) &
 isUnderlyingcauseOfCause.some(CoolingFailure))
 |
 isUnderlyingcauseOfCause.some(IncorrectIndicationOfFillingLevel)
 |
 isUnderlyingcauseOfCause.some(NoSteamFlow))]
class ValveFailure(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ClosedInletValve) |
 isUnderlyingcauseOfCause.some(ClosedOutletValve) |
 isUnderlyingcauseOfCause.some(OpenedInletValve) |
 isUnderlyingcauseOfCause.some(OpenedOutletValve))]
class MaintenanceError(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(WrongMountingOfNonReturnValve | LeakingDrainValve | MissingImpeller)]
class OperationalError(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 ((underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.entityControlledBy.some(equipment_onto.Operator)) &
 isUnderlyingcauseOfCause.some(ConfusionOfSubstances | WrongTankLinedUp))
 |
 ((isUnderlyingcauseOfCause.some(ClosedInletValve) |
 isUnderlyingcauseOfCause.some(ClosedOutletValve) |
 isUnderlyingcauseOfCause.some(OpenedInletValve) |
 isUnderlyingcauseOfCause.some(OpenedOutletValve) |
 isUnderlyingcauseOfCause.some(PumpIncorrectlySet) |
 isUnderlyingcauseOfCause.some(ValveClosedPressureBuildUpInPiping) |
 isUnderlyingcauseOfCause.some(ExcessiveInflow) |
 isUnderlyingcauseOfCause.some(DeadHeadingOfPump) |
 isUnderlyingcauseOfCause.some(ConnectionsFaultyConnected) |
 isUnderlyingcauseOfCause.some(BypassOpened) |
 isUnderlyingcauseOfCause.some(ValveWronglyClosed) |
 isUnderlyingcauseOfCause.some(ValveWronglyOpened) |
 isUnderlyingcauseOfCause.some(IncorrectFilling) |
 isUnderlyingcauseOfCause.some(ValveIntactUnintentionallyClosed) |
 isUnderlyingcauseOfCause.some(DrainValveInadvertentlyOpened) |
 isUnderlyingcauseOfCause.some(IncorrectSetPointControlValve)
 )))]
class ContaminationInTankTruck(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity) &
 isUnderlyingcauseOfCause.some(InadvertentContamination))]
class CondensationAirHumidity(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(ContaminationByWater) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Storing))]
class EntryDuringFilling(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(ContaminationByWater) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling))]
class LongStorageTimeOfStabilizer(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(TooLittleStabilizer)]
class PersistentMechanicalStresses(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 isUnderlyingcauseOfCause.some(MaterialDegradation)]
class HoseIncorrectlyConnected(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ExternalLeakage) &
 underlyingcauseInvolvesEquipmentEntity.some(
 equipment_onto.hasPiping.some(equipment_onto.TankTruckHose) &
 equipment_onto.entityControlledBy.some(equipment_onto.Operator)))]
class BrokenHose(UnderlyingCause):
 equivalent_to = [UnderlyingCause &
 (isUnderlyingcauseOfCause.some(ExternalLeakage) &
 underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.hasPiping.some(equipment_onto.TankTruckHose)))]
class MalfunctionOilTemperatureControl(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 causes_onto.isUnderlyingcauseOfCause.some(MalfunctionLubricationSystem)]
class FailureOilCoolingFan(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 causes_onto.isUnderlyingcauseOfCause.some(MalfunctionLubricationSystem)]
class CloggingOilCoolingLine(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 causes_onto.isUnderlyingcauseOfCause.some(MalfunctionLubricationSystem)]
class CloggingOilFilter(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 causes_onto.isUnderlyingcauseOfCause.some(MalfunctionLubricationSystem)]
class LowCompressorOilLevel(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 causes_onto.isUnderlyingcauseOfCause.some(MalfunctionLubricationSystem)]
class EntryOfForeignGases(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 (causes_onto.isUnderlyingcauseOfCause.some(causes_onto.NonCondensables) &
 causes_onto.underlyingcauseRequiresBoundaryCondition.some(boundary_onto.IntroductionOfAir))]
class Sediments(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 (causes_onto.isUnderlyingcauseOfCause.some(causes_onto.Fouling) &
 causes_onto.underlyingcauseRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities))]
 
 
class GrowthOfOrganisms(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 (causes_onto.isUnderlyingcauseOfCause.some(causes_onto.Fouling)
 )]
class MalfunctionControlAir(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 (causes_onto.isUnderlyingcauseOfCause.some(causes_onto.ValveWronglyClosed |
 causes_onto.ValveWronglyOpened |
 causes_onto.ValveClosedPressureBuildUpInPiping |
 FailureOfControlSystem) &
 causes_onto.underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.ValveEntity &
 equipment_onto.hasSubunit.some(equipment_onto.CompressedAirSupply) &
 equipment_onto.hasInstrumentation.some(equipment_onto.PneumaticActuator)))]
class WrongElectricSignal(causes_onto.UnderlyingCause):
 equivalent_to = [causes_onto.UnderlyingCause &
 (causes_onto.isUnderlyingcauseOfCause.some(causes_onto.ValveWronglyClosed |
 causes_onto.ValveWronglyOpened |
 causes_onto.ValveClosedPressureBuildUpInPiping |
 FailureOfControlSystem) &
 causes_onto.underlyingcauseInvolvesEquipmentEntity.some(equipment_onto.ValveEntity &
 equipment_onto.hasSubunit.some(equipment_onto.ElectricalEnergySupply) &
 equipment_onto.hasInstrumentation.some(equipment_onto.ElectricalActuator)
 ))] 
 
 

 