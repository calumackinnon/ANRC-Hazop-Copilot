# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:53:23 2024

@author: qrb15201
"""

'''

class OverallModel:
    
    pass



class SiteInformation():
    
    pass

    def __init__():
        
        pass

class HexaneTankModel(OverallModel):
    
    siteInfo = None
    
    def __init__(self):
        
        self.siteInfo = SiteInformation()

class Ports:
    
    def __init__(self):
        
        pass

class BoundaryCondition:
    
    def __init__(self):
        
        pass

class Substance:
    
    def __init__(self):
        
        pass
    

class EquipmentEntity:
    
    ports = None
    boundaryCondition = None
    substance = None
    

class TankTruck(EquipmentEntity):
    
    def __init__(self):
        
        pass

class Pump(EquipmentEntity):
    
    def __init__(self):
        
        pass


class ConnectionPipe(EquipmentEntity):
    
    def __init__(self):
        
        pass


class StorageTank(EquipmentEntity):
    
    def __init__(self):
        
        pass
'''

"""
def create_process_plant_hexane_storage_tank():
    
    hazard_classes = [substance_onto.FlammableLiquidCategory2, 
                      substance_onto.SkinCorrosionIrritationCategory2,
                      substance_onto.ReproductiveToxicityCategory2, 
                      substance_onto.SpecificTargetOrganToxicityRepeatedExposureCategory2,
                      substance_onto.SpecificTargetOrganToxicitySingleExposureCategory3, 
                      substance_onto.AspirationHazardCategory1
                      ]
    
    stability_reactivity_information = [
        substance_onto.FormsExplosiveMixtureWithAir,
        substance_onto.ReactsViolentlyWithOxidizer
        ]
    """
    
def create_process_plant_hexane_storage_tank():
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
