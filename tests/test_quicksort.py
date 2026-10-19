"""Unit tests verifying that both Quicksort implementations sort correctly.

Run from the project root:
    python3 -m unittest discover -s tests -v

The tests cover boundary cases, repeated values, negative values, existing
orderings, random inputs, and preservation of the caller's original list.
"""

import random
import sys
import unittest
from pathlib import Path

# The algorithms live in src/, while this test file lives in tests/.
# Add src/ to the module search path so both functions can be imported when
# running unittest discovery from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from quicksort import deterministic_quicksort, randomized_quicksort


class QuicksortTests(unittest.TestCase):
    """Run identical correctness expectations against both algorithms."""

    def check_both(self, values):
        """Compare both implementations to Python's built-in sorted()."""
        original = list(values)   # Snapshot used to detect accidental mutation.
        expected = sorted(values)  # Reference answer for this particular input.

        # Both functions must produce the same ascending-order result.
        self.assertEqual(deterministic_quicksort(values), expected)
        self.assertEqual(randomized_quicksort(values, seed=42), expected)

        # These public functions promise to return copies, not modify inputs.
        self.assertEqual(values, original, "Functions should not alter input")

    def test_empty_and_singleton(self):
        """An empty list or a one-item list is already sorted."""
        for items in ([], [7]):
            self.check_both(items)

    def test_duplicates_and_negative_numbers(self):
        """Repeated and negative values must keep their correct order."""
        self.check_both([3, -2, 3, 0, -5, 8, 3])

    def test_sorted_and_reverse_sorted(self):
        """Verify correctness even when last-element pivots are unfavorable."""
        self.check_both(list(range(1200)))
        self.check_both(list(range(1199, -1, -1)))

    def test_random_cases(self):
        """Check many randomly generated lists and different list lengths."""
        rng = random.Random(234)  # Reuse the same cases on every test run.
        for _ in range(60):
            self.check_both([rng.randint(-100, 100) for _ in range(rng.randrange(100))])

    def test_seed_reproducibility(self):
        """A given pivot seed should consistently produce a sorted result."""
        items = [9, 5, 4, 2, 8]
        self.assertEqual(randomized_quicksort(items, seed=10),
                         randomized_quicksort(items, seed=10))


if __name__ == "__main__":
    # Also permit running this test file directly instead of using discovery.
    unittest.main()
