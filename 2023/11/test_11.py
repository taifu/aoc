import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = open(os.path.dirname(__file__) + "/example.txt").read()

    def test_part_1(self) -> None:
        self.assertEqual(374, day.solve1(self.data_example))

    def test_part_2_10(self) -> None:
        self.assertEqual(1030, day.solve2(self.data_example, 10))

    def test_part_2_100(self) -> None:
        self.assertEqual(8410, day.solve2(self.data_example, 100))

    def test_solution(self) -> None:
        self.assertEqual(day.solve1(self.data), 9521550)
        self.assertEqual(day.solve2(self.data), 298932923702)
