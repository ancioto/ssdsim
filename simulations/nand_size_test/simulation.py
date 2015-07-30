#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This simulation evaluates the different performances varying the NAND total size, keeping the same
write policy (default) and simple gc and a ratio of 2:1 between blocks and page per blocks.
"""

# IMPORTS
from simulator.Simulation import Simulation, SIM_SAMPLING_HOST_WRITE
from simulator.NAND.NANDFactory import get_instance, GARBAGECOLLECTOR_SIMPLE


def main():
    # create the simulation
    demo = Simulation(simulation_name="nand_size_test",
                      sample_size=10 ** 6, sampling_type=SIM_SAMPLING_HOST_WRITE)
    demo.init_simulation(base_path="./simulations/RESULTS/")

    # create various disks with different gc parameters
    for name, blocks, pages in (
            # Increase size
            ("256M", 256, 128),  # 256 MiB
            ("512M", 512, 256),  # 512 MiB
            ("2G", 1024, 512),  # 2 GiB
            ("8G", 2048, 1024),  # 8 GiB
            ):
        demo.add_disk(name, get_instance(garbagecollector=GARBAGECOLLECTOR_SIMPLE,
                                         total_blocks=blocks, pages_per_block=pages))

    # run the simulation
    demo.run()

#
# MAIN ENTRY POINT
#
if __name__ == "__main__":
    # execute only if run as a script
    main()
