# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the Abstract class interface for all Write Policy implementations.
"""

# IMPORTS
from abc import ABCMeta, abstractclassmethod
from simulator.NAND.common import check_block, check_page


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
        return NotImplemented
