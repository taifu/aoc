import unittest
import pytest

import day_17 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """.#.
..#
###
"""

    def test_parse(self):
        self.assertEqual(day.parse(self.data, 3), {(1, 0, 0), (2, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0)})

    def test_parse_4d(self):
        self.assertEqual(day.parse(self.data, 4), {(1, 0, 0, 0), (2, 1, 0, 0), (0, 2, 0, 0), (1, 2, 0, 0), (2, 2, 0, 0)})

    def test_around(self):
        self.assertEqual(list(day.around((0, 0, 0), 3)), [(-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
                                                          (-1, 0, -1), (-1, 0, 0), (-1, 0, 1),
                                                          (-1, 1, -1), (-1, 1, 0), (-1, 1, 1),
                                                          (0, -1, -1), (0, -1, 0), (0, -1, 1),
                                                          (0, 0, -1), (0, 0, 0), (0, 0, 1),
                                                          (0, 1, -1), (0, 1, 0), (0, 1, 1),
                                                          (1, -1, -1), (1, -1, 0), (1, -1, 1),
                                                          (1, 0, -1), (1, 0, 0), (1, 0, 1),
                                                          (1, 1, -1), (1, 1, 0), (1, 1, 1)])

    def test_around_4d(self):
        self.assertEqual(list(day.around((0, 0, 0, 0), 4)), [(-1, -1, -1, -1), (-1, -1, -1, 0), (-1, -1, -1, 1),
                                                             (-1, -1, 0, -1), (-1, -1, 0, 0), (-1, -1, 0, 1),
                                                             (-1, -1, 1, -1), (-1, -1, 1, 0), (-1, -1, 1, 1),
                                                             (-1, 0, -1, -1), (-1, 0, -1, 0), (-1, 0, -1, 1),
                                                             (-1, 0, 0, -1), (-1, 0, 0, 0), (-1, 0, 0, 1),
                                                             (-1, 0, 1, -1), (-1, 0, 1, 0), (-1, 0, 1, 1),
                                                             (-1, 1, -1, -1), (-1, 1, -1, 0), (-1, 1, -1, 1),
                                                             (-1, 1, 0, -1), (-1, 1, 0, 0), (-1, 1, 0, 1),
                                                             (-1, 1, 1, -1), (-1, 1, 1, 0), (-1, 1, 1, 1),
                                                             (0, -1, -1, -1), (0, -1, -1, 0), (0, -1, -1, 1),
                                                             (0, -1, 0, -1), (0, -1, 0, 0), (0, -1, 0, 1),
                                                             (0, -1, 1, -1), (0, -1, 1, 0), (0, -1, 1, 1),
                                                             (0, 0, -1, -1), (0, 0, -1, 0), (0, 0, -1, 1),
                                                             (0, 0, 0, -1), (0, 0, 0, 0), (0, 0, 0, 1),
                                                             (0, 0, 1, -1), (0, 0, 1, 0), (0, 0, 1, 1),
                                                             (0, 1, -1, -1), (0, 1, -1, 0), (0, 1, -1, 1),
                                                             (0, 1, 0, -1), (0, 1, 0, 0), (0, 1, 0, 1),
                                                             (0, 1, 1, -1), (0, 1, 1, 0), (0, 1, 1, 1),
                                                             (1, -1, -1, -1), (1, -1, -1, 0), (1, -1, -1, 1),
                                                             (1, -1, 0, -1), (1, -1, 0, 0), (1, -1, 0, 1),
                                                             (1, -1, 1, -1), (1, -1, 1, 0), (1, -1, 1, 1),
                                                             (1, 0, -1, -1), (1, 0, -1, 0), (1, 0, -1, 1),
                                                             (1, 0, 0, -1), (1, 0, 0, 0), (1, 0, 0, 1),
                                                             (1, 0, 1, -1), (1, 0, 1, 0), (1, 0, 1, 1),
                                                             (1, 1, -1, -1), (1, 1, -1, 0), (1, 1, -1, 1),
                                                             (1, 1, 0, -1), (1, 1, 0, 0), (1, 1, 0, 1),
                                                             (1, 1, 1, -1), (1, 1, 1, 0), (1, 1, 1, 1)])

    def test_part_1(self):
        self.assertEqual(day.solve(self.data), 112)

    def test_part_2(self):
        self.assertEqual(day.solve(self.data, 4), 848)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve(data), 265)
        self.assertEqual(day.solve(data, 4), 1936)