import pytest
from osc_replicator_pkg.utils import flatten_osc_args


def test_flatten_simple():
    assert flatten_osc_args([1, 2, 3]) == [1, 2, 3]
    assert flatten_osc_args((1, 2, 3)) == [1, 2, 3]
    assert flatten_osc_args([1, [2, 3], 4]) == [1, 2, 3, 4]
    assert flatten_osc_args([1, (2, [3, 4]), 5]) == [1, 2, 3, 4, 5]


def test_flatten_types():
    assert flatten_osc_args(["a", 1, 2.0, True, None]) == ["a", 1, 2.0, True, None]
    # Should ignore dicts, sets, etc.
    assert flatten_osc_args([1, {"bad": 2}, [3, 4]]) == [1, 3, 4]


def test_flatten_empty():
    assert flatten_osc_args([]) == []
    assert flatten_osc_args([[], []]) == []
