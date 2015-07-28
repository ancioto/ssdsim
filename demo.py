#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is a demo just to play with the simulation library.
"""

# TODO: this file will be migrated.

# IMPORTS
from scipy.stats import randint
from simulator.NAND.NANDFactory import get_instance, WRITEPOLICY_INPLACE, WRITEPOLICY_INPLACE_NOERASE, \
    GARBAGECOLLECTOR_SIMPLE

# initialize a new simulation
d1 = get_instance()
d2 = get_instance(garbagecollector=GARBAGECOLLECTOR_SIMPLE)
d3 = get_instance(WRITEPOLICY_INPLACE)
d4 = get_instance(WRITEPOLICY_INPLACE_NOERASE, GARBAGECOLLECTOR_SIMPLE)

# write approximately 10 MiB of random data
sample = 50000
b = randint.rvs(0, d1.total_blocks, size=sample)
p = randint.rvs(0, d1.pages_per_block, size=sample)

for i in range(0, sample):
    d1.host_write_page(block=b[i], page=p[i])
    d2.host_write_page(block=b[i], page=p[i])
    d3.host_write_page(block=b[i], page=p[i])
    d4.host_write_page(block=b[i], page=p[i])

    if i in (1000, 10000, 25000):
        # check
        print("------- {}\n{}\n{}\n{}\n{}\n".format(i, d1, d2, d3, d4))

# check
print("\n\n#### FINAL #####\n\n{}\n{}\n{}\n{}\n".format(d1, d2, d3, d4))
