import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

    def test_part_1(self) -> None:
        self.assertEqual(50, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(24, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 4774877510)
        self.assertEqual(day.solve2(self.data), 1560475800)
