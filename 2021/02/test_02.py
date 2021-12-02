import unittest

import day_02 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

    def test_part_1(self):
        self.assertEqual(150, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(900, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 1693300)
        self.assertEqual(day.solve2(data), 1857958050)
