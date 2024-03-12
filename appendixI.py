# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:11:24 2024

@author: qrb15201
"""


# === HIGHER-LEVEL STRUCTURE
class PlantItem(Thing):
 pass
class FunctionalPlantItem(PlantItem):
 pass
class StructuralPlantItem(PlantItem):
 pass
AllDisjoint([FunctionalPlantItem, StructuralPlantItem])
# === Ports
class Port(Thing):
 pass
class ConnectionType(Thing):
 pass
class Inlet(ConnectionType):
 pass
class Outlet(ConnectionType):
 pass
class hasConnectionType(Port >> ConnectionType, FunctionalProperty):
 pass
class hasName(Port >> str, FunctionalProperty):
 pass
class portEquippedWithInstrumentation(Port >> PlantItem, FunctionalProperty):
 pass
# === Control instance
class ControlInstance(Thing):
 pass
class Operator(ControlInstance):
 pass
class ProgrammableLogicController(ControlInstance):
 pass
class OperatorAndProcessControlSystem(ControlInstance):
 pass
class NotControlled(ControlInstance):
 pass
AllDisjoint([Operator, ProgrammableLogicController, NotControlled])
# === FailSafePosition
class FailSafePosition(Thing):
 pass
class FailOpen(FailSafePosition):
 pass
class FailClosed(FailSafePosition):
 pass
# === OperatingConditions
class OperationMode(Thing):
 pass
class NormalOperation(OperationMode):
 pass
class StartUpOperation(OperationMode):
 pass
class ShutDownOperation(OperationMode):
 pass
class Maintenance(OperationMode):
 pass
# === Piping
class Piping(StructuralPlantItem):
 pass
class Pipe(Piping):
 pass
class BlanketingGasline(Pipe):
 pass
class TubeCoil(Pipe):
 pass
class TubeBundle(Pipe):
 pass
class VentPipe(Pipe):
 pass
class TankTruckHose(Pipe):
 pass
class Fitting(Piping):
 pass
# === Material transfer equipment
class MaterialTransferEquipment(FunctionalPlantItem):
 pass
class Pump(MaterialTransferEquipment):
 pass
class Fan(MaterialTransferEquipment):
 pass
class CentrifugalPump(Pump):
 pass

class ReciprocatingPump(Pump):
 pass
ReciprocatingPump.comment = ["is a positive displacement pump"]
class VacuumPump(Pump):
 pass
class Compressor(MaterialTransferEquipment):
 pass
class ScrewCompressor(Compressor):
 pass
class PistonCompressor(Compressor):
 pass
PistonCompressor.comment = ["piston compressor", "positive-displacement compressor"]
# ==== APPARATUS
class Apparatus(StructuralPlantItem):
 pass
class NoApparatus(Apparatus):
 pass
class AtmosphericStorageTank(Apparatus):
 pass
class PressureVessel(Apparatus):
 pass
class OpenVessel(Apparatus):
 pass
OpenVessel.comment = ["e.g. cooling tower"]
class Casing(Apparatus):
 pass
class Body(Apparatus):
 pass
Body.comment = ["e.g. valve body"]
class PumpCasing(Casing):
 pass
class CompressorCasing(Casing):
 pass
# === INSTRUMENTATION
class Instrumentation(FunctionalPlantItem):
 pass
# Trivial case
class NoInstrumentation(Instrumentation):
 pass
class FrequencyConverter(Instrumentation):
 pass
FrequencyConverter.comment = ["speed control pump/compressor"]
class Controller(Instrumentation):
 pass
class SpeedController(Controller):
 pass
class LevelIndicatorController(Controller):
 pass
class QualityIndicatorController(Controller):
 pass
class LevelIndicator(Instrumentation):
 pass
class PressureIndicatorController(Controller):
 pass
class FlowIndicatorController(Controller):
 pass
class Transmitter(Instrumentation):
 pass
class MonitoringSystem(Instrumentation):
 pass
class Alarm(MonitoringSystem):
 pass
class HighLevelAlarm(MonitoringSystem):
 pass
class FlashingLight(MonitoringSystem):
 pass
class Actuator(Instrumentation):
 pass
class ElectricalActuator(Actuator):
 pass
class ElectricMotor(ElectricalActuator):
 pass
class Solenoid(ElectricalActuator):
 pass
class HydraulicActuator(Actuator):
 pass
class PneumaticActuator(Actuator):
 pass
class ManualActuator(Actuator):
 pass
# === FIXTURE
class Fixture(StructuralPlantItem):
 pass


class NoFixture(Fixture):
 pass
class Jacket(Fixture):
 pass
class Tray(Fixture):
 pass
class ChimneyTray(Fixture):
 pass
class LiquidDistributor(Fixture):
 pass
LiquidDistributor.comment = ["Used in Cooling tower or wet scrubber", "can be spray system etc."]
class PackedBed(Fixture):
 pass
PackedBed.comment = ["Fill / Package / Fill Material"]
class Baffle(Fixture):
 pass
class Basin(Fixture):
 pass
class PlatePackage(Fixture):
 pass
PlatePackage.comment = ["For plate heat exchanger"]
class HalfPipeCoilJacket(Fixture):
 pass
class FinnedCoil(Fixture):
 pass
class Impeller(Fixture):
 pass
class Stirrer(Fixture):
 pass
# === OPERATION RELATED EQUIPMENT
class Subunit(FunctionalPlantItem):
 pass
class SealingSystem(Subunit):
 pass
SealingSystem.comment = [
 "[Seals] is a generic term for 'mech. seals', 'gasket', 'shaft seal', 'rotary seal', 'o-ring seal', "
 "'liquid seal'", "gasket: between flat flanges"]
class LubricationSystem(Subunit):
 pass
class NoLubricationSystem(Subunit):
 pass
class CoolingSystem(Subunit):
 pass
class HeatingSystem(Subunit):
 pass
class Burner(Subunit):
 pass
class Bypass(Subunit):
 pass
class ElectricalEnergySupply(Subunit):
 pass
class CompressedAirSupply(Subunit):
 pass
class SteamSupply(Subunit):
 pass
class CondensateSeparator(Subunit):
 pass
class InertgasSupply(Subunit):
 pass
class PhysicalDevice(Instrumentation):
 pass
class FlowControlValve(PhysicalDevice):
 pass
class PressureControlValve(PhysicalDevice):
 pass
class NonReturnValve(PhysicalDevice):
 pass
class ApiAdaptorValve(PhysicalDevice):
 pass
comment = ["https://www.opwglobal.com/products/us/transportation-products/"
 "tank-truck-products/mechanical-tank-truck-products/"
 "bottom-loading-adapters-gravity-couplers-dust-caps/api-adaptors"]
class ShutOffValve(PhysicalDevice):
 pass
class BottomDrainValve(PhysicalDevice):
 pass
class ThreeWayValve(PhysicalDevice):
 pass
class ThrottlingValve(PhysicalDevice):
 pass
class InletValve(PhysicalDevice):
 pass
class OutletValve(PhysicalDevice):
 pass
class Orifice(PhysicalDevice):
 pass


class EquipmentEntity(Thing):
 pass
EquipmentEntity.comment = ["Process unit is composed of plant items (fixture, instrumentation, support system)",
 "has a nominal function and an operating state"]
class SourceEntity(EquipmentEntity):
 pass
class SinkEntity(EquipmentEntity):
 pass
class ConnectionPipeEntity(EquipmentEntity):
 pass
class TankTruckEntity(EquipmentEntity):
 pass
class StorageTankEntity(EquipmentEntity):
 pass
class SettlingTankEntity(EquipmentEntity):
 pass
class StabilizerColumnEntity(EquipmentEntity):
 pass
class DistillationColumnEntity(EquipmentEntity):
 pass
class SteamDrivenReboilerEntity(EquipmentEntity):
 pass
class PumpEntity(EquipmentEntity):
 pass
class CompressorEntity(EquipmentEntity):
 pass
class ValveEntity(EquipmentEntity):
 pass
class ReactorEntity(EquipmentEntity):
 pass
class WetScrubberEntity(EquipmentEntity):
 pass
class InertgasBlanketingEntity(EquipmentEntity):
 pass
# Pressure vessels
class PressureVesselEntity(EquipmentEntity):
 pass
class PressureReceiverEntity(PressureVesselEntity):
 pass
class SteamReceiverEntity(PressureVesselEntity):
 pass
class ShellTubeHeatExchangerEntity(EquipmentEntity):
 pass
class ShellTubeEvaporatorEntity(EquipmentEntity):
 pass
class PlateHeatExchangerEntity(EquipmentEntity):
 pass
class CoolingTowerEntity(EquipmentEntity):
 pass
class AirCooledCondenserEntity(EquipmentEntity):
 pass
class FinTubeEvaporatorEntity(EquipmentEntity):
 pass
# === Relations
class hasFixture(EquipmentEntity >> Fixture):
 pass
class isTransportable(EquipmentEntity >> bool, FunctionalProperty):
 pass
class hasConnectionToAdjacentPlantItem(EquipmentEntity >> PlantItem):
 pass
class hasInstrumentation(EquipmentEntity >> Instrumentation):
 pass
class hasFailSafePosition(EquipmentEntity >> FailSafePosition):
 pass
class hasMaterialTransferEquipment(EquipmentEntity >> MaterialTransferEquipment):
 pass
class hasSubunit(EquipmentEntity >> Subunit):
 pass
class hasApparatus(EquipmentEntity >> Apparatus):
 pass
class hasPiping(EquipmentEntity >> Piping):
 pass
class hasIdentifier(EquipmentEntity >> str):
 pass
class hasIntendedFunction(EquipmentEntity >> process_onto.IntendedFunction):
 pass
class hasMaximumOperatingPressureInBarGauge(EquipmentEntity >> float, FunctionalProperty):
 pass
class hasMaximumOperatingTemperatureInKelvin(EquipmentEntity >> float, FunctionalProperty):
 pass
class entityControlledBy(EquipmentEntity >> ControlInstance):
 pass
class hasOperationMode(EquipmentEntity >> OperationMode):
 pass
class formsControlLoopWith(Instrumentation >> Instrumentation):
 pass
class hasPort(EquipmentEntity >> Port):
 pass
class portEquippedWithInstrumentation(Port >> Instrumentation, FunctionalProperty):
 pass


# === Intended function
class IntendedFunction(Thing):
 pass
class NoIntendedFunction(IntendedFunction):
 pass
class Evaporating(IntendedFunction):
 pass
class Condensing(IntendedFunction):
 pass
class HeatTransferring(IntendedFunction):
 pass
class Mixing(IntendedFunction):
 pass
class Separating(IntendedFunction):
 pass
class MaterialTransfer(IntendedFunction):
 pass
class Stabilizing(IntendedFunction):
 pass
class FlowControl(IntendedFunction):
 pass
class PressureControl(IntendedFunction):
 pass
class Reacting(IntendedFunction):
 pass
class Purifying(IntendedFunction):
 pass
class Inerting(IntendedFunction):
 pass
class Transporting(IntendedFunction):
 pass
class Loading(IntendedFunction):
 pass
class Unloading(IntendedFunction):
 pass
class Emptying(IntendedFunction):
 pass
class Filling(IntendedFunction):
 pass
class Storing(IntendedFunction):
 pass
class ModeIndependent(IntendedFunction):
 pass
class DeliverConstantVolumeFlow(IntendedFunction):
 pass
