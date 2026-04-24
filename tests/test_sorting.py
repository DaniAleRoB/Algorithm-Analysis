"""Correctness tests for the plain sorting algorithms."""

from __future__ import annotations

import random

import pytest

from algorithms.sorting import (
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
    shell_sort,
    tim_sort,
)

ALL_SORTS = [
    bubble_sort,
    insertion_sort,
    selection_sort,
    merge_sort,
    quick_sort,
    heap_sort,
    shell_sort,
    tim_sort,
]


@pytest.fixture(params=ALL_SORTS, ids=lambda fn: fn.__name__)
def sorter(request):
    return request.param


@pytest.mark.parametrize(
    "values",
    [
        [],
        [42],
        [1, 2],
        [2, 1],
        [1, 1, 1, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [-5, -1, -3, 0, 2, -2],
        list(range(20)),
        list(range(20, 0, -1)),
    ],
)
def test_expected_output(sorter, values):
    original = values[:]
    result = sorter(values)
    assert result == sorted(values)
    assert values == original
    assert result is not values


@pytest.mark.parametrize("size", [0, 1, 2, 5, 10, 25])
def test_random_inputs(sorter, size):
    rng = random.Random(1234 + size)
    values = [rng.randint(-100, 100) for _ in range(size)]
    original = values[:]
    assert sorter(values) == sorted(values)
    assert values == original


@pytest.mark.parametrize("size", [5, 10, 25])
def test_against_python_sorted(sorter, size):
    rng = random.Random(4321 + size)
    for _ in range(10):
        values = [rng.randint(-1_000, 1_000) for _ in range(size)]
        assert sorter(values) == sorted(values)
