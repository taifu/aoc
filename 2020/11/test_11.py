import unittest

import day_11 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

    def test_part_1(self):
        self.assertEqual(day.solve(self.data), 37)

    def test_part_2(self):
        self.assertEqual(day.solve(self.data, step=2), 26)
