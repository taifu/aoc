import unittest
import pytest

import day_25 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data_1 = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""

    def test_part_1(self):
        self.assertEqual(day.solve1(self.data_1), 58)

    @pytest.mark.slow
    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 380)
