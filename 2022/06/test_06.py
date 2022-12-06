import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

    def test_part_1(self):
        self.assertEqual(7, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(19, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 1582)
        self.assertEqual(day.solve2(data), 3588)
