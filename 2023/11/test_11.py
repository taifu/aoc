import unittest
import os

day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/example.txt").read()

    def test_part_1(self) -> None:
        self.assertEqual(374, day.solve1(self.data))

    def test_part_2_10(self) -> None:
        self.assertEqual(1030, day.solve2(self.data, 10))

    def test_part_2_100(self) -> None:
        self.assertEqual(8410, day.solve2(self.data, 100))

    def test_solution(self) -> None:
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 9521550)
        self.assertEqual(day.solve2(data), 298932923702)
