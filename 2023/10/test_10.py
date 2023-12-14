import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/example.txt").read()
        self.data_2 = open(os.path.dirname(__file__) + "/example2.txt").read()

    def test_part_1(self) -> None:
        self.assertEqual(8, day.solve1(self.data))

    def test_part_2(self) -> None:
        self.assertEqual(10, day.solve2(self.data_2))

    def test_solution(self) -> None:
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 6800)
        self.assertEqual(day.solve2(data), 483)
