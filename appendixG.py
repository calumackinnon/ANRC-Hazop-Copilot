# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:08:24 2024

@author: qrb15201
"""

# ===Cause ========================================
class Cause(Thing):
    pass
Cause.label = ["cause"]
Cause.comment = ["Initiating event in the sequence of events of a scenario", "represents an event or situation"]
class UnderlyingCause(Thing):
    pass
UnderlyingCause.label = ["underlying cause"]
UnderlyingCause.comment = ["Underlying event in the sequence of events of a scenario",
 "represents ambient conditions, systemic and organizational causes, "
 "and causes arising from latent human errors"]
class causeInvolvesEquipmentEntity(Cause >> equipment_onto.EquipmentEntity):
    pass
class causeInvolvesSubstance(Cause >> substance_onto.Substance):
    pass
class underlyingcauseInvolvesEquipmentEntity(UnderlyingCause >> equipment_onto.EquipmentEntity):
    pass
class underlyingcauseInvolvesSubstance(UnderlyingCause >> substance_onto.Substance):
    pass
class isCauseOfDeviation(Cause >> deviation_onto.Deviation):
    pass
class causeInvolvesSecondDeviation(Cause >> deviation_onto.Deviation):
    pass
class isUnderlyingcauseOfCause(UnderlyingCause >> Cause):
    pass
class causeRequiresBoundaryCondition(Cause >> boundary_onto.BoundaryCondition):
    pass
class causeInvolvesSiteInformation(Cause >> site_information.AmbientInformation):
    pass
class underlyingcauseRequiresBoundaryCondition(UnderlyingCause >> boundary_onto.BoundaryCondition):
    pass
# === Effect ========================================
class Effect(Thing):
    pass
Effect.label = ["effect"]
Effect.comment = ["describe intermediate events that lie in the event sequence between"
 "the fault event (deviation) and hazardous event (consequence)"]
class effectInvolvesEquipmentEntity(Effect >> equipment_onto.EquipmentEntity):
 pass
class effectInvolvesSiteInformation(Effect >> site_information.AmbientInformation):
 pass
class isEffectOfDeviation(Effect >> deviation_onto.Deviation):
 pass
class effectInvolvesSecondDeviation(Effect >> deviation_onto.Deviation):
 pass
class effectInvolvesSubstance(Effect >> substance_onto.Substance):
 pass
class effectRequiresBoundaryCondition(Effect >> boundary_onto.BoundaryCondition):
 pass
class effectImpliedByCause(Effect >> causes_onto.Cause):
 pass
class effectOfPropagatedCause(Effect >> bool, FunctionalProperty):
 pass
class effectImpliedByUnderlyingcause(Effect >> causes_onto.UnderlyingCause):
 pass
# === Consequence ========================================
class Consequence(Thing):
 pass
Consequence.label = ["consequence"]
Consequence.comment = ["a consequence represents a hazardous event which is synonymous with a loss event"]
class consequenceInvolvesEquipmentEntity(Consequence >> equipment_onto.EquipmentEntity):
 pass
class consequenceInvolvesSubstance(Consequence >> substance_onto.Substance):
 pass
class isConsequenceOfDeviation(Consequence >> deviation_onto.Deviation):
 pass
class isConsequenceOfEffect(Consequence >> effect_onto.Effect):
 pass
class consequenceImpliedByCause(Consequence >> causes_onto.Cause):
 pass
class isSubsequentConsequence(Consequence >> Consequence, AsymmetricProperty):
 pass
class consequenceRequiresBoundaryCondition(Consequence >> boundary_onto.BoundaryCondition):
 pass

# === Safeguard ========================================
class Safeguard(Thing):
 pass
Safeguard.label = ["safeguard"]
Safeguard.comment = ["CCPS glossary: 'Any device, system, or action that interrupts the chain of events "
 "following an initiating event or that mitigates the consequences.'"]
class safeguardOfDeviation(Safeguard >> deviation_onto.Deviation):
 pass
class safeguardPreventsCause(Safeguard >> causes_onto.Cause):
 pass
class safeguardPreventsUnderlyingCause(Safeguard >> causes_onto.UnderlyingCause):
 pass
class safeguardMitigatesConsequence(Safeguard >> consequence_onto.Consequence):
 pass
class safeguardInvolvesSubstance(Safeguard >> substance_onto.Substance):
 pass
class safeguardPreventsEffect(Safeguard >> effect_onto.Effect):
 pass
class safeguardInvolvesEquipmentEntity(Safeguard >> equipment_onto.EquipmentEntity):
 pass
class safeguardInvolvesBoundaryCondition(Safeguard >> boundary_onto.BoundaryCondition):
 pass
class safeguardDependsOnRiskCategory(Safeguard >> risk_assessment_onto.RiskCategory):
 pass
class impliesSafeguard(Safeguard >> Safeguard, AsymmetricProperty):
 pass
# === Disjoint statement
AllDisjoint([deviation_onto.Deviation,
 causes_onto.Cause,
 causes_onto.UnderlyingCause,
 effect_onto.Effect,
 consequence_onto.Consequence,
 Safeguard,
 risk_assessment_onto.Likelihood,
 risk_assessment_onto.SeverityCategory,
 risk_assessment_onto.RiskCategory])
# === Deviation ========================================
class Deviation(Thing):
 pass
Deviation.label = ["deviation"]
Deviation.comment = ["describes (process) deviation from intention",
 "CCPS glossary: 'process condition outside of established design limits'",
"describes fault event in the sequence of events of a scenario"]
class hasGuideword(Deviation >> Guideword):
 pass
class hasParameter(Deviation >> Parameter):
 pass
