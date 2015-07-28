# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the Abstract class interface for all the NAND implementations and mixins.
It's helpful to resolve the references for the objects.
"""

# IMPORTS
from abc import ABCMeta, abstractclassmethod


class NANDInterface(metaclass=ABCMeta):
    """
    to be done
    """

    @abstractclassmethod
    def __init__(self):
        # ATTRIBUTES
        self.total_blocks = None
        self.pages_per_block = None
        self.page_size = None
        self.total_pages = None
        self.block_size = None
        self.total_disk_size = None
        self.write_page_time = None
        self.read_page_time = None
        self.erase_block_time = None
        self._elapsed_time = None
        self._host_page_write_request = None
        self._page_write_executed = None
        self._page_write_failed = None
        self._host_page_read_request = None
        self._page_read_executed = None
        self._block_erase_executed = None
        self._ftl = None

    # STATISTICAL UTILITIES
    @abstractclassmethod
    def write_amplification(self):
        return NotImplemented

    @abstractclassmethod
    def number_of_empty_pages(self):
        return NotImplemented

    @abstractclassmethod
    def number_of_dirty_pages(self):
        return NotImplemented

    @abstractclassmethod
    def number_of_in_use_pages(self):
        return NotImplemented

    @abstractclassmethod
    def failure_rate(self):
        return NotImplemented

    @abstractclassmethod
    def elapsed_time(self):
        return NotImplemented

    @abstractclassmethod
    def IOPS(self):
        return NotImplemented

    @abstractclassmethod
    def data_transfer_rate_host(self):
        return NotImplemented

    # DISK OPERATIONS UTILITIES
    @abstractclassmethod
    def get_empty_page(self, block=0):
        return NotImplemented

    @abstractclassmethod
    def get_empty_block(self):
        return NotImplemented

    # RAW DISK OPERATIONS
    @abstractclassmethod
    def raw_write_page(self, block=0, page=0):
        return NotImplemented

    @abstractclassmethod
    def raw_read_page(self, block=0, page=0):
        return NotImplemented

    @abstractclassmethod
    def raw_erase_block(self, block=0):
        return NotImplemented

    @abstractclassmethod
    def host_write_page(self, block=0, page=0):
        return NotImplemented

    @abstractclassmethod
    def host_read_page(self, block=0, page=0):
        return NotImplemented
