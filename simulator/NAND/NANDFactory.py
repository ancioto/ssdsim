# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
Generates new NAND with custom Policies and Garbage Collectors
"""

# IMPORTS
from simulator.NAND.BaseNANDDisk import BaseNANDDisk
from simulator.NAND.WritePolicies.WritePolicyDefault import WritePolicyDefault
from simulator.NAND.WritePolicies.WritePolicyInPlace import WritePolicyInPlace
from simulator.NAND.WritePolicies.WritePolicyInPlaceNoErase import WritePolicyInPlaceNoErase


# SETTINGS
WRITEPOLICY_DEFAULT = 'WP_DEFAULT'
WRITEPOLICY_INPLACE = 'WP_IP'
WRITEPOLICY_INPLACE_NOERASE = 'WP_IP_NE'


# FUNCTIONS
def get_class(writepolicy=WRITEPOLICY_DEFAULT):
    """

    :param writepolicy:
    :return:
    """
    if writepolicy == WRITEPOLICY_DEFAULT:
        return type("", (BaseNANDDisk, WritePolicyDefault), {})
    elif writepolicy == WRITEPOLICY_INPLACE:
        return type("NANDWPIP", (BaseNANDDisk, WritePolicyInPlace), {})
    elif writepolicy == WRITEPOLICY_INPLACE_NOERASE:
        return type("NANDWPIPNE", (BaseNANDDisk, WritePolicyInPlaceNoErase), {})
    else:
        raise ValueError("Invalid write policy")


def get_instance(writepolicy=WRITEPOLICY_DEFAULT):
    """

    :param writepolicy:
    :return:
    """
    return get_class(writepolicy)()  # the second parenthesis is the class constructor
