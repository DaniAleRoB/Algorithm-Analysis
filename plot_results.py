"""Create static plots from the benchmark CSV outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PLOTS_DIR = BASE_DIR / "plots"

sns.set_theme(style="darkgrid", palette="tab10")
PLOTS_DIR.mkdir(exist_ok=True)

NLOGN_ALGOS = ["Merge Sort", "Quick Sort", "Heap Sort", "Shell Sort", "Tim Sort"]


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    df_time = pd.read_csv(DATA_DIR / "results_all_scenarios.csv")
    df_time["time_ms"] = df_time["time_s"] * 1000
    df_ops = pd.read_csv(DATA_DIR / "results_operations.csv")
    return df_time, df_ops


def _format_axes(ax: plt.Axes) -> None:
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda value, _: f"{int(value):,}"))


def plot_time_by_scenario(df_time: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
    scenarios = ["random", "sorted", "reversed"]

    for ax, scenario in zip(axes, scenarios):
        subset = df_time[df_time["scenario"] == scenario].dropna(subset=["time_ms"])
        for algorithm_name, group in subset.groupby("algorithm"):
            ax.plot(group["size"], group["time_ms"], marker="o", linewidth=1.5, label=algorithm_name)
        ax.set_title(f"{scenario.title()} input")
        ax.set_xlabel("Input size (n)")
        _format_axes(ax)

    axes[0].set_ylabel("Time (ms)")
    axes[-1].legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.suptitle("Sorting Algorithms: Execution Time vs Input Size", y=1.02)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "time_by_scenario.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_nlogn_zoom(df_time: pd.DataFrame) -> None:
    subset = df_time[(df_time["scenario"] == "random") & (df_time["algorithm"].isin(NLOGN_ALGOS))].dropna(
        subset=["time_ms"]
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    for algorithm_name, group in subset.groupby("algorithm"):
        ax.plot(group["size"], group["time_ms"], marker="o", linewidth=1.8, label=algorithm_name)
    ax.set_title("O(n log n) Algorithms on Random Input")
    ax.set_xlabel("Input size (n)")
    ax.set_ylabel("Time (ms)")
    _format_axes(ax)
    ax.legend()
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "nlogn_random_zoom.png", dpi=160)
    plt.close(fig)


def plot_operation_counts(df_ops: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharex=True)
    metrics = [("comparisons", "Comparisons"), ("swaps", "Swaps / moves")]

    for ax, (column, title) in zip(axes, metrics):
        for algorithm_name, group in df_ops.groupby("algorithm"):
            ax.plot(group["size"], group[column], marker="o", linewidth=1.5, label=algorithm_name)
        ax.set_title(title)
        ax.set_xlabel("Input size (n)")
        ax.set_ylabel(column.title())
        _format_axes(ax)

    axes[0].legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.suptitle("Instrumented Operation Counts", y=1.02)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "operation_counts.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_speedup_heatmap(df_time: pd.DataFrame) -> None:
    random_df = df_time[(df_time["scenario"] == "random") & df_time["time_ms"].notna()].copy()
    pivot = random_df.pivot_table(index="algorithm", columns="size", values="time_ms")
    baseline = pivot.loc["Tim Sort"]
    slowdown = pivot.div(baseline, axis="columns")

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(
        slowdown,
        annot=True,
        fmt=".1f",
        cmap="RdYlGn_r",
        linewidths=0.4,
        ax=ax,
        cbar_kws={"label": "times slower than Tim Sort"},
    )
    ax.set_title("Random Input Slowdown Relative to Tim Sort")
    ax.set_xlabel("Input size (n)")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "slowdown_heatmap.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df_time, df_ops = load_data()
    plot_time_by_scenario(df_time)
    plot_nlogn_zoom(df_time)
    plot_operation_counts(df_ops)
    plot_speedup_heatmap(df_time)
    print(f"Plots saved in {PLOTS_DIR}")


if __name__ == "__main__":
    main()
