import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

    def test_part_1(self) -> None:
        self.assertEqual(2, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(4, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 356)
        self.assertEqual(day.solve2(self.data), 413)
