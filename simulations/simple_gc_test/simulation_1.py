#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This simulation evaluates the different performances on the same default NAND varying the simple garbage collector
parameters. Write policy is default.

This is a refinement of the previous simulation
"""

# IMPORTS
from simulator.Simulation import Simulation, SIM_SAMPLING_HOST_WRITE
from simulator.NAND.NANDFactory import get_instance, GARBAGECOLLECTOR_SIMPLE


def main():
    # create the simulation
    demo = Simulation(simulation_name="simple_gc_test_1",
                      sample_size=100000, sampling=10000,
                      sampling_type=SIM_SAMPLING_HOST_WRITE)
    demo.init_simulation(base_path="./simulations/RESULTS/")

    # create various disks with different gc parameters
    for name, mintime, dirtiness in (
            ("t500d30", 500, '0.3'),  # original parameters
            ("t500d35", 500, '0.35'),  # varying the dirtiness
            ("t500d40", 500, '0.4'),
            ("t500d45", 500, '0.45'),  # we already know with 0.5 there are failures
            ("t1000d30", 1000, '0.3'),
            ("t1000d35", 1000, '0.35'),
            ("t1000d40", 1000, '0.4'),
            ("t1000d45", 1000, '0.45'),
            ("t10000d30", 1000000, '0.3'),
            ("t10000d35", 1000000, '0.35'),
            ("t10000d40", 1000000, '0.4'),
            ("t10000d45", 1000000, '0.45')):
        demo.add_disk(name, get_instance(garbagecollector=GARBAGECOLLECTOR_SIMPLE,
                                         gc_params={'mintime': mintime,
                                                    'dirtiness': dirtiness}))

    # run the simulation
    demo.run()

#
# MAIN ENTRY POINT
#
if __name__ == "__main__":
    # execute only if run as a script
    main()
