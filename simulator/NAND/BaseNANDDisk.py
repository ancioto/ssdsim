# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the base class to handle a single NAND cell in a very naive and basic implementation.
"""

# IMPORTS
from decimal import Decimal, getcontext

import simulator.NAND.common as common
from simulator.NAND.common import get_quantized_decimal as qd, check_block, check_page
from simulator.NAND.common import get_integer_decimal as qz


# BaseNANDDISK class
class BaseNANDDisk:
    """
    This class ...
    """

    # CONSTRUCTOR
    def __init__(self):
        """

        :return:
        """
        # ATTRIBUTES
        # PHYSICAL CHARACTERISTICS
        self.total_blocks = 256
        """ The total physical number of block available. Usually should be a multiple of 2.
            This is an integer value. Must be greater than zero.
        """

        self.pages_per_block = 64
        """ The number of pages per single block. Usually should be a multiple of 2.
            This is an integer value. Must be greater than zero.
        """

        self.page_size = 4096
        """ The physical size of a single page in [Bytes].
            This is an integer value. Must be greater than zero.
        """

        self.total_pages = self.pages_per_block * self.total_blocks
        """ The total physical number of pages available.
            This is an integer value. Must be greater than zero.
        """

        self.block_size = self.page_size * self.pages_per_block
        """ The physical size of a single block in [Bytes].
            It's computed as the number of pages per block times the size of a page.
            This is an integer value. Must be greater than zero.
        """

        self.total_disk_size = self.total_pages * self.page_size
        """ The total physical size of this NAND cell in [Bytes].
            It's computed as the number of total physical blocks times the size of a block.
            This is an integer value. Must be greater than zero.
        """

        self.write_page_time = 250
        """ The time to write a single page in [microseconds] (10^-6 seconds).
            This is an integer value. Must be greater than zero.
        """

        self.read_page_time = 25
        """ The time to read a single page in [microseconds] (10^-6 seconds).
            This is an integer value. Must be greater than zero.
        """

        self.erase_block_time = 1500
        """ The time to erase a single block in [microseconds] (10^-6 seconds).
            This is an integer value. Must be greater than zero.
        """

        # INTERNAL STATISTICS
        self._elapsed_time = 0
        """ Keep track of the total elapsed time for the requested operations [microseconds].
            A microsecond is 10^-6 seconds. This variable is an integer.
        """

        self._host_page_write_request = 0
        """ Number of page written as requested by the host.
            This is an integer value.
        """

        self._page_write_executed = 0
        """ Total number of page actually written by the disk.
            This is an integer value.
        """

        self._page_write_failed = 0
        """ Total number of page unable to be writted due to disk error (no empty pages).
            This is an integer value.
        """

        self._host_page_read_request = 0
        """ Number of page read as requested by the host.
            This is an integer value.
        """

        self._page_read_executed = 0
        """ Total number of page actually read by the disk.
            This is an integer value.
        """

        self._block_erase_executed = 0
        """ Total number of block erase executed.
            This is an integer value.
        """

        # INTERNAL STATE
        self._ftl = dict()
        """ This is the full state of the flash memory.
            It's an array of blocks. Every block is an array of page.
            For every page we keep the status of the page.
            Furthermore, every block has the following extra information:
                empty:  total number of empty pages in the given block;
                dirty:  total number of dirty pages in the given block.
        """

        # set the decimal context
        getcontext().prec = common.DECIMAL_PRECISION

        # initialize the FTL
        for b in range(0, self.total_blocks):
            # for every block initialize the page structure
            self._ftl[b] = dict()
            for p in range(0, self.pages_per_block):
                # for every page set the empty status
                self._ftl[b][p] = common.PAGE_EMPTY

            # for every block initialize the internal data
            self._ftl[b]['empty'] = self.pages_per_block  # all pages are empty
            self._ftl[b]['dirty'] = 0  # no dirty pages at the beginning

    # METHODS
    # PYTHON UTILITIES
    def __str__(self):
        """

        :return:
        """
        return "{} pages per block, {} blocks, {} pages of {} [Bytes]. Capacity {} [MiB]\n" \
               "Dirty: {}\{} ([pages]\[MiB])\n" \
               "Empty: {}\{} ([pages]\[MiB])\n" \
               "In Use: {}\{} ([pages]\[MiB])\n" \
               "Host read: {}\{}, write: {}\{} ([pages]\[MiB])\n" \
               "Disk read: {}\{}, write: {}\{} ([pages]\[MiB])\n" \
               "Erased blocks: {}\{} ([blocks]\[MiB])\n" \
               "Failure rate: {} % ({} [pages], {} [MiB])\n" \
               "Time: {} [s]\t IOPS: {}\t Datarate: {} [MiB\s]\n" \
               "Write Amplification: {}\n" \
               "".format(self.pages_per_block, self.total_blocks, self.total_pages, self.page_size,
                         qd(common.bytes_to_mib(self.total_disk_size)),
                         self.number_of_dirty_pages(),
                         qd(common.pages_to_mib(self.number_of_dirty_pages(), self.page_size)),
                         self.number_of_empty_pages(),
                         qd(common.pages_to_mib(self.number_of_empty_pages(), self.page_size)),
                         self.number_of_in_use_pages(),
                         qd(common.pages_to_mib(self.number_of_in_use_pages(), self.page_size)),
                         self._host_page_read_request,
                         qd(common.pages_to_mib(self._host_page_read_request, self.page_size)),
                         self._host_page_write_request,
                         qd(common.pages_to_mib(self._host_page_write_request, self.page_size)),
                         self._page_read_executed,
                         qd(common.pages_to_mib(self._page_read_executed, self.page_size)),
                         self._page_write_executed,
                         qd(common.pages_to_mib(self._page_write_executed, self.page_size)),
                         self._block_erase_executed,
                         qd(common.bytes_to_mib(self._block_erase_executed * self.block_size)),
                         qd(self.failure_rate()), self._page_write_failed,
                         qd(common.pages_to_mib(self._page_write_failed, self.page_size)),
                         qd(self.elapsed_time()), qz(self.IOPS()), qd(self.data_transfer_rate_host()),
                         qd(self.write_amplification()))

    # STATISTICAL UTILITIES
    def write_amplification(self):
        """

        :return:
        """
        return Decimal(self._page_write_executed) / Decimal(self._host_page_write_request)

    def number_of_empty_pages(self):
        """

        :return:
        """
        tot = 0
        for b in range(0, self.total_blocks):
            tot += self._ftl[b]['empty']
        return tot

    def number_of_dirty_pages(self):
        """

        :return:
        """
        tot = 0
        for b in range(0, self.total_blocks):
            tot += self._ftl[b]['dirty']
        return tot

    def number_of_in_use_pages(self):
        """

        :return:
        """
        return self.total_pages - (self.number_of_empty_pages() + self.number_of_dirty_pages())

    def failure_rate(self):
        """

        :return:
        """
        return Decimal(self._page_write_failed * 100) / Decimal(self._page_write_executed)

    def elapsed_time(self):
        """

        :return:
        """
        return Decimal(self._elapsed_time) / Decimal(1000000)

    def IOPS(self):
        """

        :return:
        """
        ops = self._page_write_executed + self._page_read_executed
        return Decimal(ops) / self.elapsed_time()

    def data_transfer_rate_host(self):
        """

        :return:
        """
        # in MiB
        return common.pages_to_mib((self._host_page_write_request + self._host_page_read_request),
                                   self.page_size) / Decimal(self.elapsed_time())

    # DISK OPERATIONS UTILITIES
    @check_block
    def get_empty_page(self, block=0):
        """

        :param block:
        :return:
        """
        # first check availability
        if self._ftl[block]['empty'] <= 0:
            raise ValueError("No empty pages available in this block.")

        # get the first empty page available in the provided block
        for p in range(0, self.pages_per_block):
            if self._ftl[block][p] == common.PAGE_EMPTY:
                return p

        # should not be reachable
        raise ValueError("No empty pages available in this block.")

    def get_empty_block(self):
        """

        :param block:
        :return:
        """
        # get the first empty block available
        for b in range(0, self.total_blocks):
            if self._ftl[b]['empty'] == self.pages_per_block:
                return True, b

        # should not be reachable
        return False, 0

    # RAW DISK OPERATIONS
    @check_block
    @check_page
    def raw_write_page(self, block=0, page=0):
        """

        :param block:
        :param page:
        :return: True if the write is successful, false otherwise (the write is discarded)
        """
        # read the FTL to check the current status
        s = self._ftl[block][page]

        # if status is EMPTY => WRITE OK
        if s == common.PAGE_EMPTY:
            # change the status of this page
            self._ftl[block][page] = common.PAGE_IN_USE

            # we need to update the statistics
            self._ftl[block]['empty'] -= 1  # we lost one empty page in this block
            self._elapsed_time += self.write_page_time  # time spent to write the data
            self._page_write_executed += 1  # one page written
            return True

        # if status is IN USE => we consider a data change,
        # we use the current disk policy to find a new page to write the new data. In case of success we invalidate
        # the current page, otherwise the operation fails.
        elif s == common.PAGE_IN_USE:
            # is the block full?
            if self._ftl[block]['empty'] <= 0:
                # yes, we need a policy to decide how to write
                if self.full_block_write_policy(block=block, page=page):
                    # all statistic MUST BE updated inside the policy method
                    return True
                else:
                    # we didn't found a suitable place to write the new data, the write request failed
                    # this is a disk error: the garbage collector was unable to make room for new data
                    self._page_write_failed += 1
                    return False
            else:
                # no, we still have space, we just need a new empty page on this block
                # find and write the new page
                newpage = self.get_empty_page(block=block)

                # change the status of this page
                self._ftl[block][page] = common.PAGE_DIRTY

                # change the status of the new page
                self._ftl[block][newpage] = common.PAGE_IN_USE

                # we need to update the statistics
                self._ftl[block]['empty'] -= 1  # we lost one empty page in this block
                self._ftl[block]['dirty'] += 1  # we have one more dirty page in this block
                self._elapsed_time += self.write_page_time  # time spent to write the data
                self._page_write_executed += 1  # one page written
                return True

        # if status is DIRTY => we discard this write operation
        # (it's not a disk error, it's a bad random value)
        return False

    @check_block
    @check_page
    def raw_read_page(self, block=0, page=0):
        """

        :param block:
        :param page:
        :return:
        """
        # read the FTL to check the current status
        s = self._ftl[block][page]

        if s == common.PAGE_IN_USE:
            # update statistics
            self._elapsed_time += self.read_page_time  # time spent to read the data
            self._page_read_executed += 1  # we executed a read of a page
            return True

        # no valid data to read
        return False

    @check_block
    def raw_erase_block(self, block=0):
        """

        :param block:
        :return:
        """
        # should mark the full block as dirty and then erase it
        # as we are in a simulation, we directly erase it
        for p in range(0, self.pages_per_block):
            # for every page set the empty status
            self._ftl[block][p] = common.PAGE_EMPTY

        # for every block initialize the internal data
        self._ftl[block]['empty'] = self.pages_per_block  # all pages are empty
        self._ftl[block]['dirty'] = 0  # fresh as new

        # update the statistics
        self._block_erase_executed += 1  # new erase operation
        self._elapsed_time += self.erase_block_time  # time spent to erase a block
        return True

    @check_block
    @check_page
    def host_write_page(self, block=0, page=0):
        """

        :param block:
        :param page:
        :return:
        """
        if self.raw_write_page(block=block, page=page):
            # update statistics
            self._host_page_write_request += 1  # the host actually asked to write a page
            return True

        return False
