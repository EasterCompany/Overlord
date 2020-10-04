"""
  PROJECT ATLAS: 
    "Suite" monitors and recurringly tests
    live services for reliability and 
    performance measures.

    "Test" is used to rapidly deploy 
    unit tests for overlord modules
""" 

from . import Test
from . import Suite

from Overlord import Bionic
from Overlord import Canopy
from Overlord import Dexter
from Overlord import Entropy

Bionic.Basics.clear_console()
Suite.add.library(Bionic)
Suite.add.library(Canopy)
Suite.add.library(Dexter)
Suite.add.library(Entropy)
Suite.run()
