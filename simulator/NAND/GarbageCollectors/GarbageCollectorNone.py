# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the empty garbage collector. Never executed.
"""

# IMPORTS
from simulator.NAND.GarbageCollectors.GarbageCollectorInterface import GarbageCollectorInterface
from simulator.NAND.common import check_block


class GarbageCollectorNone(GarbageCollectorInterface):
    """
    To be written ...
    """
    # METHODS
    def get_gc_name(self):
        return "none"

    def check_gc_run(self):
        """

        :return:
        """
        # Always skip garbage collector
        return False

    @check_block
    def check_gc_block(self, block=0):
        """

        :param block:
        :return:
        """
        # Always skip garbage collector
        return False

    @check_block
    def execute_gc_block(self, block=0):
        """

        :param block:
        :return:
        """
        # Always skip garbage collector
        return False
