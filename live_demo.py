"""Live demo runner for oral defense.

Usage examples:
  python live_demo.py --arr "9,3,5,1,8,2,7,4,6"
  python live_demo.py --arr "[9,3,5,1,8,2,7,4,6]" --save
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
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


def parse_array(raw: str) -> List[int]:
    raw = raw.strip()
    if raw.startswith("["):
        values = json.loads(raw)
        if not isinstance(values, list):
            raise ValueError("JSON input must be a list")
        return [int(x) for x in values]

    parts = [part.strip() for part in raw.split(",") if part.strip()]
    if not parts:
        raise ValueError("Input array is empty")
    return [int(x) for x in parts]


def run_plain(arr: List[int]) -> Dict[str, Dict[str, object]]:
    results: Dict[str, Dict[str, object]] = {}
    for name, fn in ALGORITHMS.items():
        start = time.perf_counter()
        sorted_arr = fn(arr)
        elapsed_ms = (time.perf_counter() - start) * 1000
        results[name] = {
            "sorted": sorted_arr,
            "time_ms": round(elapsed_ms, 6),
        }
    return results


def run_instrumented(arr: List[int]) -> Dict[str, Dict[str, object]]:
    results: Dict[str, Dict[str, object]] = {}
    for name, fn in INSTRUMENTED.items():
        output = fn(arr)
        results[name] = {
            "comparisons": int(output["comparisons"]),
            "swaps": int(output["swaps"]),
        }
    return results


def save_outputs(
    arr: List[int],
    plain: Dict[str, Dict[str, object]],
    instrumented: Dict[str, Dict[str, object]],
) -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    json_path = data_dir / "live_demo_summary.json"
    csv_path = data_dir / "live_demo_results.csv"

    consensus = next(iter(plain.values()))["sorted"]
    payload = {
        "input": arr,
        "consensus_sorted": consensus,
        "plain": plain,
        "instrumented": instrumented,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["algorithm", "time_ms", "comparisons", "swaps"],
        )
        writer.writeheader()
        for name in ALGORITHMS:
            row = {
                "algorithm": name,
                "time_ms": plain[name]["time_ms"],
                "comparisons": instrumented.get(name, {}).get("comparisons"),
                "swaps": instrumented.get(name, {}).get("swaps"),
            }
            writer.writerow(row)

    print(f"Saved JSON summary -> {json_path}")
    print(f"Saved CSV summary  -> {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run all sorting algorithms for a custom array and print live-defense evidence."
    )
    parser.add_argument(
        "--arr",
        default="9,3,5,1,8,2,7,4,6",
        help="Array as comma-separated values or JSON list.",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Also save results to data/live_demo_summary.json and data/live_demo_results.csv.",
    )
    args = parser.parse_args()

    arr = parse_array(args.arr)
    plain = run_plain(arr)
    instrumented = run_instrumented(arr)

    sorted_outputs = [tuple(item["sorted"]) for item in plain.values()]
    all_equal = len(set(sorted_outputs)) == 1
    consensus_sorted = list(sorted_outputs[0])

    print("=" * 64)
    print("LIVE DEMO: Sorting Algorithms")
    print("=" * 64)
    print(f"Input array: {arr}")
    print(f"All algorithms agree: {all_equal}")
    print(f"Sorted output: {consensus_sorted}")

    print("\nRuntime per algorithm (single run):")
    for name, output in plain.items():
        print(f"  {name:<15} {output['time_ms']:>10.6f} ms")

    print("\nOperation counts (instrumented):")
    for name, output in instrumented.items():
        print(
            f"  {name:<15} comparisons={output['comparisons']:>10}  swaps={output['swaps']:>10}"
        )

    if args.save:
        save_outputs(arr, plain, instrumented)


if __name__ == "__main__":
    main()
