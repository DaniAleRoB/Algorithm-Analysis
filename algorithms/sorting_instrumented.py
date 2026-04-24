"""Instrumented sorting algorithms.

Each function returns a dictionary with:
- sorted: sorted copy of the input list
- comparisons: number of element-to-element comparisons performed
- swaps: number of element moves or exchanges performed

The goal is to compare growth rates experimentally, not to measure hardware speed.
"""

from __future__ import annotations

from typing import Dict, List


def _result(arr: List[int], comparisons: int, swaps: int) -> Dict[str, object]:
    return {
        "sorted": arr,
        "comparisons": comparisons,
        "swaps": swaps,
    }


# Bubble Sort: O(n^2) comparisons and swaps in the worst case.
def bubble_sort_instrumented(arr: List[int]) -> Dict[str, object]:
    a = arr[:]
    comparisons = 0
    swaps = 0
    n = len(a)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return _result(a, comparisons, swaps)


# Insertion Sort: O(n) best case, O(n^2) worst case.
def insertion_sort_instrumented(arr: List[int]) -> Dict[str, object]:
    a = arr[:]
    comparisons = 0
    swaps = 0

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
            else:
                break
        a[j + 1] = key

    return _result(a, comparisons, swaps)


# Selection Sort: exactly n*(n-1)/2 comparisons.
def selection_sort_instrumented(arr: List[int]) -> Dict[str, object]:
    a = arr[:]
    comparisons = 0
    swaps = 0
    n = len(a)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1

    return _result(a, comparisons, swaps)


# Merge Sort: O(n log n) comparisons, with element moves counted as swaps.
def merge_sort_instrumented(arr: List[int]) -> Dict[str, object]:
    comparisons = [0]
    swaps = [0]

    def _merge(left: List[int], right: List[int]) -> List[int]:
        result: List[int] = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                swaps[0] += 1
                i += 1
            else:
                result.append(right[j])
                swaps[0] += 1
                j += 1

        if i < len(left):
            result.extend(left[i:])
            swaps[0] += len(left) - i
        if j < len(right):
            result.extend(right[j:])
            swaps[0] += len(right) - j
        return result

    def _sort(values: List[int]) -> List[int]:
        if len(values) <= 1:
            return values[:]
        mid = len(values) // 2
        return _merge(_sort(values[:mid]), _sort(values[mid:]))

    sorted_arr = _sort(arr)
    return _result(sorted_arr, comparisons[0], swaps[0])


# Quick Sort: average O(n log n), worst O(n^2) with a bad pivot.
def quick_sort_instrumented(arr: List[int]) -> Dict[str, object]:
    a = arr[:]
    comparisons = [0]
    swaps = [0]

    def _partition(low: int, high: int) -> int:
        mid = (low + high) // 2
        if a[mid] < a[low]:
            a[low], a[mid] = a[mid], a[low]
            swaps[0] += 1
        if a[high] < a[low]:
            a[low], a[high] = a[high], a[low]
            swaps[0] += 1
        if a[mid] < a[high]:
            a[mid], a[high] = a[high], a[mid]
            swaps[0] += 1

        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            comparisons[0] += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                swaps[0] += 1
        a[i + 1], a[high] = a[high], a[i + 1]
        swaps[0] += 1
        return i + 1

    def _sort(low: int, high: int) -> None:
        if low < high:
            pivot_index = _partition(low, high)
            _sort(low, pivot_index - 1)
            _sort(pivot_index + 1, high)

    _sort(0, len(a) - 1)
    return _result(a, comparisons[0], swaps[0])


# Heap Sort: O(n log n) comparisons, O(1) extra space.
def heap_sort_instrumented(arr: List[int]) -> Dict[str, object]:
    a = arr[:]
    comparisons = [0]
    swaps = [0]
    n = len(a)

    def _heapify(size: int, i: int) -> None:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < size:
            comparisons[0] += 1
            if a[left] > a[largest]:
                largest = left
        if right < size:
            comparisons[0] += 1
            if a[right] > a[largest]:
                largest = right
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            swaps[0] += 1
            _heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(n, i)

    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps[0] += 1
        _heapify(i, 0)

    return _result(a, comparisons[0], swaps[0])


# Shell Sort: counts comparisons and element moves for the chosen gap sequence.
def shell_sort_instrumented(arr: List[int]) -> Dict[str, object]:
    a = arr[:]
    comparisons = 0
    swaps = 0
    n = len(a)
    gap = 1

    while gap < n // 3:
        gap = gap * 3 + 1

    while gap >= 1:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap:
                comparisons += 1
                if a[j - gap] > temp:
                    a[j] = a[j - gap]
                    swaps += 1
                    j -= gap
                else:
                    break
            a[j] = temp
        gap //= 3

    return _result(a, comparisons, swaps)
