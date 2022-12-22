import os
import pytest
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.real_data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

    def test_part_1(self):
        self.assertEqual(6032, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(5031, day.solve2(self.data))

    def test_solution_part_1(self):
        self.assertEqual(36518, day.solve1(self.real_data))

    def _test_solution_part_2(self):
        self.assertEqual(3352886133831, day.solve2(self.real_data))
