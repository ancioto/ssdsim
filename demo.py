#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is a demo just to play with the simulation library.
"""

# IMPORTS
from simulator.Simulation import Simulation
from simulator.NAND.NANDFactory import get_instance, WRITEPOLICY_INPLACE, WRITEPOLICY_INPLACE_NOERASE, \
    GARBAGECOLLECTOR_SIMPLE


def main():
    # create the simulation
    demo = Simulation(simulation_name="demo")
    demo.init_simulation(base_path="../OUT/")

    # create the disks and attach to the simulation
    demo.add_disk("base", get_instance())
    demo.add_disk("basegc", get_instance(garbagecollector=GARBAGECOLLECTOR_SIMPLE))
    demo.add_disk("wpgc", get_instance(WRITEPOLICY_INPLACE, GARBAGECOLLECTOR_SIMPLE))
    demo.add_disk("wpnegc", get_instance(WRITEPOLICY_INPLACE_NOERASE, GARBAGECOLLECTOR_SIMPLE))

    # run the simulation
    demo.run()

#
# MAIN ENTRY POINT
#
if __name__ == "__main__":
    # execute only if run as a script
    main()
