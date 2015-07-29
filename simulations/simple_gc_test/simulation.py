#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This simulation evaluates the different performances on the same default NAND varying the simple garbage collector
parameters. Write policy is default.
"""

# IMPORTS
from simulator.Simulation import Simulation, SIM_SAMPLING_HOST_WRITE
from simulator.NAND.NANDFactory import get_instance, GARBAGECOLLECTOR_SIMPLE


def main():
    # create the simulation
    demo = Simulation(simulation_name="simple_gc_test",
                      sample_size=100000, sampling=10000,
                      sampling_type=SIM_SAMPLING_HOST_WRITE)
    demo.init_simulation(base_path="./simulations/RESULTS/")

    # create various disks with different gc parameters
    for name, mintime, dirtiness in (
            ("d30", 500, '0.3'),  # original parameters
            ("d10", 500, '0.1'),  # varying the dirtiness
            ("d50", 500, '0.5'),
            ("d90", 500, '0.9'),
            ("d100", 500, '1.0'),
            ("t200", 200, '0.3'),  # varying the mintime
            ("t1000", 1000, '0.3'),  # 1 millisec
            ("t50000", 50000, '0.3'),  # 50 millisec
            ("t500000", 500000, '0.3')):  # 0.5 sec
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
