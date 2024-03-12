# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:43:02 2024

@author: qrb15201
"""


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
                
        def set_intended_function(self, inteded_function):
            
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
                hasSubunit = self.subunit
                )
            
        
        
        