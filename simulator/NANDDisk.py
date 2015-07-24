# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This is the base class to handle a single NAND cell.
"""

# IMPORTS

class NANDDisk:
    # ATTRIBUTES
    total_blocks = 256
    """ The total physical number of block available. Usually should be a multiple of 2.
        This is an integer value. Must be greater than zero.
    """

    pages_per_block = 64
    """ The number of pages per single block. Usually should be a multiple of 2.
        This is an integer value. Must be greater than zero.
    """

    page_size = 4096
    """ The physical size of a single page in [KiB]. 1 KiB = 2^20.
        This is an integer value. Must be greater than zero.
    """

    block_size = page_size * pages_per_block
    """ The physical size of a single block in [KiB].
        It's computed as the number of pages per block times the size of a page.
        This is an integer value. Must be greater than zero.
    """

    total_disk_size = block_size * total_blocks
    """ The total physical size of this NAND cell in [KiB].
        It's computed as the number of total physical blocks times the size of a block.
        This is an integer value. Must be greater than zero.
    """

    write_page_time = 25
    read_page_time = 250
    erase_block_time = 1500

    # CONSTRUCTOR

    # METHODS
    pass
