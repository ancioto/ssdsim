#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is a demo just to play with the simulation library.
"""

# TODO: this file will be migrated.

# IMPORTS
#from simulator.Simulation import Simulation
from simulator.BaseNANDDisk import BaseNANDDisk
from scipy.stats import randint

# initialize a new simulation
#s = Simulation()
d = BaseNANDDisk()

# write approximately 10 MiB of random data
sample = 30000
b = randint.rvs(0, d.total_blocks, size=sample)
p = randint.rvs(0, d.pages_per_block, size=sample)

for i in range(0, sample):
    d.host_write_page(block=b[i], page=p[i])

# check
inuse = d.total_pages - d.number_of_empty_pages()

print("Af:\t\t\t\t {}".format(d.write_amplification()))
print("Host write:\t\t {} ({} MiB)".format(d._host_page_write_request, d._host_page_write_request*4/1024))
print("Disk write:\t\t {} ({} MiB)".format(d._page_write_executed, d._page_write_executed*4/1024))
print("Total pages:\t {} ({} MiB)".format(d.total_pages, d.total_pages*4/1024))
print("Dirty:\t\t\t {} ({} MiB)".format(d.number_of_dirty_pages(), d.number_of_dirty_pages()*4/1024))
print("Empty:\t\t\t {} ({} MiB)".format(d.number_of_empty_pages(), d.number_of_empty_pages()*4/1024))
print("Failure rate:\t {} % ({} pages)".format(d.failure_rate(), d._page_write_failed))
print("In Use:\t\t\t {} ({} MiB)".format(inuse, inuse*4/1024))
print("Elapsed time:\t {} [s]".format(d.elapsed_time()))
print("IOPS:\t\t\t {}".format(d.IOPS()))
