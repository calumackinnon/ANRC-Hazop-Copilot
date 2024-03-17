# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:38:12 2024

Making a file which combines all appendices into a single script.

The idea is just to see if this can allow method name errors to be resolved.

PS this looks useful: https://towardsdatascience.com/graphs-with-python-overview-and-best-libraries-a92aa485c2f8


Generally speaking, this code has to be trusted to do what it says on the tin, 
but it is opaque and not structured in a readable manner. Many of the functions
could be subdivided and commented. It appears some global variables are in use.

Presently fixing a bug at from tearing import ... as go, I believe it is to do 
with NetworkX. Is it this? https://sdopt-tearing.readthedocs.io/en/latest/
It is to do with p 118 in the dissertation.

@author: qrb15201 Calum Mackinnon
"""


# from enum import Enum
from owlready2 import *
import itertools
import unittest

# equipment_onto = None #TODO Is this a global variable?


#%% Appendix R - Graph Manipulation # Tearing

import networkx as nx
# from tearing import graph_operations as go # Is this tensorflow?
from string import ascii_lowercase 
from enum import Enum

class GraphType(Enum):
    SingleLineSystem = 0
    MultiCycleSystem = 1
    RecycleFlowSystem = 2
    JunctionSystem = 3
    BranchSystem = 4
    JunctionSystemRatiosAllZero = 5 # This has been created in response to
    # the structure of the code in the determine_propagation_strategy() method.
    SingleCycleSystem = 6 
    ComplexSystem = 7
 
# === Function to identify ratio pattern [0, 1, .., 1, 0]
def identify_single_line(out_in_ratios):
    """
    Check if a list of 1s and 0s takes the form [0,1,1,...,1,1,0] nomatter its
    overall length.

    Parameters
    ----------
    out_in_ratios : list
        A list of 0 and 1 digits.

    Returns
    -------
    boolean
        Whether or not the out_in_ratios matches the expected pattern.

    """
    if not isinstance(out_in_ratios, list): return False
    
    if len(out_in_ratios) > 2:
        
        if out_in_ratios[0] != 0 or out_in_ratios[-1] != 0: return False
        
        for i in out_in_ratios[1:-1]:
            if i!=1: return False
        
        return True # the sequence definitely matches the expected pattern.
    
    else:
        
        return True #TODO not sure! [1,1] would return True here.

def identify_and_add_predecessors_to_list(graph, current_node, tmp_list):
    end_reached = False
    while not end_reached:
        try:
            tmp_predecessor = list(graph.predecessors(current_node))[0]
            tmp_list.append(tmp_predecessor)
            current_node = tmp_predecessor
        except IndexError:
            end_reached = True

def identify_and_add_successors_to_list(graph, current_node, tmp_list):

    end_reached = False
    
    while not end_reached:
        try:
            tmp_successor = list(graph.successors(current_node))[0]
            tmp_list.append(tmp_successor)
            current_node = tmp_successor
        except IndexError:
            end_reached = True
            
    
def my_max(e):  return max(e)

def calc_out_in_flow_ratio(graph):
    """
    Evaluate the Graph structure in terms of output/input edges for each node.

    Parameters
    ----------
    graph : NetworkX.Graph
        A directed Graph.

    Returns
    -------
    node_out_in_ratio : list[float]
        A list of the same length as the numver of nodes in the Graph. It has a
        ratio of output / input edges for each node.

    """
    
    node_out_in_ratio = []
    
    for g in graph.nodes:
        
        upstream = list(graph.predecessors(g))
        downstream = list(graph.successors(g))
        
        if len(upstream) == 0: # if the first // do not divide by zero
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
        return False #TODO not sure! 3 / 3 = 1, so some cycles can still exist.
    else:
        cycles = nx.simple_cycles(graph)
        cycles = list(cycles)
        comparison = check_equality_of_list(ratios)
        if comparison:
            return False
        
        # I think the code below is simpler as
        # return not comparison and cycles # untested
        # if not comparison and cycles:
        #     return True
        # else:
        #     return False
        
        return not comparison and cycles

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


def findTypeOf(graph):
    """
    Evaluate a Graph's structure in order to help pick a propagation strategy.

    Parameters
    ----------
    graph : NetworkX.Graph
        A Graph as defined by NetworkX.

    Returns
    -------
    GraphType
        An Enum which describes the Graph structure.

    """
    
    assert isinstance(graph, nx.Digraph), 'Not a directed graph as anticipated'
    
    ratios = calc_out_in_flow_ratio(graph)
    single_line = identify_single_line(ratios)
    cycles = nx.simple_cycles(graph)
    
    recycle = determine_recycles(graph)
    
    roots = list(v for v, d in graph.in_degree() if d == 0)
    leaves = list(v for v, d in graph.out_degree() if d == 0)

    
    if len(cycles) > 1 and isinstance(cycles[0], list):
        return GraphType.MultiCycleSystem
    
    elif cycles and not recycle and not single_line:
        return GraphType.SingleCycleSystem
    
    elif (recycle or cycles) and len(leaves) == 1:
        return GraphType.RecycleFlowSystem
    
    elif not cycles and not recycle and single_line:
        return GraphType.SingleLineSystem
    
    else:
    
        # Check in case all ratios are zero
        if not all(v == 0 for v in ratios): # if some ratios are not zero
            return GraphType.JunctionSystem
        
        else: # all ratios are zero
        
            # === identify minimum ratio
            min_ratio = min(i for i in ratios if i > 0)
            
            # === get position of minimum ratio
            pos_min_elements = [i for i, x in enumerate(ratios) if x == min_ratio]
            
            # === check for cycles
            cycles = list(nx.simple_cycles(graph))

            if len(pos_min_elements) == 1 and \
                min_ratio <= 0.5 and len(cycles) == 0 and len(roots) == 1:
                return GraphType.JunctionSystem    
        
            elif len(leaves) > 1 and len(cycles) == 0 and len(roots) == 1: 
                return GraphType.BranchSystem
            
            else:
                return GraphType.ComplexSystem
    
    
def replicate(graph, graph_type):
    """
    Create a replica of the Graph according to its type.

    Parameters
    ----------
    graph : NetworkX.Graph
        A Graph.
    graph_type : GraphType
        An Enum to specify the structure of the Graph.

    Returns
    -------
    new_graph : list
        A copy of the graph structured as a list.

    """
    
    
    assert isinstance(graph, nx.Digraph), 'Not a directed graph as anticipated'
    
    ratios = calc_out_in_flow_ratio(graph)
    # single_line = identify_single_line(ratios)
    cycles = nx.simple_cycles(graph)
    # recycle = determine_recycles(graph)
    roots = list(v for v, d in graph.in_degree() if d == 0)
    leaves = list(v for v, d in graph.out_degree() if d == 0)

    new_graph = []
    
    match graph_type:
        
        case GraphType.MultiCycleSystem:
            for cycle in cycles:
                copy_of_graph = graph.copy()
                for node in graph.nodes:
                    if node not in cycle:
                        copy_of_graph.remove_node(node)
                        
                for current, next in zip(cycle, cycle[1:]):
                    copy_of_graph.add_edge(current, next)
                new_graph.append(list(copy_of_graph))

        case GraphType.RecycleFlowSystem:
            # === Tearing procedure in case of recycles  
            # H = graph.copy()
            
            # === Calculate outflow - inflow ratio
            # ratios = go.calc_out_in_flow_ratio(H)
            
            # === Evaluate max ratio, position and node
            max_ratio = max(ratios)
            max_ratio_node_pos = ratios.index(max_ratio)
            successors_of_branch = list(graph.successors(max_ratio_node_pos))
            
            
            # === consider first path until diverging node
            global_list = []
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

        case GraphType.JunctionSystem:
            # In determine_propagation_strategy(), there are two sections of 
            # code which create a new_graph for the GraphType.JunctionSystem
            # case, so I am creating a new value in the GraphType Enum.
            
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
            
        case GraphType.JunctionSystemRatiosAllZero: # Newly created
        
            # === identify minimum ratio
            min_ratio = min(i for i in ratios if i > 0)

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

        case GraphType.BranchSystem:
            all_paths = []
            
            for root in roots:
                paths = nx.all_simple_paths(graph, root, leaves)
                all_paths.extend(paths)
                
            new_graph = all_paths

        case GraphType.ComplexSystem:
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
            
        case _: # the default works for SingleLineSystem and SingleCycleSystem.
            new_graph = list(graph.copy())
        
    return new_graph

def getIntersectionNode(graph, graph_type):
    """
    In a MultiCycleSystem, find one node where different cycles intersect.

    Parameters
    ----------
    graph : NetworkX.Graph
        A directed Graph.
    graph_type : GraphType
        An Enum for the type of Graph structure.

    Returns
    -------
    intersection_node : NetworkX.Graph.Node
        A node which forms a part of more than one cycle within the Graph.

    """
    
    if graph_type != GraphType.MultiCycleSystem: return None
        
    # === Cycle detection
    cycles = nx.simple_cycles(graph)
    cycles = list(cycles)

    list_of_cycles = {}
    # Loop over cycles and assign a letter to each cycle (unambiguous identification)
    for idx, cycle in enumerate(cycles):
        list_of_cycles.update({ascii_lowercase[idx]: cycle})
        
    # === Determine intersections between cycles
    intersections = determine_cycle_intersections(list_of_cycles)
    intersection_node = intersections[0]["intersection"]
    if len(intersection_node) == 1:
        intersection_node = intersection_node[0]
        
    return intersection_node


def determine_propagation_strategy(graph):
    """
    To be deprecated & replaced by findTypeOf(graph) and replicate(graph).

    Parameters
    ----------
    graph : NetworkX.Graph
        A Graph for use with the NetworkX package.

    Returns
    -------
    type_of_graph : Enum
        GraphType set to a value in {0,1,2,3,4,6,7}.
    new_graph : list
        A list representing the graph in some new manner I'm not yet sure of.
    intersection_node : TYPE
        The node(s) at which cycles intersect. Only applies to 
        GraphType.MultiCycleSystem.

    """
    
    assert False, 'This method has now been deprecated, but is being called.'
    
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
        
        # === Tearing procedure in case of recycles. 
        H = graph.copy()
        
        # === Calculate outflow - inflow ratio
        ratios = go.calc_out_in_flow_ratio(H)
        
        # === Evaluate max ratio, position and node
        max_ratio = max(ratios)
        max_ratio_node_pos = ratios.index(max_ratio)
        successors_of_branch = list(graph.successors(max_ratio_node_pos))
        
        
        # === consider first path until diverging node
        global_list = []
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
        if not all(v == 0 for v in ratios): # if some ratios are not zero
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
        else: # all ratios are zero
            
            # === identify minimum ratio
            min_ratio = min(i for i in ratios if i > 0)
            
            # === get position of minimum ratio
            pos_min_elements = [i for i, x in enumerate(ratios) if x == min_ratio]
            
            # === check for cycles
            cycles = list(nx.simple_cycles(graph))
            
            # === in case a cycle is detected the plant section is more complex and requires another strategy
            if len(pos_min_elements) == 1 and \
                min_ratio <= 0.5 and len(cycles) == 0 and len(roots) == 1:
                    
                type_of_graph = GraphType.JunctionSystemRatiosAllZero
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

#%% Appendix S - Unit Tests


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


#%% Appendix A - Equipment and Port Classes

class MyPort:
    
    def __init__(self, name, port_instrumentation, connection_type):
        self.name = name
        self.port_instrumentation = port_instrumentation
        self.connection_type = connection_type
        self.onto_object = equipment_onto.Port(hasConnectionType=self.connection_type,
                                               hasName = self.name,
                                               portEquippedWithInstrumentation=self.port_instrumentation
                                               )
        

class MyEquipmentEntity:
    
    def __init__(self, equipment, identifier, boundary_condition, transportable,
                 operating_modes, max_operating_pressure_in_barg,
                 max_operating_temperature_in_kelvin):
        
        self.name = equipment,
        self.identifier = identifier,
        self.max_operating_pressure_in_barg = max_operating_pressure_in_barg
        self.max_operating_temperature_in_kelvin = max_operating_temperature_in_kelvin
        
        self.onto_object = None
        self.instrumentation = []
        self.fixture = []
        self.piping
        self.subunit
        self.boundary_condition = boundary_condition
        self.material_transfer_equipment = []
        self.apparatus
        self.intended_function
        self.transportable = transportable
        self.connected_plant_item
        self.control_instance
        self.operating_mode = operating_modes
        self.volume_of_enclosure = None
        self.volume_flow_of_transfer_equipment = None
        self.pressure_volume_product = None
        
    def set_volume_of_enclosure(self, voe):
        self.volume_of_enclosure = voe
        
    def set_volume_flow_of_transfer_equipment(self, volFlow):
        self.volume_flow_of_transfer_equipment = volFlow
        
    def add_connected_plantItem(self, item):
        if item:
            self.connected_plant_item.append(item(None))
            
    def set_control_instance(self, control_instance):
        
        if control_instance:
            self.control_instance.append(control_instance)
            
    def set_intended_function(self, intended_function):
        
        if intended_function:
            self.intended_function.append(intended_function(None))
            
    def set_apparatus(self, apparatus):
        
        if apparatus:
            self.set_apparatus.append(apparatus(None))
            
            
    def addFixture(self, fixture):
        
        if fixture:
            self.fixture.append(fixture(None))
            
    def add_piping(self, piping):
        
        if piping:
            self.piping.append(piping(None))
            
    def add_instrumentation(self, instrumentation):
        
        if instrumentation:
            instrumentation_instance = instrumentation[0](None)
            
            #Append a unique tag of instrumentation as an annotation to instrumentation instance
            if instrumentation[1]:
                instrumentation_instance.comment = instrumentation[1]
            self.instrumentation.append(instrumentation_instance)
            
            
    def add_subunit(self, subunit):
        if subunit:
            self.subunit.append(subunit(None))
            
    def set_material_transfer_equipment(self, mat):
        
        if mat: self.material_transfer_equipment.append(mat(None))
        
    def determine_pv_product(self):
        
        self.pressure_volume_product = self.max_operating_pressure_in_barg * self.volume_of_enclosure
        
    def assemble_ontology_object(self, equipment_entity):
        
        self.onto_object = equipment_entity(
                hasFixture = self.fixture,
                hasInstrumentation = self.instrumentation,
                hasMaterialTransferEquipment = self.material_transfer_equipment,
                hasSubunit = self.subunit,
                hasApparatus=self.apparatus,
                hasPiping=self.piping,
                hasIntendedFunction=self.intended_function,
                hasConnectionToAdjacentPlantItem=self.connected_plant_item,
                hasMaximumOperatingPressureInBarGauge=self.max_operating_pressure_in_barg,
                hasMaximumOperatingTemperatureInKelvin=self.max_operating_temperature_in_kelvin,
                isTransportable=self.transportable,
                entityControlledBy=self.control_instance,
                hasPort=[],
                hasOperationMode=[]
            )
        
    def set_max_operating_pressure_in_barg(self, max_operating_pressure):
        self.max_operating_pressure_in_barg = max_operating_pressure 
        
        
#%% Appendix B - Substance Class

class MySubstance:
    
    def __init__(   self,
                    substance_name,
                    cas_number,
                    freezing_point,
                    boiling_point,
                    flash_point,
                    lower_explosion_limit,
                    upper_explosion_limit):
        
        self.name = substance_name
        self.cas_number = cas_number
        self.onto_object = None
        self.freezing_point = freezing_point
        self.boiling_point = boiling_point
        self.flash_point = flash_point
        self.lower_explosion_limit = lower_explosion_limit
        self.upper_explosion_limit = upper_explosion_limit
        self.task = []
        self.intended_state_of_aggregation = []
        self.hazard_class = []
        self.stability_reactivity_information = []
    
    def add_hazard_class(self, hazard_class):
        if hazard_class:
            for haz_c in hazard_class:
                self.hazard_class.append(haz_c(None))
    
    def add_stability_reactivity_information(self, stability_reactivity_information):
        if stability_reactivity_information:
            for sr_info in stability_reactivity_information:
                self.stability_reactivity_information.append(sr_info())
    
    def set_intended_state_of_aggregation(self, state_of_aggregation):
        if state_of_aggregation:
            self.intended_state_of_aggregation.append(state_of_aggregation())
    
    def set_substance_task(self, substance_task):
        self.task.append(substance_task())
    
    def assemble_onto_object(self, substance):
        self.onto_object = substance(hasSpecificTask=self.task,
            hasStabilityReactivityInformation=self.stability_reactivity_information,
            hasHazardClass=self.hazard_class,
            hasStateOfAggregation=self.intended_state_of_aggregation,
            hasBoilingPointInKelvin=self.boiling_point,
            hasFreezingPointInKelvin=self.freezing_point,
            hasFlashpointInKelvin=self.flash_point,
            hasUpperExplosionLimitInPercent=self.upper_explosion_limit,
            hasLowerExplosionLimitInPercent=self.lower_explosion_limit
        )
        
        
        
#%% Appendix D 

def source(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):

    equipment = equipment_onto.SourceEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature )
    equipment_entity.set_intended_function(process_onto.NoIntendedFunction)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def sink(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):

    equipment = equipment_onto.SinkEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_intended_function(process_onto.NoIntendedFunction)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def connection_pipe(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):

    equipment = equipment_onto.ConnectionPipeEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_intended_function(process_onto.Transport)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def tank_truck(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume_of_enclosure):

    equipment = equipment_onto.TankTruckEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_volume_of_enclosure(volume_of_enclosure)
    equipment_entity.set_intended_function(process_onto.Loading)
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_piping(equipment_onto.TankTruckHose)
    equipment_entity.add_instrumentation((equipment_onto.ApiAdaptorValve, "{}-VA1".format(identifier)))
    equipment_entity.add_fixture(equipment_onto.Baffle)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def storage_tank_1(identifier, circumstances, control_instance, transportable, operating_modes):
    
    equipment = equipment_onto.StorageTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.set_apparatus(equipment_onto.AtmosphericStorageTank)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def storage_tank_2(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume_of_enclosure):

    equipment = equipment_onto.StorageTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_volume_of_enclosure(volume_of_enclosure)
    equipment_entity.set_apparatus(equipment_onto.AtmosphericStorageTank)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.add_piping(equipment_onto.VentPipe)
    equipment_entity.add_instrumentation((equipment_onto.LevelIndicator, None))
    equipment_entity.add_instrumentation((equipment_onto.HighLevelAlarm, None))
    # equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)

    return equipment_entity

def cooled_storage_tank_1(identifier, circumstances, control_instance, transportable, operating_modes):

    equipment = equipment_onto.StorageTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.CoolingSystem)
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.set_apparatus(equipment_onto.AtmosphericStorageTank)
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_piping(equipment_onto.TubeCoil)
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def cooled_storage_tank_2(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    
    equipment = equipment_onto.StorageTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.CoolingSystem)
    equipment_entity.set_apparatus(equipment_onto.AtmosphericStorageTank)
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_fixture(equipment_onto.TubeCoil)
    equipment_entity.add_instrumentation((equipment_onto.LevelIndicatorController, None))
    equipment_entity.add_connected_plant_item(equipment_onto.FlowControlValve)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def reactor(identifier, circumstances, control_instance, transportable, operating_modes):
    
    equipment = equipment_onto.ReactorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Reaction)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity


def shell_tube_heat_exchanger(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.ShellTubeHeatExchangerEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    # T-O-D-O: wieso nur 2 Anschlüsse
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_fixture(equipment_onto.Baffle)
    equipment_entity.add_piping(equipment_onto.TubeBundle)
    equipment_entity.set_intended_function(process_onto.HeatTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def reboiler(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.SteamDrivenReboilerEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_fixture(equipment_onto.Baffle)
    equipment_entity.add_piping(equipment_onto.TubeBundle)
    equipment_entity.add_subunit(equipment_onto.SteamSupply)
    equipment_entity.set_intended_function(process_onto.HeatTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity


def settling_tank(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume_of_enclosure):

    equipment = equipment_onto.SettlingTankEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    # equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_instrumentation((equipment_onto.LevelIndicatorController, None))
    equipment_entity.add_instrumentation((equipment_onto.PressureIndicatorController, None))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Separation)
    equipment_entity.assemble_ontology_object(equipment)
    equipment_entity.set_control_instance(control_instance)
    
    return equipment_entity

def inertgas_blanketing(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):

    equipment = equipment_onto.InertgasBlanketingEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.PressureControlValve, "{}-VA1".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.InertgasSupply)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.add_subunit(equipment_onto.NonReturnValve)
    equipment_entity.add_piping(equipment_onto.BlanketingGasline)
    equipment_entity.add_connected_plant_item(equipment_onto.PressureIndicatorController)
    equipment_entity.set_intended_function(process_onto.Inertization)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def pressure_vessel(identifier, circumstances, control_instance, transportable, operating_modes):

    equipment = equipment_onto.PressureVesselEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def pressure_receiver(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume):
    equipment = equipment_onto.PressureReceiverEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Storage)
    equipment_entity.set_volume_of_enclosure(volume)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def plate_heat_exchanger(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.PlateHeatExchangerEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.add_fixture(equipment_onto.PlatePackage)
    equipment_entity.set_apparatus(equipment_onto.NoApparatus)
    equipment_entity.set_intended_function(process_onto.HeatTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def centrifugal_pump_1(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.PumpEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.set_material_transfer_equipment(equipment_onto.CentrifugalPump)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.set_apparatus(equipment_onto.PumpCasing)
    equipment_entity.set_intended_function(process_onto.MaterialTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity 


def centrifugal_pump_2( identifier,
                        circumstances,
                        control_instance,
                        transportable,
                        operating_modes,
                        max_pressure,
                        max_temperature,
                        volume_flow):
    equipment = equipment_onto.PumpEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_volume_flow_of_transfer_equipment(volume_flow)
    equipment_entity.set_apparatus(equipment_onto.PumpCasing)
    equipment_entity.set_intended_function(process_onto.MaterialTransfer)
    equipment_entity.set_material_transfer_equipment(equipment_onto.CentrifugalPump)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.add_fixture(equipment_onto.Impeller)
    # equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    # equipment_entity.add_instrumentation((equipment_onto.BottomDrainValve, "{}-VA3".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.add_subunit(equipment_onto.NonReturnValve)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def screw_compressor(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume_flow):
    
    equipment = equipment_onto.CompressorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.add_subunit(equipment_onto.LubricationSystem)
    equipment_entity.set_material_transfer_equipment(equipment_onto.ScrewCompressor)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_apparatus(equipment_onto.CompressorCasing)
    equipment_entity.set_intended_function(process_onto.MaterialTransfer)
    equipment_entity.set_volume_flow_of_transfer_equipment(volume_flow)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def piston_compressor(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.CompressorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_subunit(equipment_onto.SealingSystem)
    equipment_entity.add_subunit(equipment_onto.LubricationSystem)
    equipment_entity.set_material_transfer_equipment(equipment_onto.PistonCompressor)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_apparatus(equipment_onto.CompressorCasing)
    equipment_entity.set_intended_function(process_onto.MaterialTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity


def pneumatically_flow_control_valve_1(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.FluidControl)
    equipment_entity.add_instrumentation((equipment_onto.PneumaticActuator, None))
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.add_subunit(equipment_onto.CompressedAirSupply)
    equipment_entity.add_subunit(equipment_onto.Bypass)
    equipment_entity.add_instrumentation((equipment_onto.FlowControlValve, "{}-VA1".format(identifier)))
    equipment_entity.add_connected_plant_item(equipment_onto.LevelIndicatorController)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def pneumatically_pressure_control_valve_1(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.PressureControl)
    equipment_entity.add_instrumentation((equipment_onto.PneumaticActuator, None))
    equipment_entity.add_instrumentation((equipment_onto.Controller, None))
    equipment_entity.add_subunit(equipment_onto.CompressedAirSupply)
    equipment_entity.add_instrumentation((equipment_onto.PressureControlValve, "{}-VA1".format(identifier)))
    equipment_entity.add_connected_plant_item(equipment_onto.PressureIndicatorController)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def manual_three_way_valve(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.ThreeWayValve, "{}-VA1".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.FluidControl)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def throttling_valve(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.ThrottlingValve, "{}-VA1".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.FluidControl)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity 

def manual_valve(identifier, circumstances, control_instance, transportable, operating_modes):
    equipment = equipment_onto.ValveEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.ShutOffValve, "{}-VA1".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.Body)
    equipment_entity.set_intended_function(process_onto.FluidControl)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def air_cooled_condenser(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.AirCooledCondenserEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.set_apparatus(equipment_onto.Casing)
    equipment_entity.add_fixture(equipment_onto.FinnedCoil)
    equipment_entity.set_material_transfer_equipment(equipment_onto.Fan)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_intended_function(process_onto.Condensation)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def shell_tube_evaporator(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature, volume):
    equipment = equipment_onto.ShellTubeEvaporatorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_fixture(equipment_onto.Baffle)
    equipment_entity.add_fixture(equipment_onto.TubeBundle)
    equipment_entity.set_volume_of_enclosure(volume)
    equipment_entity.set_intended_function(process_onto.Evaporation)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def fin_tube_evaporator(identifier, circumstances, control_instance, transportable, operating_modes):
    
    equipment = equipment_onto.FinTubeEvaporatorEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.add_instrumentation((equipment_onto.InletValve, "{}-VA1".format(identifier)))
    equipment_entity.add_instrumentation((equipment_onto.OutletValve, "{}-VA2".format(identifier)))
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.set_apparatus(equipment_onto.Casing)
    equipment_entity.add_fixture(equipment_onto.FinnedCoil)
    equipment_entity.set_material_transfer_equipment(equipment_onto.Fan)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_intended_function(process_onto.Evaporation)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def wet_scrubber(identifier, circumstances, control_instance, transportable, operating_modes):
    
    equipment = equipment_onto.WetScrubberEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.add_fixture(equipment_onto.LiquidDistributor)
    equipment_entity.add_fixture(equipment_onto.PackedBed)
    equipment_entity.set_intended_function(process_onto.Purification)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def cooling_tower(identifier, circumstances, control_instance, transportable, operating_modes):
    
    equipment = equipment_onto.CoolingTowerEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes)
    equipment_entity.set_apparatus(equipment_onto.OpenVessel)
    equipment_entity.add_subunit(equipment_onto.ElectricalEnergySupply)
    equipment_entity.add_fixture(equipment_onto.LiquidDistributor)
    equipment_entity.add_fixture(equipment_onto.PackedBed)
    equipment_entity.add_fixture(equipment_onto.Basin)
    equipment_entity.add_instrumentation((equipment_onto.ElectricMotor, None))
    equipment_entity.add_instrumentation((equipment_onto.SpeedController, None))
    equipment_entity.set_intended_function(process_onto.HeatTransfer)
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity

def crude_stabilizer_column(identifier, circumstances, control_instance, transportable, operating_modes, max_pressure, max_temperature):
    equipment = equipment_onto.StabilizerColumnEntity
    equipment_entity = MyEquipmentEntity(equipment, identifier, circumstances, transportable, operating_modes, max_pressure, max_temperature)
    equipment_entity.set_apparatus(equipment_onto.PressureVessel)
    equipment_entity.set_intended_function(process_onto.Stabilization)
    equipment_entity.add_fixture(equipment_onto.Tray)
    equipment_entity.add_fixture(equipment_onto.ChimneyTray)
    equipment_entity.add_instrumentation((equipment_onto.LevelIndicatorController, None))
    equipment_entity.set_control_instance(control_instance)
    equipment_entity.assemble_ontology_object(equipment)
    
    return equipment_entity 


#%% Appendix E

phase_weight = 0.15
apparatus_weight = 0.3
event_weight = 0.4
equipment_weight = 0.05
intended_function_weight = 0.1

class CaseAttributes(Enum):
    
    No = 1
    EquipmentEntity = 2
    Event = 3
    Apparatus = 4
    IntendedFunction = 5
    SubstancePhase = 6
    InferredDeviation = 7    
    
# propagation_case_base is a list of dictionaries.
#TODO Check that equipment_onto is defined.
propagation_case_base = [
    # === Pump
    {CaseAttributes.No: 1,
    CaseAttributes.EquipmentEntity:     (equipment_onto.PumpEntity, equipment_weight),
    CaseAttributes.Event:               (effect_onto.PumpRunningDry, event_weight),
    CaseAttributes.Apparatus:           (equipment_onto.PumpCasing, apparatus_weight),
    CaseAttributes.IntendedFunction:    (process_onto.MaterialTransfer, intended_function_weight),
    CaseAttributes.SubstancePhase:      (substance_onto.Liquid, phase_weight),
    CaseAttributes.InferredDeviation:   [deviation_onto.HighTemperature,
                                         deviation_onto.HighVibration]},
    
    {CaseAttributes.No: 2,
    CaseAttributes.EquipmentEntity:     (equipment_onto.PumpEntity, equipment_weight),
    CaseAttributes.Event:               (causes_onto.EntrainedAir, event_weight),
    CaseAttributes.Apparatus:           (equipment_onto.PumpCasing, apparatus_weight),
    CaseAttributes.IntendedFunction:    (process_onto.MaterialTransfer, intended_function_weight),
    CaseAttributes.SubstancePhase:      (substance_onto.Liquid, phase_weight),
    CaseAttributes.InferredDeviation:   [deviation_onto.NoFlow,
                                         deviation_onto.LowFlow]},
    
    {CaseAttributes.No: 3,
    CaseAttributes.EquipmentEntity:     (equipment_onto.StorageTankEntity, equipment_weight),
    CaseAttributes.Event:               (effect_onto.VolumetricDisplacement, event_weight),
    CaseAttributes.Apparatus:           (equipment_onto.AtmosphericStorageTank, apparatus_weight),
    CaseAttributes.IntendedFunction:    (process_onto.Storage, intended_function_weight),
    CaseAttributes.SubstancePhase:      (substance_onto.Multiphase, phase_weight),
    CaseAttributes.InferredDeviation:   [deviation_onto.HighPressure]},
    
    {CaseAttributes.No: 4,
    CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
    CaseAttributes.Event: (effect_onto.FluidCirculatesInsidePump, event_weight),
    CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
    CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
    CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
    CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    
    {CaseAttributes.No: 5,
    CaseAttributes.EquipmentEntity: (None, equipment_weight),
    CaseAttributes.Event: (effect_onto.Overfilling, event_weight),
    CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
    CaseAttributes.IntendedFunction: (None, intended_function_weight),
    CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
    CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    
    {CaseAttributes.No: 6,
    CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
    CaseAttributes.Event: (effect_onto.Cavitation, event_weight),
    CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
    CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
    CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
    CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    
    {CaseAttributes.No: 7,
    CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
    CaseAttributes.Event: (causes_onto.DeadHeadingOfPump, event_weight),
    CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
    CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
    CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
    CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    
    {CaseAttributes.No: 8,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 9,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    
    {CaseAttributes.No: 10,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighFlow]},
    
    {CaseAttributes.No: 11,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    
    {CaseAttributes.No: 12,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]}, 

    {CaseAttributes.No: 13,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    
    {CaseAttributes.No: 14,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]},
    
    {CaseAttributes.No: 15,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow, deviation_onto.LowPressure]},
    
    {CaseAttributes.No: 16,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.UnintendedExothermicPolymerization, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature, deviation_onto.HighPressure,
     deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 17,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.UnintendedExothermicPolymerization, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature, deviation_onto.HighPressure,
     deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 18,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.UnintendedExothermicPolymerization, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature, deviation_onto.HighPressure,
     deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 19,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.UnintendedExothermicPolymerization, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature, deviation_onto.HighPressure,
     deviation_onto.NoFlow]},
    # === Overfilling
    {CaseAttributes.No: 20,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.Overfilling, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.ElsewhereFlow]},
    
    {CaseAttributes.No: 21,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.Overfilling, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.ElsewhereFlow]},
    # === ConnectionPipeEntity
    {CaseAttributes.No: 22,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.UnintendedExothermicPolymerization, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 23,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.AbnormalEvaporation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    
    {CaseAttributes.No: 24,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.AbnormalEvaporation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    
    {CaseAttributes.No: 25,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.Fracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 26,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.Fracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 27,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.Fracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]}, 
    
    {CaseAttributes.No: 28,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.Fracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 29,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (causes_onto.WaterHammer, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    
    {CaseAttributes.No: 30,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.BrittleFracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 31,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.FatigueFracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 32,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.Fracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    
    {CaseAttributes.No: 33,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.Fracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    
    {CaseAttributes.No: 34,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.Fracture, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    
    {CaseAttributes.No: 35,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 36,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 37,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    
    {CaseAttributes.No: 38,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighVibration, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    
    {CaseAttributes.No: 39,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighVibration, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    
    {CaseAttributes.No: 40,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighVibration, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    
    {CaseAttributes.No: 41,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighFlow, deviation_onto.HighVibration]},
    
    {CaseAttributes.No: 42,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighFlow]}, 
    
    {CaseAttributes.No: 43,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighFlow, deviation_onto.HighVibration]},
    
    {CaseAttributes.No: 44,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    
    {CaseAttributes.No: 45,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    
    {CaseAttributes.No: 46,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    
    {CaseAttributes.No: 47,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    
    {CaseAttributes.No: 48,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    
    {CaseAttributes.No: 49,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    
    {CaseAttributes.No: 50,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    
    {CaseAttributes.No: 51,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    {CaseAttributes.No: 52,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    {CaseAttributes.No: 53,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.ReverseFlow]},
    {CaseAttributes.No: 54,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.ReverseFlow]},
    {CaseAttributes.No: 55,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    {CaseAttributes.No: 56,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    {CaseAttributes.No: 57,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    {CaseAttributes.No: 58,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]}, 
    
    {CaseAttributes.No: 59,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]},
    {CaseAttributes.No: 60,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]},
    {CaseAttributes.No: 61,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 62,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 63,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 64,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    {CaseAttributes.No: 65,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 66,
     CaseAttributes.EquipmentEntity: (equipment_onto.ConnectionPipeEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure, deviation_onto.LowFlow]},
    # === Pressure vessel
    {CaseAttributes.No: 67,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.IncompleteEvaporation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Evaporation, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    {CaseAttributes.No: 68,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.AbnormalEvaporation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 69,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.AbnormalEvaporation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 70,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.HeatBuildUp, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 71,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.HeatBuildUp, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 72,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.AbnormalEvaporation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    # {CaseAttributes.No: 73,
    # CaseAttributes.EquipmentEntity: (None, equipment_weight),
    # CaseAttributes.Event: (effect_onto.PressureSurge, event_weight),
    # CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
    # CaseAttributes.IntendedFunction: (None, intended_function_weight),
    # CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
    # CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 74,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.AbnormalEvaporation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]}, 
    
    # === Vacuum formation
    {CaseAttributes.No: 75,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 76,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    # === Internal Leakage
    {CaseAttributes.No: 77,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (causes_onto.InternalLeakage, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    # == Fracture -> Low level, nicht relevant, since leakage is relevant in case of a Fracture
    {CaseAttributes.No: 78,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 79,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    # == Low pressure in Tank
    {CaseAttributes.No: 80,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 81,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 82,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 83,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 84,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 85,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 86,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 87,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowLevel, event_weight),
     CaseAttributes.Apparatus: (None, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 88,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 89,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 90,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]}, 
    
    {CaseAttributes.No: 91,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 92,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 93,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 94,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 95,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 96,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 97,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 98,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 99,
     CaseAttributes.EquipmentEntity:    (None, equipment_weight),
     CaseAttributes.Event:              (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus:          (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction:   (None, intended_function_weight),
     CaseAttributes.SubstancePhase:     (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 100,
     CaseAttributes.EquipmentEntity:    (None, equipment_weight),
     CaseAttributes.Event:              (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus:          (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction:   (None, intended_function_weight),
     CaseAttributes.SubstancePhase:     (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 101,
     CaseAttributes.EquipmentEntity:    (None, equipment_weight),
     CaseAttributes.Event:              (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus:          (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction:   (None, intended_function_weight),
     CaseAttributes.SubstancePhase:     (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    {CaseAttributes.No: 102,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    # === Compressor
    {CaseAttributes.No: 103,
     CaseAttributes.EquipmentEntity: (equipment_onto.CompressorEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow, deviation_onto.LowPressure]},
    {CaseAttributes.No: 104,
     CaseAttributes.EquipmentEntity: (equipment_onto.CompressorEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]},
    {CaseAttributes.No: 105,
     CaseAttributes.EquipmentEntity: (equipment_onto.CompressorEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    {CaseAttributes.No: 106,
     CaseAttributes.EquipmentEntity: (equipment_onto.CompressorEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]},#]}, 
        
        
    {CaseAttributes.No: 107,
     CaseAttributes.EquipmentEntity: (equipment_onto.CompressorEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow, deviation_onto.LowPressure]},
    {CaseAttributes.No: 108,
     CaseAttributes.EquipmentEntity: (equipment_onto.CompressorEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow, deviation_onto.LowPressure]},
    {CaseAttributes.No: 109,
     CaseAttributes.EquipmentEntity: (equipment_onto.CompressorEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    # === Valve
    {CaseAttributes.No: 110,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.Cavitation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    # {CaseAttributes.No: 111,
    # CaseAttributes.EquipmentEntity: (None, equipment_weight),
    # CaseAttributes.Event: (effect_onto.PressureSurge, event_weight),
    # CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
    # CaseAttributes.IntendedFunction: (None, intended_function_weight),
    # CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
    # CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 112,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.Cavitation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    {CaseAttributes.No: 113,
     CaseAttributes.EquipmentEntity: (equipment_onto.AirCooledCondenserEntity, equipment_weight),
     CaseAttributes.Event: (causes_onto.NonCondensables, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Casing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Condensation, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 114,
     CaseAttributes.EquipmentEntity: (equipment_onto.PumpEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.UnintendedExothermicPolymerization, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PumpCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Transport, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    # === Compressor
    {CaseAttributes.No: 115,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.ExcessiveDischargeTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    {CaseAttributes.No: 116,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.IncreasedOilDischarge, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.CompressorCasing, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.MaterialTransfer, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    # === Dev to Dev Cases========================================================
    {CaseAttributes.No: 117,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]},
    {CaseAttributes.No: 118,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]},
    {CaseAttributes.No: 119,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowTemperature]},
    {CaseAttributes.No: 120,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    {CaseAttributes.No: 121,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
        
    {CaseAttributes.No: 122,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighTemperature]},
    {CaseAttributes.No: 123,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 124,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 125,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 126,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 127,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 128,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 129,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighFlow]},
    {CaseAttributes.No: 130,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighFlow]},
    {CaseAttributes.No: 131,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighFlow]},
    {CaseAttributes.No: 132,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 133,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 134,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowPressure, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 135,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    {CaseAttributes.No: 136,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    
    {CaseAttributes.No: 137,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    {CaseAttributes.No: 138,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighVibration, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    {CaseAttributes.No: 139,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighVibration, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    {CaseAttributes.No: 140,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighVibration, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighVibration]},
    {CaseAttributes.No: 141,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    {CaseAttributes.No: 142,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    {CaseAttributes.No: 143,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    {CaseAttributes.No: 144,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 145,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    {CaseAttributes.No: 146,
     CaseAttributes.EquipmentEntity: (equipment_onto.ValveEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.Body, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow, deviation_onto.LowPressure]},
    {CaseAttributes.No: 147,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 148,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 149,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 150,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 151,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.ElsewhereFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 152,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]}, 
    
    {CaseAttributes.No: 153,
     CaseAttributes.EquipmentEntity: (equipment_onto.StorageTankEntity, equipment_weight),
     CaseAttributes.Event: (effect_onto.AbnormalEvaporation, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 154,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 155,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 156,
     CaseAttributes.EquipmentEntity: (equipment_onto.InertgasBlanketingEntity, equipment_weight),
     CaseAttributes.Event: (causes_onto.IncreasedInletPressure, event_weight),
     CaseAttributes.IntendedFunction: (process_onto.Inertization, intended_function_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 157,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 158,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 159,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 160,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighTemperature, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 161,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighLevel]},
    {CaseAttributes.No: 162,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighLevel]},
    {CaseAttributes.No: 163,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighLevel]},
    {CaseAttributes.No: 164,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 165,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 166,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 167,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 168,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    
    
    {CaseAttributes.No: 169,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 170,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 171,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighLevel, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    # === Source
    {CaseAttributes.No: 172,
     CaseAttributes.EquipmentEntity: (equipment_onto.SourceEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (None, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.NoFlow]},
    {CaseAttributes.No: 173,
     CaseAttributes.EquipmentEntity: (equipment_onto.SourceEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (None, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowFlow]},
    {CaseAttributes.No: 174,
     CaseAttributes.EquipmentEntity: (equipment_onto.SourceEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (None, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighFlow]},
    {CaseAttributes.No: 175,
     CaseAttributes.EquipmentEntity: (equipment_onto.SourceEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.OtherThanComposition, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (None, intended_function_weight),
     CaseAttributes.SubstancePhase: (None, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]},
    
    # === Settling tank
    {CaseAttributes.No: 176,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.BacteriaGrowth, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighCorrosion]},
    {CaseAttributes.No: 177,
     CaseAttributes.EquipmentEntity: (equipment_onto.SettlingTankEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.LowFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Separation, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 178,
     CaseAttributes.EquipmentEntity: (equipment_onto.SettlingTankEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Separation, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowLevel]},
    {CaseAttributes.No: 179,
     CaseAttributes.EquipmentEntity: (equipment_onto.SettlingTankEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Separation, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Liquid, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighLevel, deviation_onto.HighFlow]},
    {CaseAttributes.No: 180,
     CaseAttributes.EquipmentEntity: (equipment_onto.SettlingTankEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Separation, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighLevel, deviation_onto.HighFlow]},
    # === Inertgas blanketing unit
    {CaseAttributes.No: 181,
     CaseAttributes.EquipmentEntity: (equipment_onto.InertgasBlanketingEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.NoFlow, event_weight),
     CaseAttributes.IntendedFunction: (process_onto.Inertization, intended_function_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.LowPressure]},
    {CaseAttributes.No: 182,
     CaseAttributes.EquipmentEntity: (equipment_onto.InertgasBlanketingEntity, equipment_weight),
     CaseAttributes.Event: (deviation_onto.HighFlow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.NoApparatus, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Inertization, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Gaseous, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighPressure]},
    {CaseAttributes.No: 183,
     CaseAttributes.EquipmentEntity: (None, equipment_weight),
     CaseAttributes.Event: (effect_onto.BacteriaGrowth, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.AtmosphericStorageTank, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Storage, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.HighCorrosion]},
    {CaseAttributes.No: 184,
     CaseAttributes.EquipmentEntity: (equipment_onto.SettlingTankEntity, equipment_weight),
     CaseAttributes.Event: (causes_onto.ExcessiveInflow, event_weight),
     CaseAttributes.Apparatus: (equipment_onto.PressureVessel, apparatus_weight),
     CaseAttributes.IntendedFunction: (process_onto.Separation, intended_function_weight),
     CaseAttributes.SubstancePhase: (substance_onto.Multiphase, phase_weight),
     CaseAttributes.InferredDeviation: [deviation_onto.OtherThanComposition]}, 
] 

    
    
def calculate_similarity(new_case, old_case):
    
    if new_case is None or old_case is None:
        print("Similarity could not be calculated because of None")
        return 0
    # else:
        
    attr_list = [   CaseAttributes.EquipmentEntity,
                    CaseAttributes.Event,
                    CaseAttributes.Apparatus,
                    CaseAttributes.IntendedFunction,
                    CaseAttributes.SubstancePhase
                ]
    similarities = []
    weights = []
    sum_of_weights = 0
    
    for attr in attr_list:
        if old_case.get(attr)[0]:
            similarities.append(similar(new_case.get(attr), old_case.get(attr)[0]))
        else:
            similarities.append(0)
            weights.append(old_case.get(attr)[1])
            sum_of_weights += old_case.get(attr)[1]
    similarity_products = [a * b for a, b in zip(similarities, weights)]
    sum_ = sum(similarity_products)
    
    # Overall similarity
    similarity = 1 / sum_of_weights * sum_
    
    return similarity

def match_case_with_cb(current_case, case_base):
    list_similarities = []
    
    for case in case_base:
        list_similarities.append((calculate_similarity(current_case, case), case.get(CaseAttributes.InferredDeviation)))

    res_list = [x[0] for x in list_similarities]
    max_similarity_measure = max(res_list)
    
    if max_similarity_measure >= 0.75:
        index = res_list.index(max_similarity_measure)
        relevant_deviation = list_similarities[index][1]
    else:
        relevant_deviation = None
        
    return relevant_deviation




#%% Appendix G - Ontology for Causes



# ===Cause ========================================
class Cause(Thing):
    pass
Cause.label = ["cause"] #TODO
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






#%% Appendix H - Ontology for Deviations

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





#%% Appendix I - Ontology for Equipment

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
#TODO
AllDisjoint([Operator, ProgrammableLogicController, NotControlled]) #TODO
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


#%% Appendix J - Ontology for Chemicals

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






#%% Appendix K - Ontology for Causes


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
 
 
 
 
#%% Appendix L - Ontology for Causes

class ReducedFlowArea(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity) &
 isCauseOfDeviation.some(deviation_onto.LowFlow))]
class HosePipeBlocked(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causeInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity &
 equipment_onto.hasPiping.some(equipment_onto.TankTruckHose)))]
class PhysicalImpact(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.ElsewhereFlow) &
 causeInvolvesSiteInformation.some(
 site_information.involvesPlantAmbientInformation.some(site_information.VehicleTraffic |
 site_information.CranePresent)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))]
class MechanicalFailureOfSupport(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.ElsewhereFlow) &
 causeRequiresBoundaryCondition.some(boundary_onto.FoundationCanBeAffected) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))]
class Pollution(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities) &
 causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank |
 equipment_onto.PressureVessel)))]
class NoFeed(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity |
 equipment_onto.ReactorEntity))]
class WrongMountingOfNonReturnValve(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.NonReturnValve))
 )]
# Unit tests conducted @200414 [TestFreezeUp] in unit_tests\overarching_phenomena.py
class FreezeUp(Cause):
 equivalent_to = [Cause &
 (causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid) &
 (substance_onto.hasFreezingPointInKelvin >= upper_onto.lowest_ambient_temperature)
 )
 &
 causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity) &
 isCauseOfDeviation.some(deviation_onto.LowTemperature))]
FreezeUp.comment = ["[FreezeUp] is seen as a cause for no flow.",
 "It can also be modeled as an [Effect] (T_low & pipe -> [FreezeUp])",
"The modelling is consequence-oriented, thus (T_low & pipe -> [PipeFracture])"]
class ValveClosedPressureBuildUpInPiping(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.ShutOffValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))
 |
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))
 |
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.PressureControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.PressureControl)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))]
class DrainValveInadvertentlyOpened(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow |
 equipment_onto.NormalOperation)) &
 causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow)))]
class LiquidTransferWithoutCompensation(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Emptying)) &
 causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.LowPressure))
 ]
class InsufficientThermalInbreathing(Cause):
 equivalent_to = [Cause &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 isCauseOfDeviation.some(deviation_onto.LowPressure)
 ]



class InsufficientThermalOutbreathing(Cause):
 equivalent_to = [Cause &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure)]
class NoInertgasSupply(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causeInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Inerting)) &
 causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.InertGas)))]
class IncreasedInletPressure(Cause):
 equivalent_to = [Cause &
 ((isCauseOfDeviation.some(deviation_onto.HighFlow) &
 causeInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Inerting)) &
 causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.InertGas))))]
class IncorrectPressureAdjustment(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.LowPressure) &
 causeInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent) &
 equipment_onto.hasPiping.some(equipment_onto.BlanketingGasline) &
 equipment_onto.hasInstrumentation.some(equipment_onto.PressureIndicatorController)))]
class BlockedOutflowLine(Cause):
 equivalent_to = [Cause &
 (
 (causeInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity |
 equipment_onto.AirCooledCondenserEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.FinTubeEvaporatorEntity) &
 isCauseOfDeviation.some(deviation_onto.NoFlow |
 deviation_onto.HighPressure))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 isCauseOfDeviation.some(deviation_onto.NoFlow |
 deviation_onto.HighPressure) &
 causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 isCauseOfDeviation.some(deviation_onto.HighLevel) &
 causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium))))]
class TooLittleStabilizer(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causeInvolvesEquipmentEntity.some((equipment_onto.ConnectionPipeEntity |
 equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.FinTubeEvaporatorEntity)) &
 causeRequiresBoundaryCondition.some(boundary_onto.SubstanceContainsStabilizer) &
 causeInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(substance_onto.PolymerizesExothermicallyWithoutInhibitor)))]
class TooLittleInhibitor(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causeInvolvesEquipmentEntity.some((equipment_onto.ConnectionPipeEntity |
 equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.FinTubeEvaporatorEntity)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(substance_onto.PolymerizesExothermicallyWithoutInhibitor)))]
class ExcessiveFluidWithdrawal(Cause):
 equivalent_to = [Cause &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity) &
 isCauseOfDeviation.some(deviation_onto.LowPressure)]
ExcessiveFluidWithdrawal.comment = ["The issue of depressurization and collapse of vessel is addressed",
 "https://www.aiche.org/resources/publications/cep/2019/december/protect-tanks-overpressure-and-vacuum",
"API 2000"]
class WaterHammer(Cause):
 equivalent_to = [Cause &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid) &
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure) &
 causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling |
 process_onto.ModeIndependent))]
WaterHammer.comment = ["Synonyms: hydraulic shock, fluid hammer"]
class ThermalExpansion(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase |
 substance_onto.Gaseous) &
substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causeRequiresBoundaryCondition.some(boundary_onto.ExternalFirePossible |
 boundary_onto.LocatedOutside) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))
 |
 (causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase |
 substance_onto.Gaseous) &
substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)
 ) &
 causeRequiresBoundaryCondition.some(boundary_onto.ExternalFirePossible |
 boundary_onto.LocatedOutside) &
 isCauseOfDeviation.some(deviation_onto.HighPressure)))]



class HighAmbientTemperature(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 isCauseOfDeviation.some(deviation_onto.HighTemperature |
 deviation_onto.HighPressure) &
 causeRequiresBoundaryCondition.some(boundary_onto.LocatedOutside))]
class WrongRotatingSpeed(Cause):
 equivalent_to = [Cause &
 (
 (isCauseOfDeviation.some(deviation_onto.HighFlow |
 deviation_onto.LowFlow) &
 causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)) &
 causeInvolvesEquipmentEntity.some((equipment_onto.CompressorEntity |
 equipment_onto.PumpEntity) &
 equipment_onto.hasInstrumentation.some(equipment_onto.FrequencyConverter) &
 equipment_onto.hasInstrumentation.some(equipment_onto.SpeedController) &
 equipment_onto.hasInstrumentation.some(equipment_onto.ElectricMotor)))
 |
 (isCauseOfDeviation.some(
 deviation_onto.HighPressure | deviation_onto.HighTemperature) &
 causeInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity &
 equipment_onto.hasInstrumentation.some(equipment_onto.ElectricMotor) &
 equipment_onto.hasInstrumentation.some(equipment_onto.SpeedController) &
 equipment_onto.hasInstrumentation.some(equipment_onto.FrequencyConverter))
 ))]
class ConfusionOfSubstances(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesEquipmentEntity.some(equipment_onto.SourceEntity &
 equipment_onto.entityControlledBy.some(equipment_onto.Operator)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition)))]
class WrongTankLinedUp(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))]
class OtherSubstanceFromUpstream(Cause):
 equivalent_to = [Cause &
 ((causeRequiresBoundaryCondition.some(boundary_onto.UpstreamProcessInvolved) &
 causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.SourceEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))
 |
 ((causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.InertGas)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Inerting)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))))]
class ReducedDwellTime(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causeInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating)))]
class ContaminationInUnloadingLines(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some((equipment_onto.hasPiping.some(
 equipment_onto.TankTruckHose)) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading)) &
 causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities |
 boundary_onto.IntroductionOfWater) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))]
class InadvertentContamination(Cause):
 equivalent_to = [Cause &
 ((causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities) &
 causeInvolvesEquipmentEntity.some((equipment_onto.SourceEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureReceiverEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))
 |
 (causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities) &
 causeInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition)))]
class ContaminationByWaterAndTemperatureFallsBelowFreezingPoint(Cause):
 equivalent_to = [Cause &
 (causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfWater) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(
 equipment_onto.AtmosphericStorageTank |
 equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing | process_onto.ModeIndependent)) &
 causeInvolvesSecondDeviation.some(deviation_onto.OtherThanComposition) &
 isCauseOfDeviation.some(deviation_onto.LowTemperature))]
class ContaminationByWater(Cause):
 equivalent_to = [Cause &
 ((causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfWater) &
 causeInvolvesEquipmentEntity.some((equipment_onto.SettlingTankEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.FinTubeEvaporatorEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent |
 process_onto.Filling)
 ) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition))
 |
 (causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfWater) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing |
 process_onto.Filling)) &
 isCauseOfDeviation.some(deviation_onto.OtherThanComposition)))]
 
 
class MaterialDegradation(Cause):
 equivalent_to = [Cause &
 (isCauseOfDeviation.some(deviation_onto.HighVibration) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(
 equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank |
 equipment_onto.Piping)))]
class ExternalLeakage(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Gaseous)) & # liquid: because lubricant
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (isCauseOfDeviation.some(deviation_onto.HighCorrosion) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))
 |
 (causeInvolvesEquipmentEntity.some((equipment_onto.PressureReceiverEntity |
 equipment_onto.FinTubeEvaporatorEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.AirCooledCondenserEntity |
 equipment_onto.WetScrubberEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.TankTruckEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Gaseous |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve |
 equipment_onto.ThreeWayValve |
 equipment_onto.ShutOffValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Gaseous |
 substance_onto.Multiphase)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Gaseous |
 substance_onto.Multiphase) &
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 isCauseOfDeviation.some(deviation_onto.ElsewhereFlow)))]
class InternalLeakage(Cause):
 equivalent_to = [Cause &
 ((isCauseOfDeviation.some(deviation_onto.ElsewhereFlow |
 deviation_onto.OtherThanComposition) &
 causeInvolvesEquipmentEntity.some(equipment_onto.hasFixture.some(equipment_onto.HalfPipeCoilJacket |
 equipment_onto.Jacket |
 equipment_onto.PlatePackage) |
 equipment_onto.hasPiping.some(equipment_onto.TubeCoil |
 equipment_onto.TubeBundle)))
 |
 (isCauseOfDeviation.some(deviation_onto.ElsewhereFlow) &
 causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity |
 equipment_onto.SteamDrivenReboilerEntity)))]
class ClosedOutletValve(Cause):
 equivalent_to = [Cause &
 (
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.OutletValve) &
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 isCauseOfDeviation.some(deviation_onto.HighPressure))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.OutletValve) &
 equipment_onto.hasApparatus.some(equipment_onto.Compressor)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 isCauseOfDeviation.some(deviation_onto.NoFlow | deviation_onto.HighPressure))))]
ClosedOutletValve.comment = ["Pump specific details are covered in pump ontology"]
class ClosedInletValve(Cause):
 equivalent_to = [Cause &
 ((causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.InletValve) &
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank)) &
 causeInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 isCauseOfDeviation.some(deviation_onto.LowLevel | deviation_onto.NoFlow))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasInstrumentation.some(equipment_onto.InletValve) &
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 isCauseOfDeviation.some(deviation_onto.LowPressure))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity &
 equipment_onto.hasInstrumentation.some(equipment_onto.InletValve)) &
 causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 isCauseOfDeviation.some(deviation_onto.NoFlow |
 deviation_onto.LowPressure))
 |
 (causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasInstrumentation.some(equipment_onto.InletValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow)) &
 isCauseOfDeviation.some(deviation_onto.NoFlow)))]
ClosedInletValve.comment = ["Pump specific details are covered in pump ontology"] 



class LossOfCooling(Cause):
 equivalent_to = [Cause &
 (causeInvolvesEquipmentEntity.some(equipment_onto.hasSubunit.some(equipment_onto.CoolingSystem)) &
 isCauseOfDeviation.some(deviation_onto.HighTemperature))]
class DeliveryOfHighVolatilityComponents(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 causes_onto.causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)))]
class BlockedReboilerLines(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)))]
class MalfunctionLubricationSystem(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.Lubricant)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity &
 equipment_onto.hasSubunit.some(equipment_onto.LubricationSystem)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))]
MalfunctionLubricationSystem.comment = ["Issues described in 'How to limit fire and explosion hazards with oil-flooded rotary screw compressors' by Steven J. Luzik"]
class InsufficientVentilation(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))]
class NoSteamFlow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))]
class LessSteamFlow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.LowFlow) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))]
class MoreSteamFlow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow) &
 causes_onto.causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))]
class NonCondensables(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 causes_onto.causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfAir) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition))]
NonCondensables.comment = ["Eigentlich wird hier noch high pressure benötigt"]
class Fouling(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 causes_onto.causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfImpurities) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ShellTubeEvaporatorEntity) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature |
 deviation_onto.OtherThanComposition)))]
class IncorrectSetPointControlValve(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow |
 deviation_onto.NoFlow |
 deviation_onto.LowFlow))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.PressureControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.PressureControl)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighPressure |
 deviation_onto.LowPressure)))]
class BypassOpened(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasSubunit.some(equipment_onto.Bypass) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow))
 ]
class ValveIntactUnintentionallyClosed(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some((equipment_onto.ValveEntity |
 equipment_onto.InertgasBlanketingEntity) &
 equipment_onto.hasInstrumentation.some(
 equipment_onto.FlowControlValve |
 equipment_onto.PressureControlValve |
 equipment_onto.ShutOffValve |
 equipment_onto.ThreeWayValve) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 (equipment_onto.hasInstrumentation.some(equipment_onto.OutletValve) |
 equipment_onto.hasInstrumentation.some(equipment_onto.InletValve)) &
 causes_onto.isCauseOfDeviation.some(
 deviation_onto.NoFlow |
 deviation_onto.HighTemperature))
 ))]


class ValveStuckOpen(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ValveEntity &
 equipment_onto.hasInstrumentation.some(
 equipment_onto.FlowControlValve |
 equipment_onto.PressureControlValve) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.FlowControl |
 process_onto.PressureControl)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel)))]
class ValvePartiallyOpened(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ValveEntity &
 equipment_onto.hasInstrumentation.some(
 equipment_onto.ShutOffValve)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowFlow))]
class PluggedRestrictionOrifice(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.Orifice) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow))]
class ValveWronglyClosed(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow))]
class ValveWronglyOpened(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.FlowControlValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl |
 process_onto.ModeIndependent)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow))]
class PumpingAgainstPolymerizedLine(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWhenExposedToLight |
 substance_onto.PolymerizesExothermicallyWhenExposedToHeat |
 substance_onto.PolymerizesExothermicallyWithoutInhibitor)) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)))]
class ImpellerFault(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowFlow))]
class WrongImpeller(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow))]
class MissingImpeller(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasFixture.some(
 equipment_onto.Impeller) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow))]
class PumpOperationFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.ReverseFlow)))]
class PumpIncorrectlySet(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow)]
class OperationBelowMinimumFlowRate(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)
 ) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowFlow))]
class EntrainedAir(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.causeRequiresBoundaryCondition.some(boundary_onto.IntroductionOfAir) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition))] 


class DeadHeadingOfPump(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasInstrumentation.some(
 equipment_onto.OutletValve) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow |
 equipment_onto.NormalOperation)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow)))]
DeadHeadingOfPump.comment = ["Occurs when the pump's discharge is closed (blockage or closed valve)"]
class InsufficientNPSH(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowPressure))]
class PumpSealFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.ElsewhereFlow)))]
class ChargingFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition |
 deviation_onto.OtherSequence) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ReactorEntity))]
class DosingFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.isCauseOfDeviation.some(deviation_onto.OtherThanComposition |
 deviation_onto.OtherSequence) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ReactorEntity))]
class AbnormalHeatInput(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesEquipmentEntity.some((equipment_onto.PressureVesselEntity |
 equipment_onto.PlateHeatExchangerEntity |
 equipment_onto.AirCooledCondenserEntity |
 equipment_onto.ShellTubeHeatExchangerEntity |
 equipment_onto.ConnectionPipeEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent |
 process_onto.Storing)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling |
 process_onto.Storing)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasSubunit.some(equipment_onto.HeatingSystem)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature)))]
class LeakingDrainValve(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.ElsewhereFlow))]
class AbruptReliefOfContent(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity |
 equipment_onto.hasApparatus.some(
 equipment_onto.PressureVessel))) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowTemperature))]
AbruptReliefOfContent.comment = ["Abrupt relief can lead to ignition of flammable mixture"]
class CoolingFailure(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasSubunit.some(equipment_onto.CoolingSystem)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighTemperature))]
class BlockedInflowLine(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowPressure) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow | deviation_onto.LowFlow |
 deviation_onto.LowLevel | deviation_onto.LowPressure))
 |
 (causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 causes_onto.causeInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.NoFlow)))]

class ExcessiveInflow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous |
 substance_onto.Multiphase |
 substance_onto.Liquid)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(
 substance_onto.Liquid | substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank |
 equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling))
 )
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighFlow) &
 causes_onto.causeInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Inerting)
 )
 )
 )
 ]
class LossOfInflow(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)
 ))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ))
 )
 ]
class IncorrectIndicationOfFillingLevel(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 ((causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)))
 |
 (causes_onto.causeInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.HighLevel) &
 causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)))
 )
 ]
class IncorrectFilling(causes_onto.Cause):
 equivalent_to = [causes_onto.Cause &
 (causes_onto.causeInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank) &
 equipment_onto.entityControlledBy.some(equipment_onto.Operator) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)) &
 causes_onto.isCauseOfDeviation.some(deviation_onto.LowLevel |
 deviation_onto.HighLevel |
 deviation_onto.LowFlow |
 deviation_onto.HighFlow))]







#%% Appendix M - Ontology for Effects

class BackContaminationOfSupply(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity) &
 isEffectOfDeviation.some(deviation_onto.ReverseFlow)))]
class InsufficientFilling(Effect):
 equivalent_to = [Effect & (
 (effectImpliedByCause.some(causes_onto.BlockedInflowLine | causes_onto.LossOfInflow) &
 isEffectOfDeviation.some(deviation_onto.NoFlow | deviation_onto.LowLevel) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)))
 |
 (isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectOfPropagatedCause.value(True) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling))))]
     
class UnintendedExothermicPolymerization(Effect):
 equivalent_to = [Effect &
 (
 (effectInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWithoutInhibitor) &
 effectImpliedByCause.some(causes_onto.TooLittleStabilizer |
 causes_onto.TooLittleInhibitor |
 causes_onto.InadvertentContamination) &
 effectInvolvesEquipmentEntity.some((equipment_onto.ConnectionPipeEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)
 )))
 |
 (effectInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWhenExposedToHeat)) &
 effectImpliedByCause.some(causes_onto.AbnormalHeatInput) &
 effectImpliedByUnderlyingcause.some(causes_onto.ExternalFire) &
 effectInvolvesEquipmentEntity.some((equipment_onto.ConnectionPipeEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent))
 )
 |
 (effectInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.PolymerizesExothermicallyWithoutInhibitor)) &
 isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 effectImpliedByCause.some(causes_onto.TooLittleInhibitor)
 )
 )]
class PotentialViolentReactionWithOxidizers(Effect):
 equivalent_to = [Effect &
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.AtmosphericStorageTank) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStabilityReactivityInformation.some(
 substance_onto.ReactsViolentlyWithOxidizer |
 substance_onto.IncompatibleToStrongOxidizers)) &
 isEffectOfDeviation.some(deviation_onto.OtherThanComposition) &
 effectImpliedByCause.some(causes_onto.WrongTankLinedUp |
 causes_onto.ConfusionOfSubstances))]
class AbnormalEvaporation(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase) &
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)
 ) &
 effectImpliedByUnderlyingcause.some(causes_onto.ExternalFire) &
 isEffectOfDeviation.some(deviation_onto.HighTemperature))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling |
 process_onto.Storing)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectImpliedByCause.some(causes_onto.AbnormalHeatInput))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.PressureVessel &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling |
 process_onto.Storing)) &
 effectInvolvesSubstance.some(substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectImpliedByCause.some(causes_onto.AbnormalHeatInput))
 |
 (isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effectInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity) &
 effectImpliedByCause.some(causes_onto.MoreSteamFlow))
 |
 (effectImpliedByCause.some(causes_onto.DeliveryOfHighVolatilityComponents) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity))
 )]


class AccumulationOfImpurities(Effect):
 equivalent_to = [Effect &
 (effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)) &
 effectImpliedByCause.some(causes_onto.ContaminationInUnloadingLines |
 causes_onto.InadvertentContamination) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectOfPropagatedCause.value(True) &
 isEffectOfDeviation.some(deviation_onto.OtherThanComposition))]
class BacteriaGrowth(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectImpliedByCause.some(causes_onto.ContaminationByWater) &
 isEffectOfDeviation.some(deviation_onto.OtherThanComposition)
 )
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Storing)) &
 effectImpliedByCause.some(causes_onto.ContaminationInUnloadingLines |
 causes_onto.InadvertentContamination) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectOfPropagatedCause.value(True) &
 isEffectOfDeviation.some(deviation_onto.OtherThanComposition)))]
class GenerationOfElectrostaticCharge(Effect):
 equivalent_to = [Effect &
 (effectInvolvesEquipmentEntity.some((equipment_onto.TankTruckEntity |
 equipment_onto.ConnectionPipeEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Unloading |
 process_onto.ModeIndependent)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isEffectOfDeviation.some(deviation_onto.HighFlow))]
class Overfilling(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isEffectOfDeviation.some(deviation_onto.HighLevel))
 |
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel) &
 equipment_onto.hasPiping.some(equipment_onto.VentPipe) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling |
 process_onto.ModeIndependent)) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 isEffectOfDeviation.some(deviation_onto.HighLevel))
 |
 (isEffectOfDeviation.some(deviation_onto.HighFlow) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank |
 equipment_onto.OpenVessel) &
 equipment_onto.hasIntendedFunction.some(process_onto.Filling)) &
 effectImpliedByCause.some(causes_onto.BypassOpened |
 causes_onto.IncorrectSetPointControlValve |
 causes_onto.WrongImpeller |
 causes_onto.IncorrectFilling) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)))
 |
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank)) &
 effectImpliedByCause.some(causes_onto.IncorrectIndicationOfFillingLevel) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase))
 ))]

class PressureExceedingDesignPressure(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.HighPressure) &
 effectInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity |
 equipment_onto.hasApparatus.some(equipment_onto.PressureVessel)))
 |
 (effectInvolvesEquipmentEntity.some((equipment_onto.AirCooledCondenserEntity |
 equipment_onto.ShellTubeEvaporatorEntity |
 equipment_onto.SteamDrivenReboilerEntity |
 equipment_onto.FinTubeEvaporatorEntity |
 equipment_onto.CompressorEntity) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 effectImpliedByCause.some(causes_onto.BlockedOutflowLine))
 |
 (effectOfPropagatedCause.value(True) &
 isEffectOfDeviation.some(deviation_onto.HighPressure) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Filling | process_onto.Storing | process_onto.ModeIndependent)))
 |
 (isEffectOfDeviation.some(deviation_onto.HighPressure) &
 effectImpliedByCause.some(causes_onto.ThermalExpansion | causes_onto.InsufficientThermalOutbreathing) &
 effectInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity |
 equipment_onto.hasApparatus.some(
 equipment_onto.PressureVessel |
 equipment_onto.AtmosphericStorageTank)))
 |
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.ReciprocatingPump)) &
 effectImpliedByCause.some(causes_onto.DeadHeadingOfPump |
 causes_onto.PumpingAgainstPolymerizedLine))
 |
 (effectInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.FlowControl | process_onto.ModeIndependent)) &
 effectImpliedByCause.some(causes_onto.ValveClosedPressureBuildUpInPiping))
 |
 PotentialViolentReactionWithOxidizers)] 
 
 
class Fracture(Effect):
 equivalent_to = [Effect &
 (
 (effectImpliedByCause.some(causes_onto.PhysicalImpact) &
 isEffectOfDeviation.some(deviation_onto.ElsewhereFlow) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))
 |
 PressureExceedingDesignPressure)]
class FatigueFracture(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.HighVibration) &
 effectImpliedByCause.some(causes_onto.MaterialDegradation))
 |
 (isEffectOfDeviation.some(deviation_onto.HighVibration) &
 effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity))
 |
 (isEffectOfDeviation.some(deviation_onto.HighVibration) &
 effectInvolvesEquipmentEntity.some(equipment_onto.ConnectionPipeEntity)))]
class BrittleFracture(Effect):
 equivalent_to = [Effect &
 isEffectOfDeviation.some(deviation_onto.LowTemperature) &
 effectImpliedByCause.some(causes_onto.MaterialDegradation)]
BrittleFracture.comment = ["Source: Managing Cold Temperature and Brittle Fracture Hazards in Pressure "
 "Vessels by Daniel J. Benac, Nicholas Cherolis & David Wood",
 "Requires crack in high stress region",
"sudden and unexpected failure",
"https://www.psenterprise.com/sectors/oil-and-gas/brittle-fracture"]
class DrainlineFracture(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.OtherThanComposition) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.ModeIndependent)) &
 effectRequiresBoundaryCondition.some(
 boundary_onto.AmbientTemperatureCanDropBelowFreezingPoint))
 |
 (isEffectOfDeviation.some(deviation_onto.LowTemperature) &
 effectInvolvesSecondDeviation.some(deviation_onto.OtherThanComposition) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Multiphase |
 substance_onto.Liquid)) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve) &
 equipment_onto.hasIntendedFunction.some(process_onto.Storing | process_onto.ModeIndependent)))
 |
 (effectImpliedByCause.some(causes_onto.FreezeUp))
 |
 (isEffectOfDeviation.some(deviation_onto.LowTemperature) &
 effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasInstrumentation.some(equipment_onto.BottomDrainValve)) &
 effectRequiresBoundaryCondition.some(boundary_onto.IntroductionOfWater) &
 effectInvolvesSiteInformation.some(
 site_information.hasMinimumAmbientTemperatureInKelvin <= 273.15)))]
DrainlineFracture.comment = ["second part of definition accomplishes for double jeopardy, T_low and X_other"]
class InsufficientInertization(Effect):
 equivalent_to = [Effect &
 (effectInvolvesEquipmentEntity.some(equipment_onto.InertgasBlanketingEntity) &
 isEffectOfDeviation.some(deviation_onto.NoFlow |
 deviation_onto.OtherThanComposition) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.InertGas)))
 |
 (isEffectOfDeviation.some(deviation_onto.OtherThanComposition |
 deviation_onto.NoFlow) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasPiping.some(equipment_onto.BlanketingGasline) &
 equipment_onto.hasIntendedFunction.some(process_onto.Inerting)) &
 effectImpliedByCause.some(causes_onto.NoInertgasSupply |
 causes_onto.OtherSubstanceFromUpstream))]
class PoorSeparation(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.OtherThanComposition) &
 effectImpliedByCause.some(causes_onto.ConfusionOfSubstances |
 causes_onto.OtherSubstanceFromUpstream) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Separating)))
 |
 (isEffectOfDeviation.some(deviation_onto.OtherThanComposition) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectImpliedByCause.some(causes_onto.ReducedDwellTime) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.Separating)))
 |
 (effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effectImpliedByCause.some(causes_onto.BypassOpened |
 causes_onto.ValveWronglyOpened |
 causes_onto.IncorrectSetPointControlValve) &
 isEffectOfDeviation.some(deviation_onto.HighFlow) &
 effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating | process_onto.ModeIndependent)))
 )]
class PoolFormation(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 (effectImpliedByCause.some(causes_onto.ExternalLeakage |
 causes_onto.PumpSealFailure |
 causes_onto.DrainValveInadvertentlyOpened |
 causes_onto.HoseIncorrectlyConnected)))
 |
 (isEffectOfDeviation.some(deviation_onto.HighCorrosion) &
 effectOfPropagatedCause.value(True)))
 ] 
 
 
class EmptyingOfContainer(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Emptying)) &
 isEffectOfDeviation.some(deviation_onto.LowLevel | deviation_onto.NoFlow | deviation_onto.LowFlow) &
 effectImpliedByCause.some(causes_onto.LossOfInflow |
 causes_onto.IncorrectFilling |
 causes_onto.ClosedInletValve))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating)) &
 isEffectOfDeviation.some(deviation_onto.LowLevel | deviation_onto.NoFlow | deviation_onto.LowFlow) &
 effectImpliedByCause.some(causes_onto.LossOfInflow | causes_onto.ValveWronglyClosed |
 causes_onto.IncorrectFilling | causes_onto.ClosedInletValve))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Emptying)) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectOfPropagatedCause.value(True))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectOfPropagatedCause.value(True)))]
class LossOfMechanicalIntegrity(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity |
 equipment_onto.SettlingTankEntity |
 equipment_onto.WetScrubberEntity |
 equipment_onto.PressureVesselEntity |
 equipment_onto.PressureReceiverEntity |
 equipment_onto.ReactorEntity) &
 effectImpliedByCause.some(
 causes_onto.InsufficientThermalInbreathing |
 causes_onto.DrainValveInadvertentlyOpened))
 |
 (effectImpliedByCause.some(causes_onto.MechanicalFailureOfSupport) &
 isEffectOfDeviation.some(deviation_onto.ElsewhereFlow) &
 effectInvolvesEquipmentEntity.some(equipment_onto.StorageTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)))
 |
 ((effectInvolvesEquipmentEntity.some((equipment_onto.StorageTankEntity) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Emptying |
 process_onto.Storing))) &
 isEffectOfDeviation.some(deviation_onto.LowPressure))
 |
 ((effectInvolvesEquipmentEntity.some(equipment_onto.SettlingTankEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.Separating |
 process_onto.ModeIndependent))) &
 isEffectOfDeviation.some(deviation_onto.LowPressure)))]
LossOfMechanicalIntegrity.comment = ["Underpressure", "Armospheric Tank Failures: Mechanisms and an Unexpected Case Study"]
class GasDispersion(Effect):
 equivalent_to = [Effect &
 (effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Gaseous)) &
 effectImpliedByCause.some(causes_onto.ExternalLeakage))]
class FluidCirculatesInsidePump(Effect):
 equivalent_to = [Effect &
 ((isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump) &
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow)) &
 effectImpliedByCause.some(causes_onto.PumpingAgainstPolymerizedLine |
 causes_onto.DeadHeadingOfPump))
 |
 (isEffectOfDeviation.some(deviation_onto.NoFlow) &
 effectInvolvesEquipmentEntity.some(
 equipment_onto.hasMaterialTransferEquipment.some(equipment_onto.CentrifugalPump) &
 equipment_onto.hasOperationMode.some(equipment_onto.StartUpOperation)) &
 effectImpliedByCause.some(causes_onto.WrongMountingOfNonReturnValve)))]
class Overheating(Effect):
 equivalent_to = [Effect &
 ((effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 isEffectOfDeviation.some(deviation_onto.HighTemperature))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 effectImpliedByCause.some(causes_onto.MalfunctionLubricationSystem))
 |
 (effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effectOfPropagatedCause.value(True))
 |
 FluidCirculatesInsidePump)]
class HeatBuildUp(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 effect_onto.effectImpliedByCause.some(BlockedReboilerLines)
 ]
class ColumnFlooded(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.isEffectOfDeviation.some(deviation_onto.HighLevel) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity))
 |
 (effect_onto.effectImpliedByCause.some(causes_onto.ExcessiveInflow) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium)) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity)
 ))]


class LiquidSlugging(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.hasMaterialTransferEquipment.some(
 equipment_onto.PistonCompressor | equipment_onto.ScrewCompressor)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)) &
 (effect_onto.effectImpliedByCause.some(causes_onto.ContaminationByWater |
 causes_onto.OtherSubstanceFromUpstream)
 |
 effect_onto.isEffectOfDeviation.some(deviation_onto.OtherThanComposition)))]
LiquidSlugging.comment = ["Screw compressors have a higher tolerance to liquid slugging"]
class ExcessiveDischargeTemperature(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity))
 |
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity) &
 effect_onto.effectImpliedByCause.some(causes_onto.MalfunctionLubricationSystem)))]
class IncreasedOilDischarge(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ProcessMedium |
 substance_onto.Refrigerant)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighFlow) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.CompressorEntity &
 equipment_onto.hasSubunit.some(equipment_onto.LubricationSystem))]
class IncompleteEvaporation(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((
 effect_onto.effectInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighFlow |
 deviation_onto.LowTemperature) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.FinTubeEvaporatorEntity |
 equipment_onto.ShellTubeEvaporatorEntity))
 |
 (effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.HeatingMedium)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.LowTemperature) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.ShellTubeEvaporatorEntity)))]
class IncompleteCondensation(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (
 effect_onto.effectInvolvesSubstance.some(substance_onto.hasSpecificTask.some(substance_onto.Refrigerant)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighFlow |
 deviation_onto.HighTemperature) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity))]
class LossOfHeatTransfer(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.ShellTubeHeatExchangerEntity) &
 effect_onto.effectImpliedByCause.some(causes_onto.Fouling))
 |
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.AirCooledCondenserEntity) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighTemperature) &
 effect_onto.effectImpliedByCause.some(causes_onto.WrongRotatingSpeed |
 causes_onto.Fouling |
 causes_onto.HighAmbientTemperature |
 causes_onto.NonCondensables))
 |
 (effect_onto.effectImpliedByCause.some(NoSteamFlow)))]
class ReducedHeatingCapacity(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.StabilizerColumnEntity) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.LowTemperature))]
class IncreasedHeatingCapacity(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.SteamDrivenReboilerEntity) &
 effect_onto.effectImpliedByCause.some(causes_onto.MoreSteamFlow))]
class IncreasedWear(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 effect_onto.effectImpliedByCause.some(OperationBelowMinimumFlowRate)))]
class PumpRunningDry(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 effect_onto.effectImpliedByCause.some(causes_onto.ClosedInletValve |
 causes_onto.LossOfInflow |
 causes_onto.BlockedInflowLine)))]
PumpRunningDry.comment = [
 "https://www.worldpumps.com/operating-design/features/how-to-overcome-the-challenge-of-dry-running/"]
class PumpDeliversNoLiquid(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.DeliverConstantVolumeFlow)) &
 effect_onto.effectImpliedByCause.some(causes_onto.MissingImpeller |
 causes_onto.EntrainedAir) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.NoFlow))
 ]
class Cavitation(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectImpliedByCause.some(InsufficientNPSH) &
 effect_onto.effectInvolvesEquipmentEntity.some(
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow)))
 |
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PumpEntity &
 equipment_onto.hasIntendedFunction.some(process_onto.DeliverConstantVolumeFlow)) &
 effect_onto.effectOfPropagatedCause.some(True) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighTemperature)))]
class PoorPumpPerformance(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectImpliedByCause.some(EntrainedAir | causes_onto.ImpellerFault) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.LowFlow))
 ]



class RunawayReaction(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.ReactorEntity) &
 (effect_onto.effectImpliedByCause.some(causes_onto.CoolingFailure |
 causes_onto.ConfusionOfSubstances |
 causes_onto.NoFeed |
 causes_onto.Pollution |
 ChargingFailure |
 DosingFailure
 ))
 |
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.ReactorEntity) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.ReverseFlow))
 ))]
class InsufficientAmountOfLiquidRefrigerant(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.isEffectOfDeviation.some(deviation_onto.OtherThanComposition |
 deviation_onto.LowLevel) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.PressureReceiverEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.Refrigerant))
 )
 ]
class ScrubberAgentNotAvailable(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 ((effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ScrubbingAgent)) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasFixture.some(
 equipment_onto.LiquidDistributor) &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.NoFlow))
 |
 ((effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasSpecificTask.some(substance_onto.ScrubbingAgent)) &
 effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectImpliedByCause.some(LossOfInflow |
 BlockedInflowLine) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)))))
 ]
class InsufficientGasPurification(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid |
 substance_onto.Multiphase)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.OtherThanComposition))
 ]
class FloodedPackedBed(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.effectInvolvesSubstance.some(
 substance_onto.hasStateOfAggregation.some(substance_onto.Liquid)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighLevel))
 ]
class AbnormalOperationCondition(effect_onto.Effect):
 equivalent_to = [effect_onto.Effect &
 (effect_onto.effectInvolvesEquipmentEntity.some(equipment_onto.WetScrubberEntity &
 equipment_onto.hasIntendedFunction.some(
 process_onto.ModeIndependent)) &
 effect_onto.isEffectOfDeviation.some(deviation_onto.HighTemperature |
 deviation_onto.LowTemperature |
 deviation_onto.LowPressure |
 deviation_onto.HighPressure |
 deviation_onto.HighFlow |
 deviation_onto.LowFlow |
 deviation_onto.HighLevel |
 deviation_onto.OtherThanComposition))
 ] 








#%% Appendix N - Ontology for Effects

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





#%% Appendix O - Ontology for Risks

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
       ))
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





#%% Appendix P - Ontology for Safeguards

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
 
 





#%% Appendix Q - Inference and Analysis

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
    
infer_follow_up(process_unit,   #TODO
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


#%% Appendix W - Specific Case Studies

def create_process_plant_hexane_storage_tank():
    """
    Create a specific case study about a hexane storage tank.

    Returns
    -------
    graph : NetworkX.Digraph
        A graph of 4 components linked by 3 edges in a direct sequence.

    """
    
    hazard_classes = [substance_onto.FlammableLiquidCategory2, substance_onto.SkinCorrosionIrritationCategory2,
                      substance_onto.ReproductiveToxicityCategory2, substance_onto.SpecificTargetOrganToxicityRepeatedExposureCategory2,
                      substance_onto.SpecificTargetOrganToxicitySingleExposureCategory3, substance_onto.AspirationHazardCategory1]
    stability_reactivity_information = [substance_onto.FormsExplosiveMixtureWithAir, substance_onto.ReactsViolentlyWithOxidizer]
    substances = [substance.substance("Hexane",
                                      "110-54-3",
                                      substance_onto.ProcessMedium,
                                      substance_onto.Liquid,
                                      hazard_classes,
                                      stability_reactivity_information,
                                      273.15 - 95.0,
                                      273.15 + 65.0,
                                      273.15 - 20.0,
                                      1.1,
                                      8.3),
    substance.substance("Hexane",
                        "110-54-3",
                        substance_onto.ProcessMedium,
                        substance_onto.Multiphase,
                        hazard_classes,
                        stability_reactivity_information,
                        273.15 - 95.0,
                        273.15 + 65.0,
                        273.15 - 20.0,
                        1.1,
                        8.3)]
    ambient_information = environment_information.ambient_information(273.15 - 8.0,
                                                                      273.15 + 35.0,
                                                                      [site_information.DangerOfHeavyRainfall(),
                                                                       site_information.DangerOfSevereStorm()],
                                                                      [site_information.VehicleTraffic()])
    boundary_conditions = [boundary_onto.LocatedOutside, boundary_onto.IntroductionOfWater, boundary_onto.IntroductionOfImpurities,
                           boundary_onto.FoundationCanBeAffected, boundary_onto.PersonnelPresentInTheNearField,
                           boundary_onto.ExternalFirePossible]
    set_further_boundary_conditions(boundary_conditions, upper_onto.lowest_ambient_temperature)
    boundary_conditions = instantiate_boundary_conditions(boundary_conditions)
    
    tank_truck = equipment_entities.tank_truck("TT100",
                                               boundary_conditions,
                                               equipment_onto.Operator(),
                                               False,
                                               [(prep.DictName.intended_function, process_onto.Unloading),
                                                (None, None),
                                                (None, None),
                                                (None, None)],
                                               1.5, # bar(g)
                                               273.15 + 80., # K
                                               34.4) # m³
    transfer_pump = equipment_entities.centrifugal_pump_2("P200",
                                                          boundary_conditions,
                                                          equipment_onto.Operator(),
                                                          False,
                                                          [(prep.DictName.intended_function, process_onto.DeliverConstantVolumeFlow),
                                                           (None, None),
                                                           (None, None),
                                                           (None, None)],
                                                          1.5, # bar(g)
                                                          273.15 + 80., # K
                                                          90.) # m³/h
    pipe = equipment_entities.connection_pipe("PIP1",
                                              boundary_conditions,
                                              equipment_onto.NotControlled(),
                                              False,
                                              [(prep.DictName.intended_function, process_onto.ModeIndependent),
                                               (None, None),
                                               (None, None),
                                               (None, None)],
                                              15e5,
                                              500)
    tank = equipment_entities.storage_tank_2("T400",
                                             boundary_conditions,
                                             equipment_onto.NotControlled(),
                                             False,
                                             [(prep.DictName.intended_function, process_onto.Filling),
                                              (prep.DictName.intended_function, process_onto.Storing),
                                              (prep.DictName.intended_function, process_onto.Emptying),
                                              (prep.DictName.intended_function, process_onto.ModeIndependent)
                                              ],
                                             0.2, # bar(g)
                                             360., # K
                                             55.) # m³
    
    graph = nx.DiGraph()
    graph.add_node(0,
                   data=tank_truck,
                   ports=dict(
                       p1=equipment_entities.MyPort('p1', equipment_onto.ApiAdaptorValve(), equipment_onto.Outlet())
                       ),
                   substances=[substances[0]],
                   environment=ambient_information)
    graph.add_node(1,
                   data=transfer_pump,
                   ports=dict(p1=equipment_entities.MyPort('p1', equipment_onto.InletValve(), equipment_onto.Inlet()),
                              p2=equipment_entities.MyPort('p2', equipment_onto.OutletValve(),
                                                           equipment_onto.Outlet())),
                   substances=[substances[0]],
                   environment=ambient_information)
    graph.add_node(2,
                   data=pipe,
                   ports=dict(p1=equipment_entities.MyPort('p1', equipment_onto.InletValve(), equipment_onto.Inlet()),
                              p2=equipment_entities.MyPort('p2', equipment_onto.OutletValve(),
                                                           equipment_onto.Outlet())),
                   substances=[substances[0]],
                   environment=ambient_information)
    graph.add_node(3,
                   data=tank,
                   ports=dict(p1=equipment_entities.MyPort('p1', equipment_onto.InletValve(), equipment_onto.Inlet()),
                              p2=equipment_entities.MyPort('p2', equipment_onto.OutletValve(), equipment_onto.Outlet()),
                              p3=equipment_entities.MyPort('p3', equipment_onto.BottomDrainValve(),
                                                           equipment_onto.Outlet())
                              ),
                   substances=[substances[1]],
                   environment=ambient_information)
    
    add_edge_port(graph, 0, 'p1', 1, 'p1')
    add_edge_port(graph, 1, 'p2', 2, 'p1')
    add_edge_port(graph, 2, 'p2', 3, 'p1')
    
    return graph


def create_olefin_feed_section():
    """
    Create a specific case study about an olefin feed section.

    Returns
    -------
    graph : NetworkX.Digraph
        A graph with 6 nodes and 5 edges, but not all in a linear sequence.

    """
    
    # Mixture of Hexane/Hexene and water
    hazard_classes = [substance_onto.FlammableLiquidCategory2,
                      substance_onto.SkinCorrosionIrritationCategory2,
                      substance_onto.ReproductiveToxicityCategory2,
                      substance_onto.SpecificTargetOrganToxicityRepeatedExposureCategory2,
                      substance_onto.SpecificTargetOrganToxicitySingleExposureCategory3,
                      substance_onto.AspirationHazardCategory1]
    stability_reactivity_information = [substance_onto.PolymerizesExothermicallyWithoutInhibitor,
                                        substance_onto.PolymerizesExothermicallyWhenExposedToHeat,
                                        substance_onto.FormsExplosiveMixtureWithAir]
    
    substances = [
        substance.substance("Olefin&Water",
                            "",
                            substance_onto.ProcessMedium,
                            substance_onto.Liquid,
                            hazard_classes,
                            stability_reactivity_information,
                            273.15 - 117.5,
                            273.15 + 63.5,
                            273.15 - 23.0,
                            1.15,
                            7.6),
        substance.substance("Nitrogen",
                            "",
                            substance_onto.InertGas,
                            substance_onto.Gaseous,
                            [],
                            [],
                            273.15 - 210.0,
                            273.15 - 196.0,
                            None,
                            None,
                            None
                            ),
        substance.substance("Olefin&Water&Nitrogen",
                            "",
                            substance_onto.ProcessMedium,
                            substance_onto.Multiphase,
                            hazard_classes,
                            stability_reactivity_information,
                            273.15 - 117.5,
                            273.15 + 63.5,
                            273.15 - 23.0,
                            1.15,
                            7.6)
    ]
    graph = nx.DiGraph()
    ambient_information = environment_information.ambient_information(273.15 - 8.0,
                                                                      273.15 + 35.0,
                                                                      [site_information.DangerOfHeavyRainfall(),
                                                                       site_information.DangerOfSevereStorm()],
                                                                      [site_information.VehicleTraffic()])
    boundary_conditions = [ boundary_onto.LocatedOutside,
                            boundary_onto.IntroductionOfWater,
                            boundary_onto.IntroductionOfImpurities,
                            boundary_onto.PersonnelPresentInTheNearField,
                            boundary_onto.ExternalFirePossible
                            ]
    
    # In case water is not part of the substances it can be introducted by rain, humidity etc.
    for subst in substances:
        if not "Water" in subst.name and subst.intended_state_of_aggregation[0].is_a[0].name != "Gaseous":
            boundary_conditions.append(boundary_onto.IntroductionOfWater)
            
    boundary_conditions.append(boundary_onto.UpstreamProcessInvolved)
    boundary_conditions.append(boundary_onto.IntroductionOfAir)
    set_further_boundary_conditions(boundary_conditions, upper_onto.lowest_ambient_temperature)
    boundary_conditions = instantiate_boundary_conditions(boundary_conditions)
    
    # === Equipment entity definition
    transfer_pump = equipment_entities.centrifugal_pump_2("P200",
                                                          boundary_conditions,
                                                          equipment_onto.Operator(),
                                                          False,
                                                          [(prep.DictName.intended_function, process_onto.DeliverConstantVolumeFlow),
                                                           (prep.DictName.intended_function, process_onto.ModeIndependent)],
                                                          10.0, # barg
                                                          400., # K
                                                          25.) # m³/h
    pipe = equipment_entities.connection_pipe("PIP1",
                                              boundary_conditions,
                                              equipment_onto.NotControlled(),
                                              False,
                                              [(prep.DictName.intended_function, process_onto.ModeIndependent),
                                               (None, None)],
                                              10.0,
                                              500.0)
    settling_tank = equipment_entities.settling_tank("ST01",
                                                     boundary_conditions,
                                                     equipment_onto.NotControlled(),
                                                     False,
                                                     [(prep.DictName.intended_function, process_onto.Separating),
                                                      (prep.DictName.intended_function, process_onto.ModeIndependent)],
                                                     1.0, # barg
                                                     400., # K
                                                     50.) # m³
    inertization = equipment_entities.inertgas_blanketing("IB01",
                                                          boundary_conditions,
                                                          equipment_onto.NotControlled(),
                                                          False,
                                                          [(prep.DictName.intended_function, process_onto.Inerting),
                                                           (prep.DictName.intended_function, process_onto.ModeIndependent)],
                                                          2.0, # barg
                                                          400., # K
                                                          )
    control_valve = equipment_entities.pneumatically_flow_control_valve_1("CV01",
                                                                          boundary_conditions,
                                                                          equipment_onto.NotControlled(),
                                                                          False,
                                                                          [(prep.DictName.intended_function, process_onto.FlowControl),
                                                                           (prep.DictName.intended_function, process_onto.ModeIndependent)],
                                                                          10.0, # barg
                                                                          400., # K
                                                                          )
    
    graph.add_node(0,
                   data=equipment_entities.source("Source", boundary_conditions, equipment_onto.NotControlled(), False,
                                                  [(prep.DictName.intended_function, process_onto.ModeIndependent),
                                                   (None, None)], None, None),
                   ports=dict(p1=equipment_entities.MyPort('p1', None, equipment_onto.Outlet())),
                   substances=[substances[0]],
                   environment=ambient_information)
    graph.add_node(1,
                   data=transfer_pump,
                   ports=dict(p1=equipment_entities.MyPort('p1', equipment_onto.InletValve(), equipment_onto.Inlet()),
                              p2=equipment_entities.MyPort('p2', equipment_onto.OutletValve(), equipment_onto.Outlet()),
                              p3=equipment_entities.MyPort('p3', equipment_onto.BottomDrainValve(),
                                                           equipment_onto.Outlet())),
                   substances=[substances[0]],
                   environment=ambient_information)
    graph.add_node(2,
                   data=pipe,
                   ports=dict(p1=equipment_entities.MyPort('p1', None, equipment_onto.Inlet()),
                              p2=equipment_entities.MyPort('p2', None, equipment_onto.Outlet())),
                   substances=[substances[0]],
                   environment=ambient_information)
    graph.add_node(3,
                   data=control_valve,
                   ports=dict(p1=equipment_entities.MyPort('p1', None, equipment_onto.Inlet()),
                              p2=equipment_entities.MyPort('p2', None, equipment_onto.Outlet())),
                   substances=[substances[0]],
                   environment=ambient_information)
    graph.add_node(4,
                   data=settling_tank,
                   ports=dict(p1=equipment_entities.MyPort('p1', equipment_onto.InletValve(), equipment_onto.Inlet()),
                              p2=equipment_entities.MyPort('p2', equipment_onto.OutletValve(), equipment_onto.Outlet()),
                              p3=equipment_entities.MyPort('p3', equipment_onto.BottomDrainValve(),
                                                           equipment_onto.Outlet()),
                              p4=equipment_entities.MyPort('p4', None, equipment_onto.Inlet())),
                   substances=[substances[2]],
                   environment=ambient_information)
    graph.add_node(5,
                   data=inertization,
                   ports=dict(p1=equipment_entities.MyPort('p1', None, equipment_onto.Inlet()),
                              p2=equipment_entities.MyPort('p2', None, equipment_onto.Outlet())),
                   substances=[substances[1]],
                   environment=ambient_information)
    # graph.add_node(6,
    #                data=equipment_entities.Sink("Sink", boundary_conditions, equipment_onto.NotControlled(), False,
    #                                             [equipment_onto.ContinuesProcess, equipment_onto.ModeIndependent], None, None),
    #                ports=dict(
    #                    p1=equipment_entities.MyPort('p1', None, equipment_onto.Inlet())),
    #                substances=[substances[0]],
    #                environment=ambient_information)
    
    add_edge_port(graph, 0, 'p1', 1, 'p1')
    add_edge_port(graph, 1, 'p2', 2, 'p1')
    add_edge_port(graph, 2, 'p2', 3, 'p1')
    add_edge_port(graph, 3, 'p2', 4, 'p1')
    add_edge_port(graph, 5, 'p2', 4, 'p4')
    # add_edge_port(graph, 4, 'p2', 6, 'p1')
    
    # print(graph.edges(data=True))
    
    return graph







#%% Appendix C - Main


if __name__ == '__main__':
    
    # === save all ontologies
    ontology_operations.save_ontology()
    ontology_operations.save_ontology_as_sql()
    upper_onto.determine_onto()
    
    start_time = time.time()
    
    # === Process model
    process_plant_model = model.create_hazid_benchmark_1()
    
    deviation_number = None
    stack_elements = []
    
    # === Tearing strategy/strategy for defining order of process equipment/start-end point
    if len(process_plant_model.nodes) > 1:
        
        # The following single method is now subdivided into 3 for clarity.
        # graph_type, newly_arranged_graphs, intersections = algorithm.determine_propagation_strategy(process_plant_model)
        graph_type = findTypeOf(process_plant_model)
        newly_arranged_graphs = replicate(process_plant_model, graph_type)
        intersections = getIntersectionNode(process_plant_model, graph_type)
        
        print(list(newly_arranged_graphs))

    if config.EQUIPMENT_BASED_EVALUATION:
        
        for index in range(len(process_plant_model.nodes)):
            equipment_specific_prop_scenarios = []
            
            equipment_entity = process_plant_model.nodes[index]["data"]
            
            # Add port information to equipment entity
            for key, value in process_plant_model.nodes[index]["ports"].items():
                equipment_entity.onto_object.hasPort.append(value.onto_object)
                
                # Add port information to equipment entity
                if value.port_instrumentation:
                    equipment_entity.onto_object.hasInstrumentation.append(value.port_instrumentation)
                    
            process_unit_obj = equipment_entity.onto_object.is_a[0]
            
            # === continue in case of source and sink, since they are not relevant in
            # equipment-based mode to save reasoner calls
            if process_unit_obj == equipment_onto.SinkEntity:
                continue
            
            substances = process_plant_model.nodes[index]["substances"]
            environment = process_plant_model.nodes[index]["environment"]
            deviations = config.deviation_selector(process_unit_obj)
            
            # === Infer hazards
            infer.equipment_based_analysis( equipment_entity,
                                            deviations,
                                            substances,
                                            environment,
                                            equipment_specific_prop_scenarios )
    
            stack_elements.append({"{0}".format(equipment_entity.name): equipment_entity,
                                   pre_processing.DictName.scenario: equipment_specific_prop_scenarios})

    # === Entry point for hazard/malfunction propagation
    if config.PROPAGATION_BASED_EVALUATION:
        
        if graph_type == algorithm.GraphType.SingleLineSystem:
            infer.propagation_based_analysis(process_plant_model, newly_arranged_graphs, stack_elements)
            
        elif graph_type == algorithm.GraphType.MultiCycleSystem:
            
            for index, cycle in enumerate(newly_arranged_graphs):
                # intersection of cycles
                intersection_node_index = cycle.index(intersections)
    
                # start first cycle one node after intersection and following nodes at intersection
                if index == 0:
                    intersection_node_index += 1

                # === Change order of graph [intersection + 1] as starting node
                new_order = []
                for node in go.starting_with(cycle, intersection_node_index):
                    new_order.append(node)
    
                infer.propagation_based_analysis(process_plant_model,
                                                 new_order,
                                                 stack_elements)
    
        elif graph_type == algorithm.GraphType.JunctionSystem or \
                graph_type == algorithm.GraphType.ComplexSystem or \
                graph_type == algorithm.GraphType.RecycleFlowSystem:
            for stream in newly_arranged_graphs:
                infer.propagation_based_analysis(process_plant_model, stream, stack_elements)
        else:
            print("Case not covered by any strategy!")

    # === remove duplicates and sort results table
    results = pre_processing.cleanup_result_list(results)
    results = sorted(results, key=lambda k: k["process_equipment_id"])

    # === Hazop table
    if results:
        counter = 0
        for row in results:
            if row["cause"] or row["effect"] or row["consequence"]:
                output.hazop_table.add_row([counter,
                                            row["process_equipment"],
                                            row["process_equipment_id"],
                                            ', '.join(row["operation_mode"]),
                                            row["substance"],
                                            ', '.join(row["deviation"]),
                                            ', '.join(row["super_cause"]),
                                            ', '.join(row["cause"]),
                                            ', '.join(row["effect"]),
                                            ', '.join(row["consequence"]),
                                            ', '.join(row["safeguard"]),
                                            row["propagated"],
                                            ', '.join(row["risk"]),
                                            ])
            counter += 1
            
    print(output.hazop_table)

    output.create_output()
    
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    ontology_operations.save_ontology()

    # === Get errors
    print(list(default_world.inconsistent_classes()))
    
    
        
        