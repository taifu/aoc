import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

    def test_part_1(self) -> None:
        self.assertEqual(4361, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(467835, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 544664)
        self.assertEqual(day.solve2(self.data), 84495585)
