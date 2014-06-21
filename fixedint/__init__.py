#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import FixedInt, MutableFixedInt

def test(verbosity=1, repeat=1):
    from . import test_fixedint
    return test_fixedint.run(verbosity, repeat)
