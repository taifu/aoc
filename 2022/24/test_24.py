import os
import pytest
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.real_data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

    def test_part_1(self):
        self.assertEqual(18, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(54, day.solve2(self.data))

    @pytest.mark.slow
    def test_solution_part_1(self):
        self.assertEqual(326, day.solve1(self.real_data))

    @pytest.mark.slow
    def test_solution_part_2(self):
        self.assertEqual(976, day.solve2(self.real_data))
