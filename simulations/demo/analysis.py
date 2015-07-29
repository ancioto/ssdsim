#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This script elaborates the demo results.
"""

# IMPORTS
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


def main():
    # read the simulation data
    data = dict()
    base_path = Path("./simulations/RESULTS/demo/")
    for d in ("base", "basegc", "wpgc", "wpnegc"):
        fp = base_path.joinpath("raw_data_{}.csv".format(d))
        data[d] = dict()
        for i in range(0, 10):
            data[d][i] = np.genfromtxt(str(fp), dtype=None, skip_header=2, delimiter=',', usecols=[i, ])

    # now plot host write vs disk write
    plt.plot(data["base"][4], data["base"][6], 'k-',
             data["basegc"][4], data["basegc"][6], 'r-',
             data["wpgc"][4], data["wpgc"][6], 'g-',
             data["wpnegc"][4], data["wpnegc"][6], 'b-')
    plt.xlabel('Host write [pages]')
    plt.ylabel('Disk write [pages]')
    plt.title('Random writes of single 4 KiB page')
    plt.grid(True)
    # plt.show()
    plt.savefig(filename=str(base_path.joinpath("write_host_disk.png")), format='png', frameon=True)

#
# MAIN ENTRY POINT
#
if __name__ == "__main__":
    # execute only if run as a script
    main()
