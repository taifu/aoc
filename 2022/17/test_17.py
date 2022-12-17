import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

    def test_part_1(self):
        self.assertEqual(3068, day.solve1(self.data))

    def _test_part_2(self):
        self.assertEqual(45000, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(3111, day.solve1(data))
        #self.assertEqual(201491, day.solve2(data))
