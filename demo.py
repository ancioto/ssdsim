#!/bin/bash

# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is a demo just to play with the simulation library.
"""

# TODO: this file will be migrated.

# IMPORTS
from simulator.BaseNANDDisk import BaseNANDDisk
from simulator.NANDDiskInPlace import NANDDiskInPlace
from scipy.stats import randint

# initialize a new simulation
d1 = BaseNANDDisk()
d2 = NANDDiskInPlace()

# write approximately 10 MiB of random data
sample = 100
b = randint.rvs(0, d1.total_blocks, size=sample)
p = randint.rvs(0, d1.pages_per_block, size=sample)

for i in range(0, sample):
    d1.host_write_page(block=b[i], page=p[i])
    d2.host_write_page(block=b[i], page=p[i])

# check
d1_nonempty = d1.total_pages - d1.number_of_empty_pages()
d2_nonempty = d2.total_pages - d2.number_of_empty_pages()

print("d1 Af:\t\t\t\t {}".format(d1.write_amplification()))
print("d1 Host write:\t\t {} ({} MiB)".format(d1._host_page_write_request, d1._host_page_write_request*4/1024))
print("d1 Disk write:\t\t {} ({} MiB)".format(d1._page_write_executed, d1._page_write_executed*4/1024))
print("d1 Total pages:\t\t {} ({} MiB)".format(d1.total_pages, d1.total_pages*4/1024))
print("d1 Dirty:\t\t\t {} ({} MiB)".format(d1.number_of_dirty_pages(), d1.number_of_dirty_pages()*4/1024))
print("d1 Empty:\t\t\t {} ({} MiB)".format(d1.number_of_empty_pages(), d1.number_of_empty_pages()*4/1024))
print("d1 Failure rate:\t {} % ({} pages)".format(d1.failure_rate(), d1._page_write_failed))
print("d1 Non Empty:\t\t {} ({} MiB)".format(d1_nonempty, d1_nonempty*4/1024))
print("d1 Elapsed time:\t {} [s]".format(d1.elapsed_time()))
print("d1 IOPS:\t\t\t {}".format(d1.IOPS()))
print("d1 Erased blocks:\t {}".format(d1._block_erase_executed))

print("\n")

print("d2 Af:\t\t\t\t {}".format(d2.write_amplification()))
print("d2 Host write:\t\t {} ({} MiB)".format(d2._host_page_write_request, d2._host_page_write_request*4/1024))
print("d2 Disk write:\t\t {} ({} MiB)".format(d2._page_write_executed, d2._page_write_executed*4/1024))
print("d2 Total pages:\t\t {} ({} MiB)".format(d2.total_pages, d2.total_pages*4/1024))
print("d2 Dirty:\t\t\t {} ({} MiB)".format(d2.number_of_dirty_pages(), d2.number_of_dirty_pages()*4/1024))
print("d2 Empty:\t\t\t {} ({} MiB)".format(d2.number_of_empty_pages(), d2.number_of_empty_pages()*4/1024))
print("d2 Failure rate:\t {} % ({} pages)".format(d2.failure_rate(), d2._page_write_failed))
print("d2 Non Empty:\t\t {} ({} MiB)".format(d2_nonempty, d2_nonempty*4/1024))
print("d2 Elapsed time:\t {} [s]".format(d2.elapsed_time()))
print("d2 IOPS:\t\t\t {}".format(d2.IOPS()))
print("d2 Erased blocks:\t {}".format(d2._block_erase_executed))
