#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This simulation evaluates the different performances varying the NAND (total blocks and page per block).
"""

# IMPORTS
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


def main():
    sim_names = ("256x128", "512x64", "1024x32", "2048x16", "4096x8")
    # "64x512", "128x256" removed as the disk fails

    # read the simulation data
    data = dict()
    base_path = Path("./simulations/RESULTS/nand_parameters_test/")
    for d in sim_names:
        fp = base_path.joinpath("raw_data_{}.csv".format(d))
        data[d] = dict()
        for i in range(0, 10):
            data[d][i] = np.genfromtxt(str(fp), dtype=None, skip_header=2, delimiter=',', usecols=[i, ])

    # convert all times in seconds
    for n in sim_names:
        data[n][0] = np.array(data[n][0] / 1000000)

    # plot host write vs disk write
    plt.figure(1)
    for n in sim_names:
        plt.plot(data[n][4], data[n][6], linestyle='-', label=n)
    plt.yscale('log')
    plt.xscale('log')
    plt.axis([0, 100000, 0, 1000000])  # [xmin, xmax, ymin, ymax]
    plt.xlabel('Host write [log pages]')
    plt.ylabel('Disk write [log pages]')
    plt.title('Random writes of ~100K pages (4 KiB each)')
    plt.legend(loc='best', fancybox=True, framealpha=0.5)
    plt.grid(True)
    plt.savefig(filename=str(base_path.joinpath("write_host_disk.png")), format='png', frameon=True)

    # plot host write time
    plt.figure(2)
    for n in sim_names:
        plt.plot(data[n][0], data[n][4], linestyle='-', label=n)
    plt.xscale('log')
    plt.xlabel('Elapsed time [log seconds]')
    plt.ylabel('Host write [pages]')
    plt.title('Random writes of ~100K pages (4 KiB each)')
    plt.legend(loc='best', fancybox=True, framealpha=0.5)
    plt.grid(True)
    plt.savefig(filename=str(base_path.joinpath("write_host_time.png")), format='png', frameon=True)

    # plot the IOPS
    plt.figure(3)
    for n in sim_names:
        plt.plot(data[n][0], data[n][1], linestyle='-', label=n)
    plt.xscale('log')
    plt.xlabel('Elapsed time [log seconds]')
    plt.ylabel('Host IOPS')
    plt.title('Random writes of ~100K pages (4 KiB each)')
    plt.legend(loc='best', fancybox=True, framealpha=0.5)
    plt.grid(True)
    plt.savefig(filename=str(base_path.joinpath("iops.png")), format='png', frameon=True)

    # plot the Amplification factor
    plt.figure(4)
    for n in sim_names:
        plt.plot(data[n][0], data[n][3], linestyle='-', label=n)
    plt.xscale('log')
    plt.xlabel('Elapsed time [log seconds]')
    plt.ylabel('Write amplification')
    plt.title('Random writes of ~100K pages (4 KiB each)')
    plt.legend(loc='best', fancybox=True, framealpha=0.5)
    plt.grid(True)
    plt.savefig(filename=str(base_path.joinpath("amplification.png")), format='png', frameon=True)

    # plot the bandwidth
    plt.figure(5)
    for n in sim_names:
        plt.plot(data[n][0], data[n][1], linestyle='-', label=n)
    plt.xscale('log')
    plt.xlabel('Elapsed time [log seconds]')
    plt.ylabel('Bandwidth [MiB\s]')
    plt.title('Random writes of ~100K pages (4 KiB each)')
    plt.legend(loc='best', fancybox=True, framealpha=0.5)
    plt.grid(True)
    plt.savefig(filename=str(base_path.joinpath("bandwidth.png")), format='png', frameon=True)

#
# MAIN ENTRY POINT
#
if __name__ == "__main__":
    # execute only if run as a script
    main()
