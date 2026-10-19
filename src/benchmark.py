"""Compare how long deterministic and randomized Quicksort take.

The experiment tests three input arrangements and several list sizes. Each
case is repeated to reduce dependence on a single timing measurement.
Output files are saved under ``results/`` in the project root.

Run from the project root: python3 src/benchmark.py
"""

import csv
import random
import statistics
import sys
import time
from pathlib import Path

# Reuse the actual implementations rather than duplicating sorting code.
from quicksort import deterministic_quicksort, randomized_quicksort

# Resolve paths relative to this script, regardless of the current directory.
ROOT = Path(__file__).resolve().parents[1]
SIZES = (100, 400, 800)  # Number of elements in each test list.
TRIALS = 5                # Number of measurements for each configuration.
SEED = 2026              # Fixed seed for reproducible sample inputs.


def make_data(size: int, distribution: str, rng: random.Random) -> list[int]:
    """Generate an input list with the requested ordering.

    Random lists may include duplicates. Sorted and reverse-sorted lists help
    expose the poor pivot choices made by deterministic last-pivot Quicksort.
    """
    if distribution == "random":
        return [rng.randint(-10_000, 10_000) for _ in range(size)]
    if distribution == "sorted":
        return list(range(size))
    if distribution == "reverse-sorted":
        return list(range(size - 1, -1, -1))
    # Reject typos instead of silently running an unintended experiment.
    raise ValueError(f"Unknown distribution: {distribution}")


def main() -> None:
    # Use a dedicated RNG to generate repeatable benchmark inputs.
    rng = random.Random(SEED)
    rows = []

    # Measure each algorithm for every combination of distribution and size.
    for distribution in ("random", "sorted", "reverse-sorted"):
        for size in SIZES:
            elapsed = {"deterministic": [], "randomized": []}
            for trial in range(TRIALS):
                # Within one trial, both algorithms receive identical data.
                # This makes the two timing measurements comparable.
                data = make_data(size, distribution, rng)
                expected = sorted(data)  # Trusted correctness reference.

                for method_name, sort_fn in (
                    ("deterministic", deterministic_quicksort),
                    ("randomized", lambda x, t=trial: randomized_quicksort(x, seed=SEED + t)),
                ):
                    # perf_counter is suitable for measuring short durations.
                    start = time.perf_counter()
                    output = sort_fn(data)
                    duration = (time.perf_counter() - start) * 1000  # ms

                    # A fast but incorrect sorting result must not be accepted.
                    assert output == expected, f"Incorrect {method_name} output"
                    elapsed[method_name].append(duration)

            # Summarize multiple trials so the report can compare patterns,
            # rather than relying on a single possibly noisy measurement.
            for method_name, measurements in elapsed.items():
                rows.append({
                    "distribution": distribution,
                    "n": size,
                    "algorithm": method_name,
                    "trials": TRIALS,
                    "mean_ms": round(statistics.mean(measurements), 4),
                    "median_ms": round(statistics.median(measurements), 4),
                    "min_ms": round(min(measurements), 4),
                    "max_ms": round(max(measurements), 4),
                })

    # Save detailed measurements as CSV for spreadsheets or later analysis.
    output_dir = ROOT / "results"
    output_dir.mkdir(exist_ok=True)
    with (output_dir / "benchmark_results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # Build a readable comparison table with mean times for both algorithms.
    lines = ["QUICKSORT BENCHMARK RESULTS", f"Python: {sys.version.split()[0]}",
             f"Trials per case: {TRIALS}; base seed: {SEED}",
             "Time shown: average milliseconds (smaller is better)", "",
             f"{'Distribution':<17} {'Size':>5} {'Fixed pivot (ms)':>19} {'Random pivot (ms)':>19}"]
    for distribution in ("random", "sorted", "reverse-sorted"):
        for size in SIZES:
            # Each distribution/size pair has one record per algorithm.
            records = [r for r in rows if r["distribution"] == distribution and r["n"] == size]
            fixed = next(r["mean_ms"] for r in records if r["algorithm"] == "deterministic")
            rand = next(r["mean_ms"] for r in records if r["algorithm"] == "randomized")
            lines.append(f"{distribution:<17} {size:>5} {fixed:>19.4f} {rand:>19.4f}")

    # Note that measured performance depends on the machine and workload.
    lines += ["", "Times depend on hardware, Python version and system load.",
              "Random pivoting reduces the likelihood of badly unbalanced partitions;",
              "it does not guarantee a faster result on every individual run."]
    summary = "\n".join(lines) + "\n"
    (output_dir / "benchmark_summary.txt").write_text(summary)
    print(summary)


if __name__ == "__main__":
    # Running benchmark.py starts the experiment; importing it does not.
    main()
