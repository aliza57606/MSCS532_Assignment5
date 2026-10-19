"""Assignment 5: deterministic and randomized Quicksort implementations.

Both public functions return a new sorted list so the original input is kept
unchanged. They share the same partitioning procedure, but choose pivots
differently:
    - Deterministic Quicksort always uses the last element as its pivot.
    - Randomized Quicksort selects a random pivot from the current subarray.
"""

import random
from typing import List, Optional


def _partition(values: List[int], low: int, high: int) -> int:
    """Put the pivot into its final position and return that position.

    The pivot is stored at ``high``. After partitioning, elements at or to the
    left of the returned index are <= the pivot, and elements to its right
    are > the pivot.
    """
    # The caller has already placed the chosen pivot at the end of this range.
    pivot = values[high]

    # boundary marks where the next value <= pivot should be placed.
    boundary = low

    # Examine every element except the pivot itself.
    for scan in range(low, high):
        if values[scan] <= pivot:
            # Move this smaller/equal value into the left partition.
            values[boundary], values[scan] = values[scan], values[boundary]
            boundary += 1

    # Insert the pivot immediately after all elements <= pivot.
    values[boundary], values[high] = values[high], values[boundary]
    return boundary


def _quicksort(values: List[int], low: int, high: int,
               rng: Optional[random.Random]) -> None:
    """Sort the inclusive index range [low, high] in place.

    Supplying an RNG enables random pivot selection; ``None`` uses the final
    element. Only the smaller partition is processed recursively. The larger
    partition is handled by the while loop, keeping recursion depth bounded
    even for poorly balanced splits.
    """
    # A range containing zero or one element is already sorted.
    while low < high:
        if rng is not None:
            # Pick any index in the current range, including both endpoints.
            pivot_index = rng.randint(low, high)
            # _partition expects the pivot at high, so move it there first.
            values[pivot_index], values[high] = values[high], values[pivot_index]

        # Split the range: smaller/equal values | pivot | greater values.
        pivot_index = _partition(values, low, high)

        # Sort the smaller side recursively to save call-stack memory.
        # Then continue with the larger side in the next loop iteration.
        if pivot_index - low < high - pivot_index:
            _quicksort(values, low, pivot_index - 1, rng)
            low = pivot_index + 1
        else:
            _quicksort(values, pivot_index + 1, high, rng)
            high = pivot_index - 1


def deterministic_quicksort(items: List[int]) -> List[int]:
    """Return a sorted copy using the final element as each pivot.

    Average time: O(n log n). Worst-case time: O(n^2), for example when the
    input is already sorted and the final element creates very uneven splits.
    """
    # Copy first: the internal partition swaps elements in place.
    values = list(items)
    # Sort every index in the copied list; empty lists are handled naturally.
    _quicksort(values, 0, len(values) - 1, rng=None)
    return values


def randomized_quicksort(items: List[int], seed: Optional[int] = None) -> List[int]:
    """Return a sorted copy after choosing a random pivot at each split.

    A fixed seed reproduces the sequence of pivot selections during testing.
    Expected time: O(n log n); a theoretical O(n^2) worst case remains possible.
    """
    values = list(items)
    # Create a separate random generator so this call does not change the
    # program-wide random state. Passing a seed makes runs reproducible.
    _quicksort(values, 0, len(values) - 1, rng=random.Random(seed))
    return values


if __name__ == "__main__":
    # This example runs only when executing this file directly. Importing the
    # sorting functions from tests or benchmarks does not run the demo.
    sample = [9, 3, 7, 1, 5, 3, -2]
    print("Input:                 ", sample)
    print("Deterministic Quicksort:", deterministic_quicksort(sample))
    print("Randomized Quicksort:   ", randomized_quicksort(sample, seed=42))
    print("Original unchanged:     ", sample)
