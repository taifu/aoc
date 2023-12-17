import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = open(os.path.dirname(__file__) + "/example.txt").read()
        self.data_example_2 = open(os.path.dirname(__file__) + "/example2.txt").read()

    def test_part_1(self) -> None:
        self.assertEqual(52, day.solve1(self.data_example))

    def test_part_1_2(self) -> None:
        self.assertEqual(1320, day.solve1(self.data_example_2))

    def test_part_2(self) -> None:
        self.assertEqual(145, day.solve2(self.data_example_2))

    def test_solution(self) -> None:
        self.assertEqual(day.solve1(self.data), 520500)
        self.assertEqual(day.solve2(self.data), 213097)