# Assignment 5: Quicksort Algorithm — Implementation, Analysis, and Randomization

Python implementations of deterministic (fixed last-element pivot) and randomized Quicksort, with correctness tests and a repeatable empirical benchmark.

## Requirements

Python 3.9+; no third-party packages required.

## Run from the project root

```bash
python3 src/quicksort.py
python3 -m unittest discover -s tests -v
python3 src/benchmark.py
```

`src/benchmark.py` rewrites `results/benchmark_results.csv` and `results/benchmark_summary.txt` with **your computer's measured timings**. Results vary by hardware, operating system, and background activity.

## Repository files

- `src/quicksort.py`: both commented algorithms, shared partitioning routine, sample demonstration.
- `src/benchmark.py`: 5 timed trials per combination of 3 sizes × 3 distributions × 2 algorithms; correctness checked before results are recorded.
- `tests/test_quicksort.py`: tests for empty, singleton, duplicates, negatives, sorted/reversed, randomized arrays, seed repeatability, and non-mutating inputs.
- `results/benchmark_results.csv`: measured timings, including mean/median/min/max.
- `results/benchmark_summary.txt`: concise table of measured timings.
- `report/Quicksort_Assignment5_Report.docx` and `.pdf`: written analysis.

## Design choices and key findings

Both algorithms use Lomuto partitioning; the deterministic variant picks the last element, while the randomized variant picks a uniformly random pivot. The smaller partition is processed recursively and the larger partition iteratively, avoiding deep recursion even on adversarial input. This changes stack usage, **not** the O(n²) worst-case runtime.

Fixed last-element pivot selection leads to O(n²) work for ascending or descending unique values. Random pivot selection produces expected O(n log n) time regardless of original input order, although O(n²) remains theoretically possible. Actual benchmark outcomes are discussed in the report.
# MSCS532_Assignment5
