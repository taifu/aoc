import unittest
import pytest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

    def test_part_1(self):
        self.assertEqual(31, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(29, day.solve2(self.data))

    @pytest.mark.slow
    def test_solution(self):
        import os
        with open(os.path.dirname(__file__) + "/input.txt") as f_data:
            data = f_data.read()
            self.assertEqual(day.solve1(data), 534)
            self.assertEqual(day.solve2(data), 525)
