#!/usr/bin/env python

from __future__ import absolute_import

import re
import random
from operator import mul

from .util import clean_id

"""
Functions for working with Brazilian CEI identifiers.

"""

NONDIGIT = re.compile(r'[^0-9]')
CEI_WEIGHTS = [7, 4, 1, 8, 5, 2, 1, 6, 3, 7, 4]

def validate_cei(cei):
    """Check whether CEI is valid."""
    cei = clean_id(cei)
    # all complete CEI are 12 digits long
    if len(cei) != 12:
        return False
    digits = [int(k) for k in cei]  # identifier digits
    return _cei_check(digits[:-1]) == digits[-1]

def cei_check_digit(cei):
    """Find check digit needed to make a CEI valid."""
    cei = clean_id(cei)
    if len(cei) < 11:
        raise ValueError('CEI must have at least 11 digits: {0}'.format(cei))
    digits = [int(k) for k in cei[:12]]
    return _cei_check(digits)

def format_cei(cei):
    """Applies typical 00.000.00000/00 formatting to CEI."""
    fmt = '{0}.{1}.{2}/{3}'
    cei = clean_id(cei)
    return fmt.format(cei[:2], cei[2:5], cei[5:10], cei[10:])

def pad_cei(cei, validate=True):
    """Takes a CEI that probably had leading zeros and pads it."""
    cei = clean_id(cei)
    cei = '%0.012i' % int(cei)
    if validate and not validate_cei(cei):
        raise ValueError('Invalid CEI: {0}'.format(cei))
    return cei

def random_cei(formatted=True):
    """Create a random, valid CEI identifier."""
    uf = random.randint(11, 53)
    stem = '{0}{1}'.format(uf, random.randint(100000000, 999999999))
    cei = '{0}{1}'.format(stem, cei_check_digit(stem))
    if formatted:
        return format_cei(cei)
    return cei

def _cei_check(digits):
    """Calculate check digit from iterable of integers."""
    digsum = sum(mul(*k) for k in zip(CEI_WEIGHTS, digits))
    modulo = (sum(divmod(digsum % 100, 10)) % 10)
    if modulo == 0:
        return 0
    return 10 - modulo
