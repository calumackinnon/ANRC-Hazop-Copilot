# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:10:27 2024

@author: qrb15201
"""

# === Guideword ========================================
class Guideword(Thing):
 pass
class More(Guideword):
 pass
class Less(Guideword):
 pass
class No(Guideword):
 pass
class PartOf(Guideword):
 pass
class AsWellAs(Guideword):
 pass
class WhereElse(Guideword):
 pass
class OtherThan(Guideword):
 pass
class Reverse(Guideword):
 pass
# === Parameters ========================================
class Parameter(Thing):
 pass
class Pressure(Parameter):
 pass
class Temperature(Parameter):
 pass
class Level(Parameter):
 pass
class Flow(Parameter):
 pass
class Material(Parameter):
 pass
class Vibration(Parameter):
 pass
class Composition(Parameter):
 pass
class Corrosion(Parameter):
 pass
class Time(Parameter):
 pass
# === Deviation ========================================
class Deviation(Thing):
 pass
Deviation.label = ["deviation"]
Deviation.comment = ["describes (process) deviation from intention", "CCPS glossary: 'process condition outside of established design limits'",
 "describes fault event in the sequence of events of a scenario"]
class hasGuideword(Deviation >> Guideword):
 pass
class hasParameter(Deviation >> Parameter):
 pass
class HighCorrosion(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(More) & hasParameter.some(Corrosion))]
HighCorrosion.label = ["high corrosion"]
class HighVibration(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(More) & hasParameter.some(Vibration))]
HighVibration.label = ["high vibration"]
class HighTemperature(Deviation):
 equivalent_to = [Deviation &
 (hasGuideword.some(More) & hasParameter.some(Temperature))]
HighTemperature.label = ["high temperature"]
class LowTemperature(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(Less) & hasParameter.some(Temperature))]
LowTemperature.label = ["low temperature"]
class HighPressure(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(More) & hasParameter.some(Pressure))]
HighPressure.label = ["high pressure"]
class LowPressure(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(Less) & hasParameter.some(Pressure))]
LowPressure.label = ["low pressure"]
class NoFlow(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(No) & hasParameter.some(Flow))]
NoFlow.label = ["no flow"]
class HighFlow(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(More) & hasParameter.some(Flow))]
HighFlow.label = ["high flow"]
class LowFlow(Deviation):
 equivalent_to = [Deviation & (hasGuideword.only(Less) & hasParameter.only(Flow))]
LowFlow.label = ["low flow"]
class ElsewhereFlow(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(WhereElse) & hasParameter.some(Flow))]
ElsewhereFlow.label = ["elsewhere flow"]
class ReverseFlow(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(Reverse) & hasParameter.some(Flow))]
ReverseFlow.label = ["reverse flow"]
class OtherSequence(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(OtherThan) & hasParameter.some(Time))]
OtherSequence.label = ["other sequence"]
# === Also used for contamination
class OtherThanComposition(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(OtherThan) & hasParameter.some(Composition))]
OtherThanComposition.comment = ["Used for 'Contamination', 'Changed concentration', 'Different phase' etc."]
OtherThanComposition.label = ["other than composition"]
class HighLevel(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(More) & hasParameter.some(Level))]
HighLevel.label = ["high level"]

class LowLevel(Deviation):
 equivalent_to = [Deviation & (hasGuideword.some(Less) & hasParameter.some(Level))]
LowLevel.label = ["low level"]
AllDisjoint([HighVibration, HighTemperature, HighCorrosion, LowTemperature, HighCorrosion, HighPressure,
 LowPressure, NoFlow, HighFlow, LowFlow, ElsewhereFlow, OtherSequence, ReverseFlow,
 OtherThanComposition, HighLevel, LowLevel])