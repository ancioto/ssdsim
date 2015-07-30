#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This simulation evaluates the different performances varying the NAND (total blocks and page per block).
"""

# IMPORTS
from simulator.Simulation import Simulation, SIM_SAMPLING_HOST_WRITE
from simulator.NAND.NANDFactory import get_instance, GARBAGECOLLECTOR_SIMPLE


def main():
    # create the simulation
    demo = Simulation(simulation_name="nand_parameters_test",
                      sample_size=10 ** 5, sampling_type=SIM_SAMPLING_HOST_WRITE)
    demo.init_simulation(base_path="./simulations/RESULTS/")

    # create various disks with different gc parameters
    for name, blocks, pages in (
            # the size is kept constant (128 MiB)
            ("2x16384", 2, 16384),  # 128 MiB
            ("16x2048", 16, 2048),  # 128 MiB
            ("32x1024", 32, 1024),  # 128 MiB
            ("64x512", 64, 512),  # 128 MiB
            ("128x256", 128, 256),  # 128 MiB
            ("256x128", 256, 128),  # original parameters (128 MiB)
            ("512x64", 512, 64),  # 128 MiB
            ("1024x32", 1024, 32)):  # 128 MiB
            # ("2048x16", 2048, 16)):  # 128 MiB Simulation too expensive (anyway no improvements in results)
            # ("4096x8", 4096, 8),  # 128 MiB Simulation too expensive (anyway no improvements in results)
            # ("16384x2", 16384, 2),  # 128 MiB Simulation too expensive (anyway no improvements in results)
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
