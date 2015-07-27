# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
Common static values.
"""

# IMPORTS

# DECIMAL PRECISION
# to be used to set the Decimal context in a consistent way
DECIMAL_PRECISION = 6

# THE PAGE STATUSES
# The statuses of a page
PAGE_IN_USE = "U"
PAGE_DIRTY = "D"
PAGE_EMPTY = "E"

PAGE_STATUSES = (PAGE_IN_USE, PAGE_DIRTY, PAGE_EMPTY)
