import unittest
import os

day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/example.txt").read()

    def test_part_1(self) -> None:
        self.assertEqual(288, day.solve1(self.data))

    def test_part_2(self) -> None:
        self.assertEqual(71503, day.solve2(self.data))

    def test_solution(self) -> None:
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 303600)
        self.assertEqual(day.solve2(data), 23654842)
