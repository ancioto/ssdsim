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
                      sample_size=10 ** 5, sampling_type=SIM_SAMPLING_HOST_WRITE)
    demo.init_simulation(base_path="./simulations/RESULTS/")

    # create various disks with different gc parameters
    for name, mintime, dirtiness in (
            # changing the mintime
            ("t1", 1, '0.4'),  # 1 microseconds => always check run
            ("t500", 500, '0.4'),  # original parameters (500 microseconds)
            ("t5000", 5000, '0.4'),  # 5000 microseconds
            ("t50000", 50000, '0.4'),  # 50000 microseconds
            ("t500000", 500000, '0.4'),  # 500000 microseconds
            ("t5000000", 5000000, '0.4')):  # 5000000 microseconds
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
