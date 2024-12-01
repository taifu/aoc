import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """3   4
4   3
2   5
1   3
3   9
3   3"""

    def test_part_1(self) -> None:
        self.assertEqual(11, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(31, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 2057374)
        self.assertEqual(day.solve2(self.data), 23177084)
