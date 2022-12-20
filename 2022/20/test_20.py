import os
import pytest
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.real_data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data = """1
2
-3
3
-2
0
4
"""

    def test_part_1(self):
        self.assertEqual(3, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(1623178306, day.solve2(self.data))

    def test_solution_part_1(self):
        self.assertEqual(7225, day.solve1(self.real_data))

    def test_solution_part_2(self):
        self.assertEqual(548634267428, day.solve2(self.real_data))
