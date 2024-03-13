# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:30:15 2024

@author: qrb15201
"""

def equipment_based_hazard_specific_deviation(deviation, args):
    # === Input
    process_unit = args[0]
    substance = args[1]
    environment = args[2]
    subsequent_deviation_loop = args[3]
    subsequent_deviations = args[4]
    stack_elements = args[5]
    # === Loop over causes =====================================================================================
    preliminary_scenario_list = []
    extended_scenarion_list = []
    cause_list = None
    cause = None
    likelihood_ = None
    underlying_cause_ = None
    if not subsequent_deviation_loop:
        # = Cause =========================================================================================
        # =================================================================================================
        deviation1, deviation2 = assemble_deviation(deviation)
        cause = causes_onto.Cause(isCauseOfDeviation=deviation1,
                causeInvolvesSecondDeviation=deviation2,
                causeInvolvesEquipmentEntity=[process_unit.onto_object],
                causeRequiresBoundaryCondition=process_unit.boundary_condition,
                causeInvolvesSiteInformation=[environment.onto_object],
                causeInvolvesSubstance=[substance.onto_object]
            ) # functional, nur 1 substanz übergeben
        sync_reasoner(debug=0)
    else:
        if isinstance(deviation, dict):
            if isinstance(deviation[prep.DictName.subsequent_deviation], str):
                cause_list = deviation[prep.DictName.explanation]
                underlying_cause_ = deviation[prep.DictName.underlying_cause]()
                likelihood_ = deviation[prep.DictName.likelihood]()
                deviation = [upper_onto.pse_onto[deviation[prep.DictName.subsequent_deviation]]()]
            else:
                cause_list = deviation[prep.DictName.explanation]
                underlying_cause_ = deviation[prep.DictName.underlying_cause]()
                likelihood_ = deviation[prep.DictName.likelihood]()
                deviation = deviation[prep.DictName.subsequent_deviation]()
    if cause and cause.is_a:
        cause_lst = prep.get_inferred_results(cause)
        for idx, cause_ in enumerate(cause_lst):
            underlying_causes, effect, consequence, = assemble_concept_instance(substance,
            process_unit,
            deviation,
            [],
            cause_,
            False)
            # if likelihood_cause and likelihood_overall:
            scenario = {prep.DictName.cause: cause_(),
            prep.DictName.underlying_cause: underlying_causes,
            prep.DictName.effect: effect,
            prep.DictName.consequence: consequence}
            preliminary_scenario_list.append(scenario)
    elif cause_list:
        underlying_causes, effect, consequence, = assemble_concept_instance(substance,
        process_unit,
        deviation,
        underlying_cause_,
        [],
        True)
        scenario = {prep.DictName.cause: cause_list,
        prep.DictName.underlying_cause: underlying_causes,
        prep.DictName.effect: effect,
        prep.DictName.consequence: consequence}
        preliminary_scenario_list.append(scenario)
    else:
        underlying_causes, effect, consequence = assemble_concept_instance(substance,
        process_unit,
        deviation,
        [],
        [],
        False)
        scenario = {prep.DictName.cause: [],
        prep.DictName.underlying_cause: underlying_causes,
        prep.DictName.effect: effect,
        prep.DictName.consequence: consequence,
        }
        preliminary_scenario_list.append(scenario)
    sync_reasoner(debug=0)
    
infer_follow_up(process_unit,
    substance,
    deviation,
    environment,
    subsequent_deviation_loop,
    likelihood_,
    underlying_cause_,
    stack_elements,
    preliminary_scenario_list,
    extended_scenarion_list
    ) 

def infer_follow_up(process_unit,
                    substance,
                    deviation,
                    environment,
                    subsequent_deviation_loop,
                    likelihood_,
                    underlying_cause_,
                    stack_elements,
                    preliminary_scenario_list,
                    extended_scenarion_list):
    
    underlying_cause_list = []
    for scenario in preliminary_scenario_list:
        # Hint: This identifies more u-causes
        underlying_cause_list = prep.get_inferred_results(scenario[prep.DictName.underlying_cause])
        # Hint: than this
        # underlying_cause_list = scenario[prep.DictName.underlying_cause].is_instance_of
        
        # Remove non relevant components of the list
        if upper_onto.owl.Thing in underlying_cause_list:
            underlying_cause_list.remove(upper_onto.owl.Thing)
        if upper_onto.pse_onto.UnderlyingCause in underlying_cause_list:
            underlying_cause_list.remove(upper_onto.pse_onto.UnderlyingCause)
            
        # === Creation of a separate scenario for each underlying_cause
        if len(underlying_cause_list) >= 1:
            for underlying_cause in underlying_cause_list:
                for consequence in scenario[prep.DictName.consequence].is_instance_of:
                    for effect in scenario[prep.DictName.effect].is_instance_of:
                        extended_scenarion_list.append({prep.DictName.cause: scenario[prep.DictName.cause],
                                                        prep.DictName.underlying_cause: underlying_cause(),
                                                        prep.DictName.effect: effect(),
                                                        prep.DictName.consequence: consequence()})
        else:
            for consequence in scenario[prep.DictName.consequence].is_instance_of:
                for effect in scenario[prep.DictName.effect].is_instance_of:
                    extended_scenarion_list.append({prep.DictName.cause: scenario[prep.DictName.cause],
                                                    prep.DictName.effect: effect(),
                                                    prep.DictName.underlying_cause: scenario[prep.DictName.underlying_cause],
                                                    prep.DictName.consequence: consequence()})
        
    scenario_list = extended_scenarion_list
    
    for scenario in scenario_list:
        deviation1, deviation2 = assemble_deviation(deviation)
        
        if not subsequent_deviation_loop:
            scenario[prep.DictName.likelihood_cause] = risk_assessment_onto.Likelihood(
            likelihoodInvolvesUnderlyingcause=[scenario[prep.DictName.underlying_cause]],
            likelihoodInvolvesCause=[scenario[prep.DictName.cause]],
            likelihoodInvolvesEquipment=[process_unit.onto_object],
            likelihoodInvolvesSiteInformation=[environment.onto_object],
            likelihoodInvolvesDeviation=deviation1,
            likelihoodRequiresBoundaryCondition=process_unit.boundary_condition)
            scenario[prep.DictName.likelihood_effect] = risk_assessment_onto.Likelihood(
            likelihoodInvolvesEffect=[scenario[prep.DictName.effect]],
            likelihoodInvolvesCause=[scenario[prep.DictName.cause]],
            likelihoodInvolvesEquipment=[process_unit.onto_object],
            likelihoodInvolvesSiteInformation=[environment.onto_object],
            likelihoodInvolvesDeviation=deviation1,
            likelihoodRequiresBoundaryCondition=process_unit.boundary_condition)
        else:
            if likelihood_:
                scenario[prep.DictName.likelihood_cause] = likelihood_
            else:
                scenario[prep.DictName.likelihood_cause] = risk_assessment_onto.Likelihood(
                likelihoodInvolvesUnderlyingcause=underlying_cause_,
                likelihoodInvolvesEquipment=[process_unit.onto_object],
                likelihoodInvolvesDeviation=deviation1,
                likelihoodRequiresBoundaryCondition=process_unit.boundary_condition)
            if underlying_cause_:
                scenario[prep.DictName.underlying_cause] = underlying_cause_
                scenario[prep.DictName.likelihood_effect] = risk_assessment_onto.Likelihood(
                likelihoodInvolvesEffect=[scenario[prep.DictName.effect]],
                likelihoodInvolvesEquipment=[process_unit.onto_object],
                likelihoodInvolvesDeviation=deviation1,
                likelihoodRequiresBoundaryCondition=process_unit.boundary_condition)
        
        # Fix for excluding delayed ignition in case of external fire, makes not sense
        if scenario[prep.DictName.underlying_cause]:
            boundary_conditions_ = process_unit.boundary_condition.copy()
            if isinstance(scenario[prep.DictName.underlying_cause], list):
                pass
            else:
                if scenario[prep.DictName.underlying_cause].is_a[0] == causes_onto.ExternalFire:
                    for bc in boundary_conditions_:
                        if bc.is_a[0] == boundary_onto.DelayedIgnition:
                            boundary_conditions_.remove(bc)
        else:
            boundary_conditions_ = process_unit.boundary_condition.copy()
    
    
    
    
    scenario[prep.DictName.consequence_2nd] = consequence_onto.Consequence(
        consequenceInvolvesSubstance=[substance.onto_object],
        consequenceInvolvesEquipmentEntity=[process_unit.onto_object],
        isConsequenceOfDeviation=deviation1,
        consequenceImpliedByUnderlyingcause=[scenario[prep.DictName.underlying_cause]],
        isSubsequentConsequence=[scenario[prep.DictName.consequence]],
        consequenceRequiresBoundaryCondition=boundary_conditions_
    )
    
    scenario[prep.DictName.consequence_3rd] = consequence_onto.Consequence(
        consequenceInvolvesSubstance=[substance.onto_object],
        consequenceInvolvesEquipmentEntity=[process_unit.onto_object],
        isConsequenceOfDeviation=deviation1,
        consequenceImpliedByUnderlyingcause=[scenario[prep.DictName.underlying_cause]],
        isSubsequentConsequence=[scenario[prep.DictName.consequence_2nd]],
        consequenceRequiresBoundaryCondition=boundary_conditions_
    )
    
    scenario[prep.DictName.severity] = risk_assessment_onto.SeverityCategory(isSeverityOfConsequence=[scenario[prep.DictName.consequence],
        scenario[
            prep.DictName.consequence_2nd],
        scenario[
            prep.DictName.consequence_3rd]],
        isSeverityOfEffect=[scenario[prep.DictName.effect]],
        severityInvolvesSubstance=[substance.onto_object],
        severityInvolvesEquipment=[
        process_unit.onto_object],
        severityRequiresBoundaryCondition=process_unit.boundary_condition
    )
    
    scenario[prep.DictName.risk_cause] = risk_assessment_onto.RiskCategory(involvesSeverity=[scenario[prep.DictName.severity]],
    involvesLikelihood=[scenario[prep.DictName.likelihood_cause]])
    
    scenario[prep.DictName.risk_effect] = risk_assessment_onto.RiskCategory(involvesSeverity=[scenario[prep.DictName.severity]],
    involvesLikelihood=[scenario[prep.DictName.likelihood_effect]])
    
    if not isinstance(scenario[prep.DictName.cause], str) and not isinstance(scenario[prep.DictName.cause], list):
        cause_argument = [scenario[prep.DictName.cause]]
    else:
        cause_argument = []
        
    scenario[prep.DictName.safeguard] = safeguard_onto.Safeguard(safeguardOfDeviation=deviation1,
        safeguardPreventsEffect=[scenario[prep.DictName.effect]],
        safeguardPreventsCause=cause_argument,
        safeguardPreventsUnderlyingCause=[scenario[prep.DictName.underlying_cause]],
        safeguardMitigatesConsequence=[scenario[prep.DictName.consequence],
            scenario[prep.DictName.consequence_2nd],
            scenario[prep.DictName.consequence_3rd]
        ],
        safeguardDependsOnRiskCategory=[scenario[prep.DictName.risk_cause],
        scenario[prep.DictName.risk_effect]],
        safeguardInvolvesEquipmentEntity=[process_unit.onto_object],
        safeguardInvolvesSubstance=[substance.onto_object]
    )
    
    scenario[prep.DictName.safeguard_2nd] = safeguard_onto.Safeguard(
        impliesSafeguard=[scenario[prep.DictName.safeguard]],
        safeguardDependsOnRiskCategory=[scenario[prep.DictName.risk_cause], scenario[prep.DictName.risk_effect]],
        safeguardInvolvesEquipmentEntity=[process_unit.onto_object],
        safeguardInvolvesSubstance=[substance.onto_object]
    )
    
    sync_reasoner(debug=0)
    
    # === Pass results
    for scenario in scenario_list:
        consequence_list = [scenario[prep.DictName.consequence], scenario[prep.DictName.consequence_2nd], scenario[prep.DictName.consequence_3rd]]
        
        # === Prioritize identified risk effect-based since likelihood of it is based on specific generic data
        if scenario[prep.DictName.risk_effect].is_a[0].name == "A" or \
            scenario[prep.DictName.risk_effect].is_a[0].name == "B" or \
            scenario[prep.DictName.risk_effect].is_a[0].name == "C" or \
            scenario[prep.DictName.risk_effect].is_a[0].name == "D":
            scenario[prep.DictName.risk] = scenario[prep.DictName.risk_effect]
            scenario[prep.DictName.likelihood] = scenario[prep.DictName.likelihood_effect]
        else:
            scenario[prep.DictName.risk] = scenario[prep.DictName.risk_cause]
            
            # == Catch special case that in propagation mode no risk is determined but likelihood is present
            if scenario[prep.DictName.likelihood_effect].is_a[0] != upper_onto.pse_onto.Likelihood:
                scenario[prep.DictName.likelihood] = scenario[prep.DictName.likelihood_effect]
            else:
                scenario[prep.DictName.likelihood] = scenario[prep.DictName.likelihood_cause]
                
        propagated_consequence_found = False
        actual_consequence_found = False
        
        # === Identify propagating and actual results
        actual_consequences = []
        for consequence_ in consequence_list:
            if consequence_.is_a[0] == consequence_onto.PROPAGATED_CONSEQUENCE:
                propagated_consequence_found = True
                break
            elif consequence_.is_a[0] != consequence_onto.Consequence:
                actual_consequence_found = True
                actual_consequences.append(consequence_)
        if actual_consequence_found:
            prep.log_scenario(  0,
                                process_unit,
                                substance.name,
                                deviation,
                                scenario[prep.DictName.cause],
                                scenario[prep.DictName.effect],
                                scenario[prep.DictName.underlying_cause],
                                actual_consequences,
                                [scenario[prep.DictName.safeguard], scenario[prep.DictName.safeguard_2nd]],
                                False, # propagated
                                scenario[prep.DictName.risk]
            )
            
        if propagated_consequence_found and not actual_consequence_found:
            data = {prep.DictName.equipment: process_unit,
                    prep.DictName.substance: substance,
                    prep.DictName.deviation: deviation,
                    prep.DictName.cause: scenario[prep.DictName.cause],
                    prep.DictName.effect: scenario[prep.DictName.effect],
                    prep.DictName.underlying_cause: scenario[prep.DictName.underlying_cause],
                    prep.DictName.likelihood: scenario[prep.DictName.likelihood],
                    prep.DictName.consequence: consequence_list,
                    prep.DictName.safeguard: [scenario[prep.DictName.safeguard], scenario[prep.DictName.safeguard_2nd]],
                    prep.DictName.id: process_unit.identifier
            }
        
        # Catch duplicate in relevant propagation stack
        if isinstance(data[prep.DictName.cause], str):
            if not any(d[prep.DictName.cause] == data[prep.DictName.cause] and
                       d[prep.DictName.underlying_cause].is_a[0].name == data[prep.DictName.underlying_cause].is_a[0].name for d in stack_elements):
                stack_elements.append(data)
        else:
            if not any(d[prep.DictName.cause].is_a[0].name == data[prep.DictName.cause].is_a[0].name and
                       d[prep.DictName.underlying_cause].is_a[0].name == data[prep.DictName.underlying_cause].is_a[0].name for d in stack_elements):
                stack_elements.append(data)
    
    
    # === Identify subsequent deviations based on the results
    if not subsequent_deviation_loop:
        if subsequent_deviation_loop:
            current_deviation = deviation[prep.DictName.subsequent_deviation].copy()
        else:
            if isinstance(deviation, list):
                if len(deviation) > 1:
                    current_deviation = []
                    for dev in deviation:
                        current_deviation.append(dev.is_a[0])
                else:
                    current_deviation = deviation[0].is_a[0]
            else:
                current_deviation = deviation.is_a[0]
            
        # === check existence of apparatus
        if process_unit.apparatus:
            apparatus = process_unit.apparatus[0].is_a
            if isinstance(apparatus, list):
                apparatus = apparatus[0]
        else:
            apparatus = "None"
            
        for scenario in extended_scenarion_list:
            # === Infer subsequent deviations based on effect
            if scenario[prep.DictName.effect]:
                for effect in scenario[prep.DictName.effect].is_a:
                    current_case = {cbr.CaseAttributes.EquipmentEntity: process_unit.onto_object.is_a[0],
                    cbr.CaseAttributes.Event: effect,
                    cbr.CaseAttributes.Apparatus: apparatus,
                    cbr.CaseAttributes.IntendedFunction: process_unit.intended_function[0].is_a[0],
                    cbr.CaseAttributes.SubstancePhase:
                    substance.onto_object.hasStateOfAggregation[0].is_a[0]}
                    match = cbr.match_case_with_cb(current_case, cbr.propagation_case_base)
                    if match:
                        for m in match:
                            if match != current_deviation:
                                dev = {}
                                fmt_phase = str(substance.onto_object.hasStateOfAggregation[0].is_a[0]).split('.', 1)[1]
                                dev[prep.DictName.subsequent_deviation] = m
                                dev[prep.DictName.cause] = scenario[prep.DictName.cause].is_a[0]
                                dev[prep.DictName.underlying_cause] = scenario[prep.DictName.underlying_cause].is_a[0]
                                dev[prep.DictName.explanation] = process_unit.identifier + ": " + dev[
                                prep.DictName.cause].name + " -> " + effect.name + " -> " + dev[
                                prep.DictName.subsequent_deviation].name + " " + "(" + fmt_phase + ")"
                                dev[prep.DictName.likelihood] = scenario[prep.DictName.likelihood].is_a[0]
                                subsequent_deviations.append(dev)
                    
            # === Infer subsequent deviations based on cause
            if scenario[prep.DictName.cause]:
                for cause in scenario[prep.DictName.cause].is_a:
                    current_case = {cbr.CaseAttributes.EquipmentEntity: process_unit.onto_object.is_a[0],
                    cbr.CaseAttributes.Event: cause,
                    cbr.CaseAttributes.Apparatus: apparatus,
                    cbr.CaseAttributes.IntendedFunction: process_unit.intended_function[0].is_a[0],
                    cbr.CaseAttributes.SubstancePhase:
                    substance.onto_object.hasStateOfAggregation[0].is_a[0]}
                    match = cbr.match_case_with_cb(current_case, cbr.propagation_case_base)
                    if match:
                        for m in match:
                            if match != current_deviation:
                                dev = {}
                                fmt_phase = \
                                str(substance.onto_object.hasStateOfAggregation[0].is_a[0]).split('.', 1)[1]
                                dev[prep.DictName.subsequent_deviation] = m
                                dev[prep.DictName.initiating_event] = cause
                                dev[prep.DictName.underlying_cause] = scenario[prep.DictName.underlying_cause].is_a[0]
                                dev[prep.DictName.likelihood] = scenario[prep.DictName.likelihood].is_a[0]
                                dev[prep.DictName.explanation] = process_unit.identifier + ": " + cause.name + " -> " + dev[
                                prep.DictName.subsequent_deviation].name + " " + "(" + fmt_phase + ")"
                                subsequent_deviations.append(dev)
    
    # === Infer dev -> dev
    if config.CONSIDER_DEV_2_DEV_PROPAGATION:
        if process_unit.intended_function:
            intended_function = process_unit.intended_function[0].is_a[0]
        else:
            intended_function = None
        current_case = {cbr.CaseAttributes.EquipmentEntity: process_unit.onto_object.is_a[0],
        cbr.CaseAttributes.Event: current_deviation,
        cbr.CaseAttributes.Apparatus: apparatus,
        cbr.CaseAttributes.IntendedFunction: intended_function,
        cbr.CaseAttributes.SubstancePhase: substance.onto_object.hasStateOfAggregation[0].is_a[0]}
        match = cbr.match_case_with_cb(current_case, cbr.propagation_case_base)
        if match and match != current_deviation:
            fmt_phase = str(substance.onto_object.hasStateOfAggregation[0].is_a[0]).split('.', 1)[1]
            for m in match:
                dev = {prep.DictName.subsequent_deviation: m,
                prep.DictName.explanation: process_unit.identifier + ": " + current_deviation.name + " -> " + m.name + " " + "(" + fmt_phase + ")",
                prep.DictName.likelihood: scenario[prep.DictName.likelihood].is_a[0]} # cannot really be estimated
                subsequent_deviations.append(dev)


def propagation_based_analysis(plant_graph, order, propagation_stacks):
    # create copy of original plant layout and remove edges that are not in 'order' list
    # therefore a graph is created according to order
    graph = plant_graph.copy()
    for node in plant_graph.nodes(data=True):
        if node[0] not in order:
            graph.remove_node(node[0])
    # === Attach a placeholder
    for stack in propagation_stacks:
        stack[prep.DictName.passed_scenarios] = []
        
    # Check for cycle since topological sort not working for cycles
    cycle = list(nx.simple_cycles(graph))
    
    # Consider direction of graph and rearrange order
    if not cycle:
        rel_order = list(nx.topological_sort(graph)) # TODO: unit test, if this is working
    else:
        rel_order = list(graph.nodes)
        
    previous_case = {}
    consumed_flag = False
    
    print("=================== PROPAGATION MODE ===================")
    # for index in range(len(plant_graph.nodes)):
    for index, node_pos in enumerate(rel_order):
        process_unit = plant_graph.nodes[node_pos]["data"]
        # Do not assume propagation in case the sink has been reached
        if process_unit == equipment_onto.SinkEntity:
            break
        substances = plant_graph.nodes[node_pos]["substances"]
        # === Loop over substances
        for s, substance in enumerate(substances):
            print("========= Substance: {} = {} of {} =========".format(substance.name, s + 1, len(substances)))
            for m, mode in enumerate(process_unit.operating_mode):
                if mode:
                    print("========= Mode of Operation: {} = {} of {} =========".format(mode.name, m + 1, len(process_unit.operating_mode)))
                # === it no mode is specified continue
                if not mode:
                    continue
                else:
                    process_unit.onto_object.hasOperationMode = [mode()]
                    
                considered_deviations = []
                last_element = len(rel_order) - 1
                no_passed_scenario_flag = True
                
                if 1 <= index < last_element:
                    pos = rel_order[index - 1]
                    # === Remove duplicates
                    scenario_list = [i for n, i in enumerate(propagation_stacks[pos][prep.DictName.scenario]) if i not in propagation_stacks[pos][prep.DictName.scenario][n + 1:]]
                    # === Set flag
                    no_passed_scenario_flag = False
                    consumed_flag = False
                    # === Loop over propagating scenarios
                    for scenario in scenario_list:
                        # === Create input object from scenario, TODO: use scenario object directly
                        subsequent_deviation = assemble_input_object(scenario)
                        # === infer scenarios
                        propagation_based_hazard(subsequent_deviation,
                                                 process_unit,
                                                 substance,
                                                 False,
                                                 previous_case,
                                                 consumed_flag
                        )
                        # === Propagate partial scenario in case no effect have been identified
                        if not consumed_flag:
                            considered_deviations.append(subsequent_deviation)
                        
                    # === consider passed propagation that had no effect in previous equipment
                    if propagation_stacks[pos][prep.DictName.passed_scenarios]:
                        consumed_flag = False
                        for propagation in propagation_stacks[pos][prep.DictName.passed_scenarios]:
                            propagation_based_hazard(propagation,
                                    process_unit,
                                    substance,
                                    False, # last equipment in graph
                                    previous_case,
                                    consumed_flag
                                )
                            # === Propagate partial scenario in case no effect have been identified
                            if not consumed_flag:
                                propagation_stacks[pos + 1][prep.DictName.passed_scenarios].append(propagation)
                    
                    # === Propagate not consumed propagations into next element
                    for propagation in considered_deviations:
                        # Create a list of all values in list of dictionaries
                        list_of_all_values = [value for elem in propagation_stacks[pos + 1][prep.DictName.passed_scenarios] for value in elem.values()]
                        
                        # Catch duplicate in relevant propagation stack
                        if propagation[prep.DictName.explanation] not in list_of_all_values and propagation[prep.DictName.underlying_cause] not in list_of_all_values:
                            propagation_stacks[pos + 1][prep.DictName.passed_scenarios].append(propagation)
                elif index == len(rel_order) - 1:
                    pos = rel_order[index - 1]
                    if propagation_stacks[pos][prep.DictName.passed_scenarios]:
                        propagation_stacks[pos][prep.DictName.passed_scenarios] = [i for n, i in enumerate(
                        propagation_stacks[pos][prep.DictName.passed_scenarios]) if i not in propagation_stacks[pos][
                        prep.DictName.passed_scenarios][n + 1:]]
                            
                        for propagation in propagation_stacks[pos][prep.DictName.passed_scenarios]:
                            propagation_based_hazard(propagation,
                                                     process_unit,
                                                     substance,
                                                     True, # last equipment in graph
                                                     previous_case,
                                                     consumed_flag
                                                     )
                    
                    # Reached in case no scenarios are passed but the end is already reached
                    if no_passed_scenario_flag:
                        # === Remove duplicates
                        scenario_list = [i for n, i in enumerate(propagation_stacks[pos][prep.DictName.scenario]) if
                                         i not in propagation_stacks[pos][prep.DictName.scenario][n + 1:]]
                        
                        for p, propagation in enumerate(scenario_list):
                            print("=== LAST NODE: {} of {} scenarios ===".format(p, len(scenario_list)))
                            # === is case there is an effect means that no consequence was found for the equipment previously
                            if propagation[prep.DictName.effect].is_a[0] != effect_onto.Effect:
                                complete_propagated_scenario(propagation, process_unit, substance)
                            else:
                                # === Create input object from scenario,
                                propagation = assemble_input_object(propagation)
                                # == infer scenarios
                                if propagation:
                                    propagation_based_hazard(   propagation,
                                                                process_unit,
                                                                substance,
                                                                True, # last equipment in graph
                                                                previous_case,
                                                                consumed_flag)


def propagation_based_hazard(devex, process_unit, substance, last_equipment_entity, previous_case, consumed_flag):
    global results
    try:
        if isinstance(devex[prep.DictName.initiating_event].is_a[0], ThingClass):
            cause = [devex[prep.DictName.initiating_event]]
        else:
            cause = []
    except:
        cause = []
        
    preliminary_scenario_list = []
    scenario_list = []
    inferred_effects = []
    safeguard = None
    cause_list = [devex[prep.DictName.explanation]]
    deviation = devex[prep.DictName.subsequent_deviation]
    underlying_cause = devex[prep.DictName.underlying_cause]
    # catch the case where by mistake no safeguard is provided
    if not devex[prep.DictName.safeguard]:
        devex[prep.DictName.safeguard] = []
    if cause_list:
        underlying_causes, effect, consequence = assemble_concept_instance(
                                                            substance,
                                                            process_unit,
                                                            deviation,
                                                            underlying_cause,
                                                            cause,
                                                            True
                                                        )
        if devex[prep.DictName.likelihood]:
            likelihood = devex[prep.DictName.likelihood]
        else:
            likelihood = []
            
        scenario = {prep.DictName.cause: cause_list,
        prep.DictName.underlying_cause: underlying_causes,
        prep.DictName.effect: effect,
        prep.DictName.consequence: consequence,
        prep.DictName.likelihood: likelihood
        }
        inferred_effects.append(effect)
        preliminary_scenario_list.append(scenario)
        
    sync_reasoner(debug=0)
    
    for scenario in preliminary_scenario_list:
        for effect in scenario[prep.DictName.effect].is_a:
            if effect.is_a != [owl.Thing]:
                for consequence in scenario[prep.DictName.consequence].is_a:
                    # === inspecting individual
                    for prop in scenario[prep.DictName.consequence].get_properties():
                        if prop == consequence_onto.isConsequenceOfEffect:
                            for value in prop[scenario[prep.DictName.consequence]]:
                                for effect_ in value.is_a:
                                    # === Effect of consequence matches overall effect
                                    if effect_ == effect and scenario[prep.DictName.cause] and effect:
                                        scenario_list.append({prep.DictName.cause: scenario[prep.DictName.cause],
                                                              prep.DictName.underlying_cause: scenario[prep.DictName.underlying_cause],
                                                              prep.DictName.effect: effect(),
                                                              prep.DictName.consequence: consequence(),
                                                              prep.DictName.likelihood: scenario[prep.DictName.likelihood]}
                                                             )
                                        # Consume deviation in case full scenario is found
                                        consumed_flag = True
    
    for scenario in scenario_list:
        scenario[prep.DictName.consequence_2nd] = consequence_onto.Consequence(
        consequenceInvolvesSubstance=[substance.onto_object],
        consequenceInvolvesEquipmentEntity=[process_unit.onto_object],
        isConsequenceOfDeviation=deviation,
        isSubsequentConsequence=[scenario[prep.DictName.consequence]],
        consequenceRequiresBoundaryCondition=process_unit.boundary_condition)
        scenario[prep.DictName.consequence_3rd] = consequence_onto.Consequence(
        consequenceInvolvesSubstance=[substance.onto_object],
        consequenceInvolvesEquipmentEntity=[process_unit.onto_object],
        isConsequenceOfDeviation=deviation,
        isSubsequentConsequence=[scenario[prep.DictName.consequence_2nd]],
        consequenceRequiresBoundaryCondition=process_unit.boundary_condition)
        consequences = [scenario[prep.DictName.consequence],
        scenario[prep.DictName.consequence_2nd],
        scenario[prep.DictName.consequence_3rd]]
        scenario[prep.DictName.severity] = risk_assessment_onto.SeverityCategory(
        isSeverityOfConsequence=consequences,
        isSeverityOfEffect=[scenario[prep.DictName.effect]],
        severityInvolvesSubstance=[substance.onto_object],
        severityInvolvesEquipment=[process_unit.onto_object],
        severityRequiresBoundaryCondition=process_unit.boundary_condition)
        scenario[prep.DictName.risk] = risk_assessment_onto.RiskCategory(
        involvesSeverity=[scenario[prep.DictName.severity]],
        involvesLikelihood=scenario[prep.DictName.likelihood])
        if isinstance(scenario[prep.DictName.cause], ThingClass):
            cause_argument = [scenario[prep.DictName.cause]]
        elif isinstance(scenario[prep.DictName.cause], list):
            cause_argument = []
        else:
            cause_argument = []
            
        safeguard = safeguard_onto.Safeguard(safeguardOfDeviation=deviation,
        safeguardPreventsEffect=[scenario[prep.DictName.effect]],
        safeguardPreventsCause=cause_argument,
        safeguardPreventsUnderlyingCause=[scenario[prep.DictName.underlying_cause]],
        safeguardMitigatesConsequence=consequences,
        safeguardDependsOnRiskCategory=[scenario[prep.DictName.risk]],
        safeguardInvolvesEquipmentEntity=[process_unit.onto_object],
        safeguardInvolvesSubstance=[substance.onto_object])
        
        if devex[prep.DictName.safeguard]:
            if safeguard:
                scenario[prep.DictName.safeguard] = [devex[prep.DictName.safeguard]]
                scenario[prep.DictName.safeguard].append(safeguard)
            else:
                scenario[prep.DictName.safeguard] = devex[prep.DictName.safeguard]
        else:
            scenario[prep.DictName.safeguard] = safeguard
    
    if scenario_list:
        sync_reasoner(debug=0)
    
    # === Check whether cause equals deviation
    do_not_consider = False
    no_of_devs_in_cause = cause_list[0].count(deviation.is_a[0].name)
    if no_of_devs_in_cause == 2:
        do_not_consider = True
        
    # === Pass results
    for scenario in scenario_list:
        consequence_list = [scenario[prep.DictName.consequence], scenario[prep.DictName.consequence_2nd], scenario[prep.DictName.consequence_3rd]]
        # Somehow it is not always set above
        if not prep.DictName.safeguard in scenario:
            if devex[prep.DictName.safeguard]:
                scenario[prep.DictName.safeguard] = devex[prep.DictName.safeguard]
            else:
                scenario[prep.DictName.safeguard] = []
        if not do_not_consider:
            prep.log_scenario(0,
            process_unit,
            substance.name,
            deviation,
            scenario[prep.DictName.cause],
            scenario[prep.DictName.effect],
            scenario[prep.DictName.underlying_cause],
            consequence_list,
            scenario[prep.DictName.safeguard],
            True, # propagated
            scenario[prep.DictName.risk]
            )
        
        # === Infer subsequent deviations
        current_case = {cbr.CaseAttributes.EquipmentEntity: process_unit.onto_object.is_a[0],
        cbr.CaseAttributes.Event: scenario[prep.DictName.effect].is_a[0],
        cbr.CaseAttributes.Apparatus: process_unit.apparatus[0].is_a[0],
        cbr.CaseAttributes.IntendedFunction: process_unit.intended_function[0].is_a[0],
        cbr.CaseAttributes.SubstancePhase:
        substance.onto_object.hasStateOfAggregation[0].is_a[0]}
        match = cbr.match_case_with_cb(current_case, cbr.propagation_case_base)
        # === make sure there is a match and match is not the same as the last one
        # (prevent infinite run due to recursion)
        if match and current_case != previous_case:
            for m in match:
                explanation = process_unit.identifier + ": " + cause[0].is_a[0].name + " -> " + scenario[prep.DictName.effect].is_a[0].name + " -> " + \
                m.name + " " + "(" + substance.onto_object.hasStateOfAggregation[0].is_a[0].name + ")"
                subsequent_deviation = {prep.DictName.explanation: explanation,
                prep.DictName.underlying_cause: scenario[prep.DictName.underlying_cause],
                prep.DictName.safeguard: scenario[prep.DictName.safeguard],
                prep.DictName.subsequent_deviation: m(),
                prep.DictName.initiating_event: [], # empty because effects cannot be passed
                prep.DictName.likelihood: scenario[prep.DictName.likelihood],
                }
                propagation_based_hazard(subsequent_deviation,
                                         process_unit,
                                         substance,
                                         last_equipment_entity,
                                         current_case,
                                         consumed_flag
                                         )
                previous_case = current_case
