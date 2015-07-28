#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is a demo just to play with the simulation library.
"""

# IMPORTS
import matplotlib.pyplot as plt
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

    # now plot some results

    # amplification factor over time
    plt.plot(demo.sample_index, demo.stats["base"]['amplification'], 'k-',
             demo.sample_index, demo.stats["basegc"]['amplification'], 'r-',
             demo.sample_index, demo.stats["wpgc"]['amplification'], 'g-',
             demo.sample_index, demo.stats["wpnegc"]['amplification'], 'b-')
    plt.show()
    #plt.savefig(fname=)

#
# MAIN ENTRY POINT
#
if __name__ == "__main__":
    # execute only if run as a script
    main()
