import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        day.Solution._instance = None
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

    def test_part_1(self) -> None:
        self.assertEqual(day.solve1(self.data_example), 3)

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 3451)
