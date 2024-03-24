# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:20:53 2024

Creating a new file to make ontologies with. This represents a step away from 
the contents of the dissertation code to use a new example situation.

From Section 8.4.1 of Russel & Norvig, 3rd Ed. 2010, there is a 7-step process:
    1. Identify the task
    2. Assemble the relevant knowledge
    3. Decide on a vocabulary of predicates
    4. Encode general knowledge about the domain
    5. Encode a description of the specific problem instance
    6. Pose queries to the inference procedure and get answers
    7. Debug the knowledge base.

@author: qrb15201
"""

from owlready2 import *

#%% 1. A tea classifier.
#       When you make tea, what you add determines how it tastes.
#       Good tea takes near-boiling water, a teabag, and a delay before milk.
#       If cold water is added the tea will not diffuse and have no taste.
#       To add milk from a fridge reduces the temperature and limits diffusion.
#       This code specifies an example which uses knowledge about all of this, 
#       to assume the quality of some tea from a process specified to make it.


#%% 2. Make an Ontology (i.e., define the outputs / possible outcomes)

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
    
    class Equipment(Thing):             pass
    # class Container(Equipment):     
    #     containsList = []
        
    #     def putIn(self, item):
    #         self.containsList.append(item)
            
    #     def allSubstances(self):
            
    #         if len(self.containsList) <= 0:
    #             return [] # base case
            
    #         substanceList = []
    #         for item in self.containsList:
                
    #             print(item)
                
    #             # Each item is either Substance or Container
    #             if isinstance(item, Container):
                    
    #                 # get the next thing it contains and recurse
    #                 substances = item.allSubstances() #TODO Error
    #                 for s in substances:
    #                     substanceList.append(s)
                        
    #             else: # item is a Substance
    #                 substanceList.append(item)
            
    #         return substanceList
        
    class Container(Equipment): pass
    class Kettle(Container):
        
        def boil(self):
            
            #TODO This should find any contained substance and set it's temp.
            pass
            
    class Bag(Container):                               pass
    class Bowl(Container):                              pass
    class Box(Container):                               pass
    class Cup(Container):                               pass
    class Fridge(Container):                            pass
    class Jug(Container):                               pass
    class Teapot(Container):                            pass

    class Substance(Thing):         
        
        def diffuse(self):
            
            print('A substance is contained.')
            
        def setTemperature(self, temp):
            self.temperature = temp
            
        def getTemperature(self, temp):
            return self.temperature
    
    class Water(Substance): # A subclass inherits from a superclass in ontology
        pass
    class Sugar(Substance):                             pass
    class Milk(Substance):                              pass
    class Tea(Substance):                               pass # Tea leaves
    class Cinnamon(Substance):                          pass # Why not?

    class hasTemperature(Substance >> float):           pass

    class TeaMixture(Substance):
        equivalent_to = [Water & Tea]
        
        def taste(self):
            print('Tasting...')
    
    class WeakTea(TeaMixture):
        
        equivalent_to = [TeaMixture & hasTemperature.max(50.0)]
        
        def taste(self):
            print('This is weak tea.')
    
    # class Tea(TeaMixture):
    #     equivalent_to = [TeaMixture & hasTemperature.min(80.0)]
        
    #     def diffuse(self): print('This is as expected.')
    
    class WhiteTea(TeaMixture):
        equivalent_to = [TeaMixture & Milk & hasTemperature.min(80.0)]
        
        def taste(self): print('This is milk tea.')
    
    class BlackTea(TeaMixture):
        equivalent_to = [TeaMixture & hasTemperature.min(80.0)]

        def taste(self): print('This is Airplane tea.')
    
    class BuildersTea(TeaMixture):
        equivalent_to = [TeaMixture & hasTemperature.min(90.0)]

        def taste(self): print('Don\'t stop for winter.')
    
    class NutrimaticTea(TeaMixture):
        equivalent_to = [TeaMixture & Cinnamon & hasTemperature.min(80.0)]

        def taste(self): print('This is almost, but not quite, entirely unlike tea.')
    
    class contains(Container >> Container):             pass

    class containsSubstance(Container >> Substance):    pass

    class EmptyCup(Cup):
        equivalent_to = [Cup & Not(containsSubstance.some(Substance))]
        
def putIn(c, addition):
    
    if isinstance(addition, Container):
        return contains(c, addition)
    else:
        return containsSubstance(c, addition)
        
# contains() or containsSubstance()
#%% Create the Individuals (In other words, define inputs for a given scenario)

hasRelations = []

tepid = Water(21)
lukewarm = Water(35)
boiled = Water(98)

pours = [tepid, lukewarm, boiled]

tealeaves = Tea()
semiskimmedmilk = Milk()
# hasRelations.append( putIn() )

#%% 5. Configure A Specific Scenario
answer = input('Configure the specific scenario? (y/n)')
if 'y' == answer:
    
    # # Set out 3 coloured cups
    # cup1 = Cup('red')
    # cup2 = Cup('blue')
    # cup3 = Cup('green')
    # tray = [cup1, cup2, cup3]
    
    # # Set up the sugar
    # sugar = Sugar('brown')
    # bowlOfSugar = Bowl()
    # # bowlOfSugar.putIn(sugar)
    # contains(bowlOfSugar, sugar)
    
    # # Make the teabags
    # t = Tea()
    # teaBagA = Bag()
    # teaBagA.putIn(t)
    # teaBagB = Bag()
    # teaBagB.putIn(t)
    # teaBagC = Bag()
    # teaBagC.putIn(t)
    
    # # for cup in tray:
    # #     cup.putIn(teaBagA)
    
    # cup1.putIn(teaBagA)
    # cup1.putIn(tepid)
    # cup2.putIn(teaBagB)
    # cup2.putIn(lukewarm)
    # cup3.putIn(teaBagC)
    # cup3.putIn(boiled)
    
    # # Set up the fridge with milk in a jug.
    # fridge = Fridge()
    # theJug = Jug()
    # milk = Milk()
    # theJug.putIn(milk)
    # fridge.putIn(theJug)
    
    cup1 = Cup(ingredients = [tealeaves, tepid])
    cup2 = Cup(ingredients = [tealeaves, lukewarm, semiskimmedmilk])
    cup3 = Cup(ingredients = [])
    tray = [cup1, cup2, cup3]
    
    close_world(Substance)

    AllDifferent(tray)

#%% 6. Pose Queries by Doing the reasoning (In other words, do the processing).

sync_reasoner()

print('onto made')

print(onto)

if 'y' == answer:
    for cup in tray:
        # for each in cup.allSubstances():
        cup.taste() # ask a specific query to the knowledge
    
    
