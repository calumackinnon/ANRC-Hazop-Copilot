# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 10:47:34 2024

@author: qrb15201
"""

from owlready2 import Thing


# with boundary_onto:
class BoundaryCondition(Thing):                                 pass
class IntroductionOfAir(BoundaryCondition):                     pass
class IntroductionOfImpurities(BoundaryCondition):              pass
class IntroductionOfWater(BoundaryCondition):                   pass
class ExternalFirePossible(BoundaryCondition):                  pass
class LocatedOutside(BoundaryCondition):                        pass
class UpstreamProcessInvolved(BoundaryCondition):               pass
class SubstanceContainsStabilizer(BoundaryCondition):           pass
class FoundationCanBeAffected(BoundaryCondition):               pass

