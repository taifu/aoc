import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    def test_part_1(self) -> None:
        self.assertEqual(36, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(81, day.solve2(self.data_example))

    def test_solution(self) -> None:
        self.assertEqual(day.solve1(self.data), 510)

    def test_solution_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 1058)
