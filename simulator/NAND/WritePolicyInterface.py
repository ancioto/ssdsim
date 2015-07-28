# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is an improved policy for writes in case the block is full:
the garbage collector is run in place: as soon a block is full the block is modified in-memory and erased.
"""

# IMPORTS
from abc import ABCMeta, abstractclassmethod
from simulator.NAND.common import check_block, check_page


# WritePolicyInPlace
class WritePolicyInterface(metaclass=ABCMeta):
    """
    To be written ...
    """
    # ATTRIBUTES

    # METHODS
    @check_block
    @check_page
    @abstractclassmethod
    def full_block_write_policy(self, block=0, page=0):
        """

        :param block:
        :return:
        """
        # TO BE IMPLEMENTED IN REAL CLASS
        return False
