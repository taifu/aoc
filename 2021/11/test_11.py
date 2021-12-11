import unittest

import day_11 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
        self.data_little = """11111
19991
19191
19991
11111
"""

    def test_part_1_little(self):
        self.assertEqual(9, day.solve1(self.data_little, 2))

    def test_part_1(self):
        self.assertEqual(1656, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(195, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 1675)
        self.assertEqual(day.solve2(data), 515)
