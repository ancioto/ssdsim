# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the Abstract class interface for all Garbage Collector implementations.
"""

# IMPORTS
from abc import ABCMeta, abstractclassmethod
from simulator.NAND.NANDInterface import NANDInterface


class GarbageCollectorInterface(NANDInterface, metaclass=ABCMeta):
    """
    To be written ...
    """
    # ATTRIBUTES

    # METHODS
    @abstractclassmethod
    def check_gc_run(self):
        return NotImplemented

    @abstractclassmethod
    def check_gc_block(self, block=0):
        return NotImplemented

    @abstractclassmethod
    def execute_gc_block(self, block=0):
        return NotImplemented

    @abstractclassmethod
    def get_gc_name(self):
        return NotImplemented

    def run_gc(self):
        """

        :return:
        """
        # check the overall conditions to execute the gc
        if self.check_gc_run():
            # run the gc on every block
            execution = False
            for b in range(0, self.total_blocks):
                # check the conditions on this block
                if self.check_gc_block(block=b):
                    # ok, run it
                    res = self.execute_gc_block(block=b)
                    if not execution and res:
                        # ok, the gc was executed on at least one block
                        execution = True

            return execution

        # gc not executed
        return False
