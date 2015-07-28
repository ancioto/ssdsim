# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
Common static values.
"""

# IMPORTS
from decimal import Decimal

# COMMON GLOBAL VALUES

# DECIMAL PRECISION
# to be used to set the Decimal context in a consistent way
DECIMAL_PRECISION = 12
TWOPLACES = Decimal('0.01')
NOPLACES = Decimal('0')

# THE PAGE STATUSES
# The statuses of a page
PAGE_IN_USE = "U"
PAGE_DIRTY = "D"
PAGE_EMPTY = "E"

PAGE_STATUSES = (PAGE_IN_USE, PAGE_DIRTY, PAGE_EMPTY)


# COMMON USEFUL FUNCTIONS
def bytes_to_mib(pbytes=0):
    """
    Convert a number of bytes into megabytes (MiB = 2^20).

    :param pbytes: the integer number of bytes to be converted.
    :return: the Decimal result of the conversion.
    """
    return Decimal(pbytes) / Decimal(1048576)


def pages_to_mib(pages=0, page_size_bytes=4096):
    """
    Convert a number of pages into a size in MiB.

    :param pages: the integer number of pages to be converted.
    :param page_size_bytes: the integer size of a single page in Bytes. Default value is 4096 Bytes (4 KiB).
    :return: the Decimal result of the conversion.
    """
    return bytes_to_mib(pages * page_size_bytes)


def get_quantized_decimal(dec=0):
    """
    Utility method to output Decimals with two decimal places.
    :param dec: a number.
    :return: a Decimal quantized to two decimal places.
    """
    return Decimal(dec).quantize(TWOPLACES)


def get_integer_decimal(dec=0):
    """
    Utility method to output Decimals with zero decimal places.
    :param dec: a number.
    :return: a Decimal quantized to zero decimal places.
    """
    return Decimal(dec).quantize(NOPLACES)
