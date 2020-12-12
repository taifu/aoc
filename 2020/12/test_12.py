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
        self.assertEqual(day.solve(self.data), 25)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data), 286)
