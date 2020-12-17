import unittest
import pytest

import day_18 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """.#.
..#
###
"""

    def test_solution(self):
        import os
        #data = open(os.path.dirname(__file__) + "/input.txt").read()
        #self.assertEqual(day.solve(data), 265)
        #self.assertEqual(day.solve(data, 4), 1936)
