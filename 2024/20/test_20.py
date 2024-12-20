import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        day.Solution._instance = None
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

    def test_part_1_A(self) -> None:
        self.assertEqual(day.solve1(self.data_example, 2, True), 14)

    def test_part_1_B(self) -> None:
        self.assertEqual(day.solve1(self.data_example, 4, True), 14)

    def test_part_1_J(self) -> None:
        self.assertEqual(day.solve1(self.data_example, 38, True), 1)

    def test_part_1_K(self) -> None:
        self.assertEqual(day.solve1(self.data_example, 64, True), 1)

    def test_part_2(self) -> None:
        self.assertEqual(day.solve2(self.data_example, 76, False, 20), 3)

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 1459)

    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 1016066)
