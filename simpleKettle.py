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
import pandas as pd

#%% 1. A tea classifier.
#       When you make tea, what you add determines how it tastes.
#       Good tea takes near-boiling water, a teabag, and a delay before milk.
#       If cold water is added the tea will not diffuse and have no taste.
#       To add milk from a fridge reduces the temperature and limits diffusion.
#       This code specifies an example which uses knowledge about all of this, 
#       to assume the quality of some tea from a process specified to make it.


#%% 2. Make an Ontology (i.e., define the outputs / possible outcomes)

# Some code creates a world as detailed at https://owlready2.readthedocs.io/en/latest/world.html#using-several-isolated-worlds
if 'y' == input('Want to create a new world to reason within? (y/n) (hint: do this once to set up the environment.)'):
    #     kitchen = World(filename='/world/quadstore.sqlite3')
    #     onto = kitchen.get_ontology("http://test.org/onto.owl").load()

    onto = get_ontology("http://test.org/onto.owl")
    
    with onto:
        
        ''' RESTRICTIONS
        Owlready provides the following types of restrictions 
        (they have the same names as in Protégé):
        
        some :      Property.some(Range_Class)
        only :      Property.only(Range_Class)
        min :       Property.min(cardinality, Range_Class)
        max :       Property.max(cardinality, Range_Class)
        exactly :   Property.exactly(cardinality, Range_Class)
        value :     Property.value(Range_Individual / Literal value)
        has_self :  Property.has_self(Boolean value)
        
        As given at https://owlready2.readthedocs.io/en/latest/restriction.html
        '''
        
        class Equipment(Thing):             pass
            
        class Container(Equipment): pass
            
            # def drink(self):
                
            #     substance = 
            #     return substance
            #     # pass
            
        class Kettle(Container):
            
            def boil(self):
                
                #TODO This should find any contained substance and set it's temp.
                pass
                
        class Bag(Container):                               pass
        class Bowl(Container):                              pass
        class Box(Container):                               pass
        class Fridge(Container):                            pass
        class Jug(Container):                               pass
        class Teapot(Container):                            pass

        class Cup(Container):                               
        # To Python the following will look like it overwrites or replaces the
        # previous class, but as in the OWLReady2 docs this instead extends it.
        # https://owlready2.readthedocs.io/en/latest/mixing_python_owl.html#forward-declarations
            def drink(self, df_relations):
                desired_domain = self
                # Filter the DataFrame based on the specified "Relation" and "Domain"
                filtered_rows = df_relations.loc[(df_relations['Relation'] == onto.containsSubstance) & 
                                                 (df_relations['Domain'] == desired_domain)]
                # print("filtered_rows is", filtered_rows)
                
                # Join the elements of filtered_rows["Range"] with "and" as the separator
                range_contents = " and ".join(map(str, filtered_rows["Range"]))
                # Print the formatted output
                print(f"The contents of {self} were {range_contents}")
    
    #%%
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
    
    
        class hasTemperature(Substance >> float):           
            python_name = "heat_to"
    
        class TeaMixture(Substance):
            equivalent_to = [Water & Tea]
            
            def taste(self):
                print('Tasting...')
                
                
    #%% 
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
            
        # class HerbalTea(TeaMixture):
            
        #     def taste(self): print('This tea tastes herbal.')
        
        class contains(Container >> Container):             pass
    
        class containsSubstance(Container >> Substance):    
            python_name = "ingredients"
    
                
        class CupOfTea(Cup):
            is_a = [containsSubstance.some(TeaMixture)]
            
        class EmptyCup(Cup):
            equivalent_to = [Cup & Not(containsSubstance.some(Substance))]
            
        class AcceptableCup(Cup):
            equivalent_to = [containsSubstance.some(TeaMixture)
                            & Not(containsSubstance.some(Cinnamon))
                            ]
            
            def drink(self): print('This cup tastes good.')
            
        class UnacceptableCup(Cup):
            equipvalent_to = [Not(AcceptableCup)]
            
            def drink(self): print('This cup does not taste good.')
            
        class mixWith(Substance >> Substance): 
            python_name = "mix"
                
        
def putIn(c, addition): #TODO - understand this (JF)
    
    if isinstance(addition, Container):
        return contains(c, addition)
    else:
        return containsSubstance(c, addition)
        
# contains() or containsSubstance()


# The AllDisjoint([]) statement states classes do not overlap on a Venn diagram
AllDisjoint([AcceptableCup, UnacceptableCup])
AllDisjoint([Kettle, Bag, Bowl, Cup, Box, Fridge, Jug, Teapot])
# So here I mean that all the containers are different, and that each cup is 
# strictly either AcceptableCup or UnacceptableCup, but can be any of the other
# classes at the same time. This is needed to structure the classification.




#%% Create the Individuals (In other words, define inputs for a given scenario)
''' According to https://owlready2.readthedocs.io/en/latest/onto.html#accessing-the-content-of-an-ontology
    the objects created in this part can be checked with a console command like
    list(default_world.individuals())
'''
    
hasRelations = [] #TODO - understand this (JF)

tepid = Water(21.0)
lukewarm = Water(35.0)
boiled = Water(98.0)

pours = [tepid, lukewarm, boiled]
AllDifferent(pours)


tealeaves = Tea() 
semiskimmedmilk = Milk()
cinnamon = Cinnamon()

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
    cup4 = Cup(ingredients = [boiled, tealeaves, cinnamon])
    tray = [cup1, cup2, cup3]
    
    close_world(Substance) #TODO - understand this (JF)

# The AllDifferent([]) command is like AllDisjoint([]) but for individuals.
# https://owlready2.readthedocs.io/en/latest/disjoint.html#different-individuals
AllDifferent(tray) #TODO - understand this (JF)


#%% 6. Pose Queries by Doing the reasoning (In other words, do the processing).

# sync_reasoner( [world] ) is where the reasoning is performed on the ontology.
sync_reasoner() #TODO - understand this (JF)

print('onto made')

print(onto)


#%% Block of script to determine the contents of a cup. 
#TODO - Further edits to determine if it drink is acceptable and therefore drunk:-

"""
Start by getting an object which is a list of the properties
Use the property_class.get_relations() method
"""


# import pandas as pd

# Initialize an empty list to store relations
relations = []

# Define column names
columns = ["Relation", "Domain", "Range"]

# Iterate through properties in the ontology
for prop in onto.properties():
    # Retrieve relations for each property
    for relation in prop.get_relations():
        # Create a dictionary to store relation, domain, and range
        relation_dict = {"Relation": prop, 
                         "Domain": relation[0],
                         "Range": relation[1]}
        # Append the dictionary to the list of relations
        relations.append(relation_dict)

# Create a DataFrame from the list of relations
df_relations = pd.DataFrame(relations, columns=columns)

# Extract an element to check
a = df_relations.loc[df_relations.index[0], "Domain"]
type(a)
a

# Get the unique values for the "Domain" column
unique_domains = df_relations['Domain'].unique()

# print(list(onto.containsSubstance.get_relations()))


#%% 
# onto.containsSubstance.get_relations()
# substance = cup1.drink()
# substance.taste()
cup1.drink(df_relations)
cup2.drink(df_relations)
cup3.drink(df_relations)
cup4.drink(df_relations)


# # Testing the self.drink() 
# desired_domain = onto.cup1
# # Filter the DataFrame based on the specified "Relation" and "Domain"
# filtered_rows = df_relations.loc[(df_relations['Relation'] == onto.containsSubstance) & 
#                                   (df_relations['Domain'] == desired_domain)]

# # Join the elements of filtered_rows["Range"] with "and" as the separator
# range_contents = " and ".join(map(str, filtered_rows["Range"]))
# # Print the formatted output
# print(f"The contents of {cup1} were {range_contents}")




# for cup in tray:
    
#     # for each in cup.allSubstances():
#     s = cup.containsSubstance() # ask a specific query to the knowledge #TODO - understand this (JF) -
#     # I think that cup() lacks the method .taste() as this was only defined for Substances
#     s.taste()

