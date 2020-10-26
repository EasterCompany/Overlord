"""
  PROJECT ATLAS: 
    "Suite" monitors and recurringly tests
    live services for reliability and 
    performance measures.

    "Test" is used to rapidly deploy 
    unit tests for overlord modules
""" 

from . import Suite

from .. import Bionic
from .. import Canopy
from .. import Dexter
from .. import Entropy
from .. import Forensic

Bionic.Basics.clear_console()
Suite.add.library(Bionic)
Suite.add.library(Canopy)
Suite.add.library(Dexter)
Suite.add.library(Entropy)
Suite.add.library(Forensic)
Suite.run()
