"""
Unit and regression test for the flamel package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import flamel


def test_flamel_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "flamel" in sys.modules
