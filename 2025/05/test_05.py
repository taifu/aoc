import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

    def test_part_1(self) -> None:
        self.assertEqual(3, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(14, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 828)
        self.assertEqual(day.solve2(self.data), 352681648086146)
