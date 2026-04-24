"""Run timing and operation-count benchmarks for sorting algorithms.

This script produces reproducible CSV outputs for three timing scenarios:
- random
- sorted
- reversed

It also produces a comparison/swap CSV based on the instrumented algorithms.
"""

from __future__ import annotations

import csv
import os
import random
import time
from pathlib import Path
from statistics import mean
from typing import Callable, Dict, List

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
from algorithms.sorting_instrumented import (
    bubble_sort_instrumented,
    heap_sort_instrumented,
    insertion_sort_instrumented,
    merge_sort_instrumented,
    quick_sort_instrumented,
    selection_sort_instrumented,
    shell_sort_instrumented,
)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

ALGORITHMS: Dict[str, Callable[[List[int]], List[int]]] = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Shell Sort": shell_sort,
    "Tim Sort": tim_sort,
}

INSTRUMENTED: Dict[str, Callable[[List[int]], Dict[str, object]]] = {
    "Bubble Sort": bubble_sort_instrumented,
    "Insertion Sort": insertion_sort_instrumented,
    "Selection Sort": selection_sort_instrumented,
    "Merge Sort": merge_sort_instrumented,
    "Quick Sort": quick_sort_instrumented,
    "Heap Sort": heap_sort_instrumented,
    "Shell Sort": shell_sort_instrumented,
}

SCENARIOS = {
    "random": lambda n, rng: [rng.randint(0, max(1, n * 10)) for _ in range(n)],
    "sorted": lambda n, rng: list(range(n)),
    "reversed": lambda n, rng: list(range(n, 0, -1)),
}

SIZES = [100, 500, 1_000, 2_000, 5_000, 10_000, 20_000]
REPEATS = 2
O2_ALGOS = {"Bubble Sort", "Insertion Sort", "Selection Sort"}
O2_MAX_SIZE = 5_000
RANDOM_SEED = 42


def timed(fn: Callable[[List[int]], List[int]], arr: List[int]) -> float:
    start = time.perf_counter()
    fn(arr)
    return round(time.perf_counter() - start, 8)


def run_scenario(scenario_name: str, generator: Callable[[int, random.Random], List[int]], rng: random.Random) -> List[dict]:
    rows: List[dict] = []
    print(f"\n{'=' * 60}\nScenario: {scenario_name.upper()}\n{'=' * 60}")

    for size in SIZES:
        samples = [generator(size, rng) for _ in range(REPEATS)]
        for algorithm_name, fn in ALGORITHMS.items():
            if algorithm_name in O2_ALGOS and size > O2_MAX_SIZE:
                rows.append(
                    {
                        "algorithm": algorithm_name,
                        "scenario": scenario_name,
                        "size": size,
                        "time_s": None,
                    }
                )
                continue

            timings = [timed(fn, sample[:]) for sample in samples]
            average_time = round(mean(timings), 8)
            print(f"  {algorithm_name:<15} n={size:>6,}  {average_time:.6f}s")
            rows.append(
                {
                    "algorithm": algorithm_name,
                    "scenario": scenario_name,
                    "size": size,
                    "time_s": average_time,
                }
            )

    return rows


def run_operations(rng: random.Random) -> List[dict]:
    rows: List[dict] = []
    sizes = [100, 500, 1_000, 2_000, 5_000]

    print(f"\n{'=' * 60}\nOperation counts\n{'=' * 60}")
    for size in sizes:
        samples = [[rng.randint(0, max(1, size * 10)) for _ in range(size)] for _ in range(REPEATS)]
        for algorithm_name, fn in INSTRUMENTED.items():
            outcomes = [fn(sample[:]) for sample in samples]
            average_comparisons = round(mean(result["comparisons"] for result in outcomes), 2)
            average_swaps = round(mean(result["swaps"] for result in outcomes), 2)
            print(
                f"  {algorithm_name:<15} n={size:>6,}  comparisons={average_comparisons:>10}  swaps={average_swaps:>10}"
            )
            rows.append(
                {
                    "algorithm": algorithm_name,
                    "size": size,
                    "comparisons": average_comparisons,
                    "swaps": average_swaps,
                }
            )

    return rows


def save_csv(rows: List[dict], path: Path, fieldnames: List[str]) -> None:
    os.makedirs(path.parent, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved -> {path}")


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    all_rows: List[dict] = []

    for scenario_name, generator in SCENARIOS.items():
        scenario_rows = run_scenario(scenario_name, generator, rng)
        all_rows.extend(scenario_rows)
        save_csv(
            scenario_rows,
            DATA_DIR / f"results_{scenario_name}.csv",
            ["algorithm", "scenario", "size", "time_s"],
        )

    save_csv(
        all_rows,
        DATA_DIR / "results_all_scenarios.csv",
        ["algorithm", "scenario", "size", "time_s"],
    )

    random_rows = [row for row in all_rows if row["scenario"] == "random"]
    save_csv(
        random_rows,
        DATA_DIR / "results.csv",
        ["algorithm", "scenario", "size", "time_s"],
    )

    operation_rows = run_operations(rng)
    save_csv(
        operation_rows,
        DATA_DIR / "results_operations.csv",
        ["algorithm", "size", "comparisons", "swaps"],
    )


if __name__ == "__main__":
    main()
