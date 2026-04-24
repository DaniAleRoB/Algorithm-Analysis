"""Sorting algorithms used for theoretical and experimental comparison.

Big-O reference:
- Bubble Sort: O(n) best, O(n^2) average/worst, O(1) space
- Insertion Sort: O(n) best, O(n^2) average/worst, O(1) space
- Selection Sort: O(n^2) best/average/worst, O(1) space
- Merge Sort: O(n log n) best/average/worst, O(n) space
- Quick Sort: O(n log n) average, O(n^2) worst, O(log n) average stack space
- Heap Sort: O(n log n) best/average/worst, O(1) extra space
- Shell Sort: depends on gap sequence; typically between O(n log n) and O(n^2)
- Tim Sort: O(n) best, O(n log n) average/worst, O(n) space
"""

from __future__ import annotations

from typing import List


# Bubble Sort: early-exit best case O(n), otherwise O(n^2).
def bubble_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


# Insertion Sort: O(n) best case, O(n^2) average/worst case.
def insertion_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# Selection Sort: O(n^2) in all cases.
def selection_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
    return a


# Merge Sort: O(n log n) in all cases, with O(n) auxiliary space.
def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    result: List[int] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Quick Sort: average O(n log n), worst O(n^2) with bad pivots.
def quick_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    _quick_sort_helper(a, 0, len(a) - 1)
    return a


def _quick_sort_helper(a: List[int], low: int, high: int) -> None:
    if low < high:
        pivot_index = _partition(a, low, high)
        _quick_sort_helper(a, low, pivot_index - 1)
        _quick_sort_helper(a, pivot_index + 1, high)


def _partition(a: List[int], low: int, high: int) -> int:
    mid = (low + high) // 2
    if a[mid] < a[low]:
        a[low], a[mid] = a[mid], a[low]
    if a[high] < a[low]:
        a[low], a[high] = a[high], a[low]
    if a[mid] < a[high]:
        a[mid], a[high] = a[high], a[mid]

    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


# Heap Sort: O(n log n) in all cases, O(1) extra space.
def heap_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    n = len(a)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(a, n, i)

    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        _heapify(a, i, 0)

    return a


def _heapify(a: List[int], n: int, i: int) -> None:
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and a[left] > a[largest]:
        largest = left
    if right < n and a[right] > a[largest]:
        largest = right
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        _heapify(a, n, largest)


# Shell Sort: depends on the gap sequence; this implementation uses Knuth gaps.
def shell_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    n = len(a)
    gap = 1

    while gap < n // 3:
        gap = gap * 3 + 1

    while gap >= 1:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 3

    return a


# Tim Sort: Python's built-in sorting algorithm.
def tim_sort(arr: List[int]) -> List[int]:
    return sorted(arr)
