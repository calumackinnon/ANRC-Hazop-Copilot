# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:20:53 2024

Creating a new file to make ontologies with. This represents a step away from 
the contents of the dissertation code to use a new example situation.

@author: qrb15201
"""

from owlready2 import *



#%% Create an Ontology (In other words, define the outputs / possible outcomes)

onto = get_ontology("http://test.org/onto.owl")

with onto:

    # Owlready provides the following types of restrictions 
    # (they have the same names as in Protégé):
    
    # some : Property.some(Range_Class)
    # only : Property.only(Range_Class)
    # min : Property.min(cardinality, Range_Class)
    # max : Property.max(cardinality, Range_Class)
    # exactly : Property.exactly(cardinality, Range_Class)
    # value : Property.value(Range_Individual / Literal value)
    # has_self : Property.has_self(Boolean value)
    
    class Equipment(Thing):         pass
    class Container(Equipment):     pass
    class Kettle(Container):
        
        def boil(self):
            
            #TODO This should find any contained substance and set it's temp.
            pass
            
    class Bag(Container):           pass
    class Bowl(Container):           pass
    class Box(Container):           pass
    class Cup(Container):           pass
    class Fridge(Container):           pass
    class Jug(Container):           pass
    class Teapot(Container):           pass

    class Substance(Thing):         
        
        def diffuse(self):
            
            print('A substance is contained.')
            
        def setTemperature(self, temp):
            self.temperature = temp
            
        def getTemperature(self, temp):
            return self.temperature
    
    class Water(Substance): # A subclass inherits from a superclass in ontology
    
        pass
    class hasTemperature(Substance >> float):           pass

    class TeaMixture(Substance):
        equivalent_to = [Water & Bag]
    
    class WeakTea(TeaMixture):
        
        equivalent_to = [TeaMixture & hasTemperature.max(50.0)]
        
        def diffuse(self):
            print('This is weak tea.')
    
    class Tea(TeaMixture):
        equivalent_to = [TeaMixture & hasTemperature.min(80.0)]
    
    class WhiteTea(TeaMixture):
        pass
    
    class BlackTea(TeaMixture):
        pass
    
    class BuildersTea(TeaMixture):
        pass
    
    class NutrimaticTea(TeaMixture):
        pass
    
    
    class contains(Container >> Container):             pass

    class containsSubstance(Container >> Substance):    pass

    

#%% Create the Individuals (In other words, define inputs for a given scenario)

tepid = Water(21)
lukewarm = Water(35)
boiled = Water(98)

cup1 = Cup


#%% Do the reasoning (In other words, do the processing).

sync_reasoner()

print('onto made')

print(onto)
