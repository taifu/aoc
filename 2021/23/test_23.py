import unittest
import pytest

import day_23 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

    def test_part_1(self):
        self.assertEqual(day.solve1(self.data), 12521)

    @pytest.mark.slow
    def test_part_2(self):
        self.assertEqual(day.solve2(self.data), 44169)

    @pytest.mark.slow
    def _test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 11120)
        self.assertEqual(day.solve2(data), 1319618626668022)
