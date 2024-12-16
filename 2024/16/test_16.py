import os
import unittest
import pytest  # noqa: F401
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        setattr(day, 'solution', None)
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

    def test_part_1(self) -> None:
        self.assertEqual(7036, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(45, day.solve2(self.data_example))

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 98416)

    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 471)
