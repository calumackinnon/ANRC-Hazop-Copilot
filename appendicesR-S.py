# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 09:40:27 2024

@author: qrb15201
"""

import networkx as nx
from tearing import graph_operations as go
from string import ascii_lowercase
from enum import Enum

class GraphType(Enum):
 SingleLineSystem = 0
 MultiCycleSystem = 1
 RecycleFlowSystem = 2
 JunctionSystem = 3
 BranchSystem = 4
 SingleCycleSystem = 6
 ComplexSystem = 7
 
# === Function to identify ratio pattern [0, 1, .., 1, 0]
def identify_single_line(out_in_ratios):
    if isinstance(out_in_ratios, list):
        if len(out_in_ratios) > 2:
            if out_in_ratios[0] == 0 and out_in_ratios[-1] == 0:
                for i in out_in_ratios[1:-1]:
                    if i == 1:
                        continue
                    else:
                        return False
                return True
            else:
                return False
        else:
            return True

def identify_and_add_predecessors_to_list(graph, current_node, tmp_list):
    end_reached = False
    while not end_reached:
        try:
            tmp_predecessor = list(graph.predecessors(current_node))[0]
            tmp_list.append(tmp_predecessor)
            current_node = tmp_predecessor
        except IndexError:
            end_reached = True
    return

def identify_and_add_successors_to_list(graph, current_node, tmp_list):
    end_reached = False
    while not end_reached:
        try:
            tmp_successor = list(graph.successors(current_node))[0]
            tmp_list.append(tmp_successor)
            current_node = tmp_successor
        except IndexError:
            end_reached = True
    return

def my_max(e):
 return max(e)

def calc_out_in_flow_ratio(graph):
    node_out_in_ratio = []
    for g in graph.nodes:
        upstream = list(graph.predecessors(g))
        downstream = list(graph.successors(g))
        if len(upstream) == 0:
            node_out_in_ratio.append(0)
        else:
            ratio = len(downstream) / len(upstream)
            node_out_in_ratio.append(ratio)
    return node_out_in_ratio

def identify_upstream_equipment(graph, reference_node):
 return dict(nx.bfs_predecessors(graph, source=reference_node))

# source https://stackoverflow.com/questions/32997395/iterate-through-a-list-given-a-starting-point
def starting_with(arr, start_index):
    for i in range(start_index, len(arr)):
        yield arr[i]
    for i in range(start_index):
        yield arr[i]
 
def determine_recycles(graph):
    ratios = calc_out_in_flow_ratio(graph)
    
    if all(p == 0 or p == 1 for p in ratios):
        return False
    else:
        cycles = nx.simple_cycles(graph)
        cycles = list(cycles)
        comparison = check_equality_of_list(ratios)
        if comparison:
            return False
        if not comparison and cycles:
            return True
        else:
            return False

def determine_cycle_intersections(list_of_cycles):
    list_of_intersections = []
    for a, b in itertools.combinations(list_of_cycles, 2):
        # find intersections
        intersection = list(set(list_of_cycles.get(a)).intersection(list_of_cycles.get(b)))
        list_of_intersections.append({"cycles": [a, b], "intersection": intersection})
    return list_of_intersections

# Check whether a list contains the same items
def check_equality_of_list(lst):
 return not lst or lst.count(lst[0]) == len(lst) 


def determine_propagation_strategy(graph):
    new_graph = []
    type_of_graph = None
    intersection_node = None
    # === Cycle detection
    cycles = nx.simple_cycles(graph)
    cycles = list(cycles)
    # === Determine recycle streams
    recycle = go.determine_recycles(graph)
    # === Calculate outflow - inflow ratio
    ratios = go.calc_out_in_flow_ratio(graph)
    # === Identify single line pattern
    single_line = identify_single_line(ratios)
    # === identify roots and potential leaves === see documentation:
    # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms
    # .simple_paths.all_simple_paths.html
    roots = list(v for v, d in graph.in_degree() if d == 0)
    leaves = list(v for v, d in graph.out_degree() if d == 0)
    
    if len(cycles) > 1 and isinstance(cycles[0], list): # check dimensions
        list_of_cycles = {}
        # Loop over cycles and assign a letter to each cycle (unambiguous identification)
        for idx, cycle in enumerate(cycles):
            list_of_cycles.update({ascii_lowercase[idx]: cycle})
            
        # === Determine intersections between cycles
        intersections = go.determine_cycle_intersections(list_of_cycles)
        intersection_node = intersections[0]["intersection"]
        if len(intersection_node) == 1:
            intersection_node = intersection_node[0]
            
        # =====================
        for cycle in cycles:
            copy_of_graph = graph.copy()
            for node in graph.nodes:
                if node not in cycle:
                    copy_of_graph.remove_node(node)
                    
            for current, next in zip(cycle, cycle[1:]):
                copy_of_graph.add_edge(current, next)
            new_graph.append(list(copy_of_graph))
        
        type_of_graph = GraphType.MultiCycleSystem
    
    elif cycles and not recycle and not single_line:
        new_graph = list(graph.copy())
        type_of_graph = GraphType.SingleCycleSystem
    
    elif (recycle or cycles) and len(leaves) == 1:
        # === Tearing procedure in case of recycles
        H = graph.copy()
        # === Calculate outflow - inflow ratio
        ratios = go.calc_out_in_flow_ratio(H)
        # === Evaluate max ratio, position and node
        max_ratio = max(ratios)
        max_ratio_node_pos = ratios.index(max_ratio)
        successors_of_branch = list(graph.successors(max_ratio_node_pos))
        global_list = []
        # === consider first path until diverging node
        node_list = []
        for node in range(max_ratio_node_pos+1):
            node_list.append(node)
            
        global_list.append(node_list)
        # === detect nodes that form the recycle
        successor_streams = []
        for successor in successors_of_branch:
            node_list = [max_ratio_node_pos, successor]
            end_reached = False
            current_node = successor
            # === identify all paths after diverging node
            while not end_reached:
                try:
                    next_successor = list(graph.successors(current_node))[0]
                    node_list.append(next_successor)
                    # === back at diverging node (indicated by maximum ratio)
                    if next_successor == max_ratio_node_pos:
                        end_reached = True
                    else:
                        current_node = next_successor
                except IndexError:
                    end_reached = True
            successor_streams.append(node_list)
        
        # sort nodes according to numbers (nodes with highest numbers last)
        successor_streams.sort(key=my_max)
        # Very first list are nodes from first to diverging node
        new_graph = global_list + successor_streams
        type_of_graph = GraphType.RecycleFlowSystem
        
    elif not cycles and not recycle and single_line:
        new_graph = list(graph.copy())
        type_of_graph = GraphType.SingleLineSystem
    
    else:
        # Check in case all ratios are zero
        if not all(v == 0 for v in ratios):
            num_inflow_nodes = []
            # search for nodes with max inflow streams
            for g in graph.nodes:
                upstream = list(graph.predecessors(g))
                num_inflow_nodes.append(len(upstream))
                
            m = max(num_inflow_nodes)
            max_pos = [i for i, j in enumerate(num_inflow_nodes) if j == m][0]
            upstream_nodes_of_max_pos = list(graph.predecessors(max_pos))
            # === The intention is to identify all streams that lead into the junction
            global_list = []
            for node in upstream_nodes_of_max_pos:
                tmp_list = list(nx.ancestors(graph, list(graph.nodes)[node]))
                tmp_list.append(node) # Append first node before max pos node
                tmp_list.append(max_pos) # append max pos node
                global_list.append(tmp_list)
                
            # === Consider successors of merged node
            downstream_line = list(nx.descendants(graph, list(graph.nodes)[max_pos]))
            if downstream_line:
                downstream_line = [list(graph.nodes)[max_pos]] + downstream_line
                global_list.append(downstream_line)
                
            # assemble new structure
            new_graph = global_list
            type_of_graph = GraphType.JunctionSystem
    
    
        # Idea: in a junction system there is just 1 element where >2 nodes enter and 1 exits
        # this means, just one element has the lowest ratios
        else:
            # === identify minimum ratio
            min_ratio = min(i for i in ratios if i > 0)
            # === get position of minimum ratio
            pos_min_elements = [i for i, x in enumerate(ratios) if x == min_ratio]
            # === check for cycles
            cycles = list(nx.simple_cycles(graph))
            # === in case a cycle is detected the plant section is more complex and requires another strategy
            if len(pos_min_elements) == 1 and \
                min_ratio <= 0.5 and len(cycles) == 0 and len(roots) == 1:
                type_of_graph = GraphType.JunctionSystem
                node_list = list(graph.nodes)
                min_ratio_node_pos = ratios.index(min_ratio)
                min_ratio_node = node_list[min_ratio_node_pos]
                upstream_nodes_of_min_ratio = list(graph.predecessors(min_ratio_node))
                # === The intention is to identify all streams that lead into the junction
                global_list = []
                for node in upstream_nodes_of_min_ratio:
                    tmp_list = [node]
                    current_node = node
                    identify_and_add_predecessors_to_list(graph, current_node, tmp_list)
                    # === rearrange global list
                    tmp_list.insert(0, min_ratio_node)
                    tmp_list.reverse()
                    global_list.append(tmp_list)
                
                # === Search for successors of min ratio node, to find final propagation route
                tmp_list = [min_ratio_node]
                current_node = min_ratio_node
                identify_and_add_successors_to_list(graph, current_node, tmp_list)
                # === Sort results
                global_list.append(tmp_list)
                new_graph = global_list
            elif len(leaves) > 1 and len(cycles) == 0 and len(roots) == 1: # Multiple leaves are an indicator for a branch
                type_of_graph = GraphType.BranchSystem
                all_paths = []
                for root in roots:
                    paths = nx.all_simple_paths(graph, root, leaves)
                    all_paths.extend(paths)
                new_graph = all_paths
            else:
                type_of_graph = GraphType.ComplexSystem
                all_paths = []
                for root in roots:
                    for leaf in leaves:
                        paths = nx.all_simple_paths(graph, root, leaf)
                        all_paths.extend(paths)
                all_paths2 = []
                for root in roots:
                    paths = nx.all_simple_paths(graph, root, leaves)
                    all_paths2.extend(paths)
                new_graph = all_paths
        
    return type_of_graph, new_graph, intersection_node 


class TestUnderlyingCauses(unittest.TestCase):
    
    def test_solar_radiation_1(self):
        cause = causes_onto.AbnormalHeatInput()
        boundary_condition = [boundary_onto.LocatedOutside()]
        super_cause = causes_onto.SuperCause(isSupercauseOfCause=[cause],
        supercauseRequiresBoundaryCondition=boundary_condition)
        sync_reasoner()
        super_cause_ = pre_processing.stringify_cleanup_inferred_res(super_cause)
        super_cause_.sort()
        time.sleep(0.01)
        self.assertEqual(super_cause_, ['SolarRadiation'], "Should be ['SolarRadiation']")
 
    def test_blocked_piping_heat_input_1(self):
        cause = causes_onto.ThermalExpansion()
        unit = equipment_onto.ConnectionPipeEntity()
        boundary_condition = [boundary_onto.ExternalFirePossible()]
        super_cause = causes_onto.SuperCause(isSupercauseOfCause=[cause],
                                             supercauseInvolvesUnit=[unit],
                                             supercauseRequiresBoundaryCondition=boundary_condition)
        sync_reasoner()
        super_cause_ = pre_processing.stringify_cleanup_inferred_res(super_cause)
        super_cause_.sort()
        time.sleep(0.01)
        self.assertEqual(super_cause_, ['BlockedPipingAndHeatInput'],
                         "Should be ['BlockedPipingAndHeatInput']")
 
