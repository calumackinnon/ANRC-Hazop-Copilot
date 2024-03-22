# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:09:25 2024

from https://paul-bruffett.medium.com/building-ontologies-with-python-84238d6eee52
and  https://owlready2.readthedocs.io/en/latest/install.html#installation-in-spyder-idle-or-any-other-python-console

@author: qrb15201
"""
from owlready2 import *
from owlready2 import Thing

onto = get_ontology("http://test.org/onto.owl")

with onto:
    #our entities are classes
    class Coffee(Thing): pass
    
    #related information can also be captured as classes
    class Roast(Thing): pass
    
    #subclassing Roast to break down additional details
    class Dark_Roast(Roast): pass
    class Blonde_Roast(Roast): pass
    class Medium_Roast(Roast): pass
    
    
    class Region(Thing): pass
    
    class Latin_America(Region): pass
    class Asia_Pacific(Region): pass
    class Multi(Region): pass