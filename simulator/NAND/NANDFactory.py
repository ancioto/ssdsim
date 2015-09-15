# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
Generates new NAND with custom Policies and Garbage Collectors
"""

# IMPORTS
from decimal import Decimal
from simulator.NAND.BaseNANDDisk import BaseNANDDisk
from simulator.NAND.WritePolicies.WritePolicyDefault import WritePolicyDefault
from simulator.NAND.WritePolicies.WritePolicyInPlace import WritePolicyInPlace
from simulator.NAND.WritePolicies.WritePolicyInPlaceNoErase import WritePolicyInPlaceNoErase
from simulator.NAND.GarbageCollectors.GarbageCollectorNone import GarbageCollectorNone
from simulator.NAND.GarbageCollectors.GarbageCollectorSimple import GarbageCollectorSimple

# SETTINGS
# WRITE POLICY
WRITEPOLICY_DEFAULT = 'WP_DEFAULT'
WRITEPOLICY_INPLACE = 'WP_IP'
WRITEPOLICY_INPLACE_NOERASE = 'WP_IP_NE'

# GARBAGE COLLECTOR
GARBAGECOLLECTOR_NONE = 'GC_NONE'
GARBAGECOLLECTOR_SIMPLE = 'GC_SIMPLE'


# FUNCTIONS
def get_class(writepolicy=WRITEPOLICY_DEFAULT, garbagecollector=GARBAGECOLLECTOR_NONE):
    """

    :param writepolicy:
    :return:
    """
    classname = "NANDDisk"
    wp = WritePolicyDefault
    gc = GarbageCollectorNone

    # GET THE WRITE POLICY
    if writepolicy == WRITEPOLICY_INPLACE:
        wp = WritePolicyInPlace
        classname += "WPIP"
    elif writepolicy == WRITEPOLICY_INPLACE_NOERASE:
        wp = WritePolicyInPlaceNoErase
        classname += "WPIPNE"
    elif writepolicy != WRITEPOLICY_DEFAULT:
        raise ValueError("Invalid write policy")

    # GET THE GARBAGE COLLECTOR
    if garbagecollector == GARBAGECOLLECTOR_SIMPLE:
        gc = GarbageCollectorSimple
        classname += "GCS"
    elif garbagecollector != GARBAGECOLLECTOR_NONE:
        raise ValueError("Invalid garbage collector")

    # ASSEMBLE THE CLASS
    return type(classname, (BaseNANDDisk, wp, gc), {})


def get_instance(writepolicy=WRITEPOLICY_DEFAULT, garbagecollector=GARBAGECOLLECTOR_NONE,
                 total_blocks=256, pages_per_block=128, page_size=4096,
                 write_page_time=40, read_page_time=20, erase_block_time=1500, gc_params=None):
    """

    :param writepolicy:
    :return:
    """
    # create the instance
    obj = get_class(writepolicy, garbagecollector)(  # here the parameters to the constructor
        total_blocks, pages_per_block, page_size, write_page_time, read_page_time, erase_block_time)

    # set the Garbage Collector parameters
    if garbagecollector == GARBAGECOLLECTOR_SIMPLE and gc_params is not None:
        obj.gc_param_mintime = gc_params['mintime']
        obj.gc_param_dirtiness = Decimal(gc_params['dirtiness'])

    return obj
