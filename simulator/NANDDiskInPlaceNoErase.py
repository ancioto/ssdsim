# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is an improved NAND cell based on BaseNANDDisk with a different policy for writes:
the garbage collector is run in place: as soon a block is full the block is modified in-memory and written
in a new free block (if available, otherwise the base policy is used). The previous block is left dirty or empty
(a gc will clean it).
"""

# IMPORTS
from simulator.BaseNANDDisk import BaseNANDDisk, check_block, check_page
from simulator import common


# NANDDiskInPlace
class NANDDiskInPlaceNoErase(BaseNANDDisk):
    """
    To be written ...
    """
    # ATTRIBUTES

    # METHODS
    @check_block
    @check_page
    def full_block_write_policy(self, block=0, page=0):
        """

        :param block:
        :return:
        """
        # first we need to be sure there is a free block to execute the copy
        res, newblock = self.get_empty_block()

        if res:
            # change the status of the original page, so we don't need to read it
            self._ftl[block][page] = common.PAGE_DIRTY

            # STEP 1: temporary copy the block data (this also simulates the in-memory change)
            #         this is a read and only useful data are read
            #         also set the original in use pages as dirty
            temp_block = dict()
            for p in range(0, self.pages_per_block):
                # READ and change the status of the original page
                if self.raw_read_page(block=block, page=p):
                    temp_block[p] = common.PAGE_IN_USE  # the page is valid and in use
                    self._ftl[block][p] = common.PAGE_DIRTY  # set the original page as dirty
                    self._ftl[block]['dirty'] += 1  # new dirty page
                else:
                    temp_block[p] = common.PAGE_EMPTY  # reset the page, even if is dirty, for the copy

            # in-memory change
            temp_block[page] = common.PAGE_IN_USE

            # STEP 2: write the IN USE pages only in the new block
            for p in range(0, self.pages_per_block):
                if temp_block[p] == common.PAGE_IN_USE:
                    self.raw_write_page(block=newblock, page=p)

            return True

        # if not, try the base naive approach
        return super().full_block_write_policy(block=block, page=page)
