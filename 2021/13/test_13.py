import unittest

import day_13 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
        self.part_2 = """
#####
#...#
#...#
#...#
#####
"""
        self.solution_2 = """
####.###..#....#..#.###..###..####.#..#
#....#..#.#....#..#.#..#.#..#.#....#..#
###..###..#....#..#.###..#..#.###..####
#....#..#.#....#..#.#..#.###..#....#..#
#....#..#.#....#..#.#..#.#.#..#....#..#
####.###..####..##..###..#..#.#....#..#
"""

    def test_part_1(self):
        self.assertEqual(17, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(self.part_2, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 708)
        self.assertEqual(day.solve2(data), self.solution_2)
