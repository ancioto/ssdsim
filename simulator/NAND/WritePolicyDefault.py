# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the defualt policy for writes in case the block is full:
just find the first available page in a different block.
"""

# IMPORTS
from simulator.NAND.WritePolicyInterface import WritePolicyInterface
from simulator.NAND.common import check_block, check_page, PAGE_DIRTY, PAGE_IN_USE


class WritePolicyDefault(WritePolicyInterface):
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
        # naive policy: just find the first available page in a different block
        for b in range(0, self.total_blocks):
            if b != block and self._ftl[b]['empty'] > 0:
                # FOUND a block with empty pages
                p = self.get_empty_page(block=b)

                # change the status of the original page
                self._ftl[block][page] = PAGE_DIRTY

                # change the status of the new page
                self._ftl[b][p] = PAGE_IN_USE

                # we need to update the statistics
                self._ftl[block]['dirty'] += 1  # we have one more dirty page in this block
                self._ftl[b]['empty'] -= 1  # we lost one empty page in this block
                self._elapsed_time += self.write_page_time  # time spent to write the data
                self._page_write_executed += 1  # one page written
                return True

        # no empty page found
        return False
