import unittest

import day_03


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
        self.assertEqual(7, day_03.slope(self.wood, 3, 1))

    def test_part_2(self):
        self.assertEqual(336, day_03.multi_slope(self.wood))
