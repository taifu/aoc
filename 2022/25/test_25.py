import os
import pytest
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.real_data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""
        self.pairs = ((1, "1"),
                      (2, "2"),
                      (3, "1="),
                      (4, "1-"),
                      (5, "10"),
                      (6, "11"),
                      (7, "12"),
                      (8, "2="),
                      (9, "2-"),
                      (10, "20"),
                      (15, "1=0"),
                      (20, "1-0"),
                      (1747, "1=-0-2"),
                      (2022, "1=11-2"),
                      (12345, "1-0---0"),
                      (314159265, "1121-1110-1=0"),
                      )

    def test_from_snafu(self):
        for number, snafu in self.pairs:
            self.assertEqual(number, day.from_snafu(snafu))

    def test_to_snafu(self):
        for number, snafu in self.pairs:
            self.assertEqual(snafu, day.to_snafu(number))

    def test_part_1(self):
        self.assertEqual("2=-1=0", day.solve1(self.data))

    def test_solution_part_1(self):
        self.assertEqual("2=2-1-010==-0-1-=--2", day.solve1(self.real_data))
