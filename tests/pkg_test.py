#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for pkg."""

import onn


def test_pkg() -> None:
    """Unit test for pkg."""
    assert onn.__package__ == "onn"
