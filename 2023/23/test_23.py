import os
import unittest
import pytest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = open(os.path.dirname(__file__) + "/example.txt").read()

    def test_part_1(self) -> None:
        self.assertEqual(94, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(154, day.solve2(self.data_example))

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 2370)

    @pytest.mark.slow
    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 6546)