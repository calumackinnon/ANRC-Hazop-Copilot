# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:14:45 2024

@author: qrb15201
"""

class Substance(Thing):
 pass
class Property(Thing):
 pass
class StabilityReactivityInformation(Thing):
 pass
class hasStabilityReactivityInformation(Substance >> StabilityReactivityInformation):
 pass
class ReactsViolentlyWithOxidizer(StabilityReactivityInformation):
 pass
class FormsExplosiveMixtureWithAir(StabilityReactivityInformation):
 pass
class FormsExplosiveMixturesWithOxidizingAgents(StabilityReactivityInformation):
 pass
class ReactsWithWater(StabilityReactivityInformation):
 pass
class ReactsWithChlorates(StabilityReactivityInformation):
 pass
class PolymerizesExothermicallyWithoutInhibitor(StabilityReactivityInformation):
 pass
class PolymerizesExothermicallyWhenExposedToLight(StabilityReactivityInformation):
 pass
class PolymerizesExothermicallyWhenExposedToHeat(StabilityReactivityInformation):
 pass
class FormationOfHazardousDecompositionProducts(StabilityReactivityInformation):
 pass
class ThermalDecompositionGeneratesCorrosiveVapors(FormationOfHazardousDecompositionProducts):
 pass
class IncompatibleToStrongAcids(StabilityReactivityInformation):
 pass
class IncompatibleToStrongBases(StabilityReactivityInformation):
 pass
class IncompatibleToStrongOxidizers(StabilityReactivityInformation):
 pass
class SpecificSubstanceTask(Thing):
 pass
class hasSpecificTask(Substance >> SpecificSubstanceTask):
 pass
class ScrubbingAgent(SpecificSubstanceTask):
 pass
class Stabilizer(SpecificSubstanceTask):
 pass
Stabilizer.comment = ["chemical that is used to prevent degradation"]
class ReactionInhibitor(SpecificSubstanceTask):
 pass
ReactionInhibitor.comment = ["Substance that decreases or prevents chemical reaction"]
class Lubricant(SpecificSubstanceTask):
 pass
class Refrigerant(SpecificSubstanceTask):
 pass
class ProcessMedium(SpecificSubstanceTask):
 pass
class CoolingMedium(SpecificSubstanceTask):
 pass
class HeatingMedium(SpecificSubstanceTask):
 pass
class InertGas(SpecificSubstanceTask):
 pass
# Source 1: https://www.chemsafetypro.com/Topics/GHS/GHS_Classification_Criteria.html, Source 2: https://pubchem.ncbi.nlm.nih.gov/ghs/
class HazardClass(Thing):
 pass
class hasHazardClass(Substance >> HazardClass):
 pass
class PhysicalHazard(HazardClass):
 pass
class HealthHazard(HazardClass):
 pass
class EnvironmentalHazard(HazardClass):
 pass
class Explosives(PhysicalHazard):
 pass
class FlammableGases(PhysicalHazard):
 pass
class FlammableGasCategory1(FlammableGases):
 pass
class FlammableGasCategory2(FlammableGases):
 pass
class PyrophoricGasCategory1(FlammableGases):
 pass


class ChemicallyUnstableGasCategoryA(FlammableGases):
 pass
class ChemicallyUnstableGasCategoryB(FlammableGases):
 pass
class Aerosols(PhysicalHazard):
 pass
class AerosolCategory1(Aerosols):
 pass
class AerosolCategory2(Aerosols):
 pass
class OxidizingGases(PhysicalHazard):
 pass
class GasesUnderPressure(PhysicalHazard):
 pass
class CompressedGas(GasesUnderPressure):
 pass
class LiquefiedGas(GasesUnderPressure):
 pass
class RefrigeratedLiquefiedGas(GasesUnderPressure):
 pass
class DissolvedGas(GasesUnderPressure):
 pass
class FlammableLiquids(PhysicalHazard):
 pass
class FlammableLiquidCategory1(FlammableLiquids):
 pass
class FlammableLiquidCategory2(FlammableLiquids):
 pass
class FlammableLiquidCategory3(FlammableLiquids):
 pass
class FlammableLiquidCategory4(FlammableLiquids):
 pass
class FlammableSolids(PhysicalHazard):
 pass
class SelfReactiveSubstances(PhysicalHazard):
 pass
class PyrophoricLiquids(PhysicalHazard):
 pass
class PyrophoricSolids(PhysicalHazard):
 pass
class SelfHeatingSubstances(PhysicalHazard):
 pass
class EmitFlammableGasesWithWater(PhysicalHazard):
 pass
class OxidizingLiquids(PhysicalHazard):
 pass
class OxidizingSolids(PhysicalHazard):
 pass
class OrganicPeroxides(PhysicalHazard):
 pass
class CorrosiveToMetals(PhysicalHazard):
 pass
class DesensitiziedExplosives(PhysicalHazard):
 pass
class HazardousToAquaticEnvironment(EnvironmentalHazard):
 pass
class HazardousToAquaticEnvironmentLongTermCategory1(HazardousToAquaticEnvironment):
 pass
class HazardousToAquaticEnvironmentLongTermCategory2(HazardousToAquaticEnvironment):
 pass
class HazardousToAquaticEnvironmentLongTermCategory3(HazardousToAquaticEnvironment):
 pass
class HazardousToAquaticEnvironmentLongTermCategory4(HazardousToAquaticEnvironment):
 pass
class HazardousToAquaticEnvironmentAcuteCategory1(HazardousToAquaticEnvironment):
 pass
class HazardousToAquaticEnvironmentAcuteCategory2(HazardousToAquaticEnvironment):
 pass
class HazardousToAquaticEnvironmentAcuteCategory3(HazardousToAquaticEnvironment):
 pass
class HazardousToOzoneLayer(EnvironmentalHazard):
 pass
class AcuteToxicity(HealthHazard):
 pass
class AcuteToxicityCategory1(AcuteToxicity):
 pass
class AcuteToxicityCategory2(AcuteToxicity):
 pass
class AcuteToxicityCategory3(AcuteToxicity):
 pass

class SpecificTargetOrganToxicitySingleExposure(HealthHazard):
 pass
class SpecificTargetOrganToxicityRepeatedExposure(HealthHazard):
 pass
class SpecificTargetOrganToxicitySingleExposureCategory1(HealthHazard):
 pass
class SpecificTargetOrganToxicitySingleExposureCategory2(HealthHazard):
 pass
class SpecificTargetOrganToxicitySingleExposureCategory3(HealthHazard):
 pass
class SpecificTargetOrganToxicityRepeatedExposureCategory1(HealthHazard):
 pass
class SpecificTargetOrganToxicityRepeatedExposureCategory2(HealthHazard):
 pass
class SpecificTargetOrganToxicityRepeatedExposureCategory3(HealthHazard):
 pass
class SkinCorrosionIrritation(HealthHazard):
 pass
class SkinCorrosionIrritationCategory1(SkinCorrosionIrritation):
 pass
class SkinCorrosionIrritationCategory2(SkinCorrosionIrritation):
 pass
class SkinCorrosionIrritationCategory3(SkinCorrosionIrritation):
 pass
class SeriousEyeDamageIrritation(HealthHazard):
 pass
class SeriousEyeDamageIrritationCategory1(HealthHazard):
 pass
class SeriousEyeDamageIrritationCategory2A(HealthHazard):
 pass
class SeriousEyeDamageIrritationCategory2B(HealthHazard):
 pass
class RespiratoryOrSkinSensitization(HealthHazard):
 pass
class GermCellMutagenicity(HealthHazard):
 pass
class Carcinogenicity(HealthHazard):
 pass
class ReproductiveToxicology(HealthHazard):
 pass
class ReproductiveToxicityCategory1(HealthHazard):
 pass
class ReproductiveToxicityCategory2(HealthHazard):
 pass
class TargetOrganSystemicToxicitySingleExposure(HealthHazard):
 pass
class TargetOrganSystemicToxicityRepeatedExposure(HealthHazard):
 pass
class AspirationToxicity(HealthHazard):
 pass
class AspirationHazardCategory1(AspirationToxicity):
 pass
class AspirationHazardCategory2(AspirationToxicity):
 pass
class Flashpoint(Property):
 pass
Flashpoint.comment = ["Flammpunkt"]
class hasFlashpointInKelvin(Substance >> float, FunctionalProperty):
 pass
class hasFreezingPointInKelvin(Substance >> float, FunctionalProperty):
 pass
hasFreezingPointInKelvin.comment = ["Schmelztemperatur gleich groß wie Erstarrungstemperatur"]
class hasVaporPressureInPascal(Substance >> float, FunctionalProperty):
 pass
class hasUpperExplosionLimitInPercent(Substance >> float, FunctionalProperty):
 pass
class hasLowerExplosionLimitInPercent(Substance >> float, FunctionalProperty):
 pass
class hasAutoIgnitionTemperatureInKelvin(Substance >> float, FunctionalProperty):
 pass
class hasBoilingPointInKelvin(Substance >> float, FunctionalProperty):
 pass
class StateOfAggregation(Substance):
 pass
class Liquid(StateOfAggregation):
 pass
class Gaseous(StateOfAggregation):
 pass
class Multiphase(StateOfAggregation):
 pass
class hasStateOfAggregation(Substance >> StateOfAggregation):
 pass 




