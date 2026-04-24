"""Tests for the instrumented sorting algorithms."""

from __future__ import annotations

import random

import pytest

from algorithms.sorting_instrumented import (
    bubble_sort_instrumented,
    heap_sort_instrumented,
    insertion_sort_instrumented,
    merge_sort_instrumented,
    quick_sort_instrumented,
    selection_sort_instrumented,
    shell_sort_instrumented,
)

ALL_INSTRUMENTED = [
    bubble_sort_instrumented,
    insertion_sort_instrumented,
    selection_sort_instrumented,
    merge_sort_instrumented,
    quick_sort_instrumented,
    heap_sort_instrumented,
    shell_sort_instrumented,
]


@pytest.fixture(params=ALL_INSTRUMENTED, ids=lambda fn: fn.__name__)
def instrumented_sorter(request):
    return request.param


def _assert_result_shape(result):
    assert isinstance(result, dict)
    assert set(result) == {"sorted", "comparisons", "swaps"}
    assert isinstance(result["sorted"], list)
    assert isinstance(result["comparisons"], int)
    assert isinstance(result["swaps"], int)
    assert result["comparisons"] >= 0
    assert result["swaps"] >= 0


@pytest.mark.parametrize(
    "values",
    [
        [],
        [42],
        [2, 1],
        [3, 1, 4, 1, 5],
        [-5, -1, -3, 0, 2, -2],
        list(range(10)),
        list(range(10, 0, -1)),
    ],
)
def test_result_and_input_preservation(instrumented_sorter, values):
    original = values[:]
    result = instrumented_sorter(values)
    _assert_result_shape(result)
    assert result["sorted"] == sorted(values)
    assert values == original
    assert result["sorted"] is not values


def test_selection_sort_comparisons_exact_for_n_items():
    values = [5, 4, 3, 2, 1]
    result = selection_sort_instrumented(values)
    _assert_result_shape(result)
    assert result["comparisons"] == len(values) * (len(values) - 1) // 2
    assert result["sorted"] == sorted(values)


@pytest.mark.parametrize("size", [2, 5, 10])
def test_sorted_input_is_fast_for_bubble_and_insertion(size):
    values = list(range(size))

    bubble = bubble_sort_instrumented(values)
    insertion = insertion_sort_instrumented(values)

    assert bubble["comparisons"] == max(0, size - 1)
    assert insertion["comparisons"] == max(0, size - 1)
    assert bubble["sorted"] == values
    assert insertion["sorted"] == values


@pytest.mark.parametrize("size", [5, 10, 25])
def test_random_inputs_return_sorted_lists(size):
    rng = random.Random(9000 + size)
    values = [rng.randint(-500, 500) for _ in range(size)]

    for sorter in ALL_INSTRUMENTED:
        result = sorter(values)
        _assert_result_shape(result)
        assert result["sorted"] == sorted(values)
