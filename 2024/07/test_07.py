import os
import unittest
import pytest  # type: ignore
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    def test_part_1(self) -> None:
        self.assertEqual(3749, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(11387, day.solve2(self.data_example))

    def test_solution(self) -> None:
        self.assertEqual(day.solve1(self.data), 882304362421)

    @pytest.mark.slow  # type: ignore[misc]
    def test_solution_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 145149066755184)
