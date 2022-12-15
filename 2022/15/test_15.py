import unittest
import pytest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

    def test_part_1(self):
        self.assertEqual(26, day.solve1(self.data, row=10))

    def test_part_2(self):
        self.assertEqual(56000011, day.solve2(self.data, space=20))

    @pytest.mark.slow
    def test_solution(self):
        import os
        with open(os.path.dirname(__file__) + "/input.txt") as f_data:
            data = f_data.read()
            self.assertEqual(day.solve1(data), 4883971)
            self.assertEqual(day.solve2(data), 12691026767556)
