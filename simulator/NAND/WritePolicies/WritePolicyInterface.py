# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the Abstract class interface for all Write Policy implementations.
"""

# IMPORTS
from abc import ABCMeta, abstractclassmethod
from simulator.NAND.NANDInterface import NANDInterface


class WritePolicyInterface(NANDInterface, metaclass=ABCMeta):
    """
    To be written ...
    """
    # ATTRIBUTES

    # METHODS
    @abstractclassmethod
    def full_block_write_policy(self, block=0, page=0):
        """

        :param block:
        :return:
        """
        # TO BE IMPLEMENTED IN REAL CLASS
        return NotImplemented
