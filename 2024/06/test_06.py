import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    def test_part_1(self) -> None:
        self.assertEqual(41, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(6, day.solve2(self.data_example))

    def test_solution(self) -> None:
        self.assertEqual(day.solve1(self.data), 4819)

    def test_solution_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 1796)
