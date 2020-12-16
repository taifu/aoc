import unittest

import day_12 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """F10
N3
F7
R90
F11
"""

    def test_part_1(self):
        self.assertEqual(day.solve1(self.data), 25)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data), 286)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 445)
        self.assertEqual(day.solve2(data), 42495)
