#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is a demo just to play with the simulation library.
"""

# TODO: this file will be migrated.

# IMPORTS
#from simulator.Simulation import Simulation
from simulator.NANDDisk import NANDDisk

# initialize a new simulation
#s = Simulation()
d = NANDDisk()

# write 24 data twice (the second time as a change)
for i in range(0, 48, 2):
    d.host_write_page(block=0, page=i)  # new write
    d.host_write_page(block=0, page=i)  # modify

# check
print(d.write_amplification())
print(d.total_pages)
print(d.number_of_dirty_pages())
print(d.number_of_empty_pages())
