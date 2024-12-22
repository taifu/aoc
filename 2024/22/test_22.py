import os
import unittest
import pytest  # type: ignore  # noqa: F401
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        day.Solution._instance = None
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """1
10
100
2024
"""
        self.data_example_2 = """1
2
3
2024
"""

    def test_part_1(self) -> None:
        self.assertEqual(day.solve1(self.data_example), 37327623)

    def test_part_2(self) -> None:
        self.assertEqual(day.solve2(self.data_example_2), 23)

    @pytest.mark.slow  # type: ignore[misc]
    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 15335183969)

    @pytest.mark.slow  # type: ignore[misc]
    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 1696)
