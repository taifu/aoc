import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +
"""

    def test_part_1(self) -> None:
        self.assertEqual(4277556, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(3263827, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 4878670269096)
        self.assertEqual(day.solve2(self.data), 8674740488592)
