import unittest

import day_03 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.wood = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    def test_part_1(self):
        self.assertEqual(7, day.solve(self.wood, 3, 1))

    def test_part_2(self):
        self.assertEqual(336, day.solve2(self.wood))
