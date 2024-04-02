# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 14:00:37 2024

A copy of Drug reasoner from https://owlready2.readthedocs.io/en/latest/reasoning.html

@author: CM
"""

from owlready2 import *

onto = get_ontology("http://test.org/onto.owl")

with onto:
    class Drug(Thing):
        def take(self): print("I took a drug")

    class ActivePrinciple(Thing):
        pass

    class has_for_active_principle(Drug >> ActivePrinciple):
        python_name = "active_principles"

    class Placebo(Drug):
        equivalent_to = [Drug & Not(has_for_active_principle.some(ActivePrinciple))]
        # I read this as, it is a Drug, and has no asspciated ActivePrinciple
        
        def take(self): print("I took a placebo")

    class SingleActivePrincipleDrug(Drug):
        equivalent_to = [Drug & has_for_active_principle.exactly(1, ActivePrinciple)]
        
        def take(self): print("I took a drug with a single active principle")

    class DrugAssociation(Drug):
        equivalent_to = [Drug & has_for_active_principle.min(2, ActivePrinciple)]
        
        def take(self): print("I took a drug with %s active principles" % len(self.active_principles))

# Create the individuals

acetaminophen   = ActivePrinciple("acetaminophen")
amoxicillin     = ActivePrinciple("amoxicillin")
clavulanic_acid = ActivePrinciple("clavulanic_acid")

AllDifferent([acetaminophen, amoxicillin, clavulanic_acid])

drug1 = Drug(active_principles = [acetaminophen])
drug2 = Drug(active_principles = [amoxicillin, clavulanic_acid])
drug3 = Drug(active_principles = [])

close_world(Drug)

sync_reasoner()

drug3.take()

list(default_world.inconsistent_classes())

