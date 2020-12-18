import unittest
from operator import add, mul

import day_18 as day


class TestDay(unittest.TestCase):
    def test_part1_1(self):
        self.assertEqual(day.solve("2 * 3 + (4 * 5)"), 26)

    def test_part1_2(self):
        self.assertEqual(day.solve("5 + (8 * 3 + 9 + 3 * 4 * 3)"), 437)

    def test_part1_3(self):
        self.assertEqual(day.solve("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"), 12240)

    def test_part1_4(self):
        self.assertEqual(day.solve("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"), 13632)

    def test_part2_1(self):
        self.assertEqual(day.solve("1 + (2 * 3) + (4 * (5 + 6))", add), 51)

    def test_part2_2(self):
        self.assertEqual(day.solve("2 * 3 + (4 * 5)", add), 46)

    def test_part2_3(self):
        self.assertEqual(day.solve("5 + (8 * 3 + 9 + 3 * 4 * 3)", add), 1445)

    def test_part2_4(self):
        self.assertEqual(day.solve("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", add), 669060)

    def test_part2_5(self):
        self.assertEqual(day.solve("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", add), 23340)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve(data), 701339185745)
        self.assertEqual(day.solve(data, add), 4208490449905)
        self.assertEqual(day.solve(data, mul), 12312398996)
