import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

    def test_part_1(self):
        self.assertEqual(3068, day.solve1(self.data, True))

    def test_part_2(self):
        self.assertEqual(1514285714288, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(3111, day.solve1(data))
        self.assertEqual(1526744186042, day.solve2(data))
