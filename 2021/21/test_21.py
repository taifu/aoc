import unittest

import day_21 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """Player 1 starting position: 4
Player 2 starting position: 8
"""

    def test_part_1(self):
        self.assertEqual(day.solve1(self.data), 739785)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data), 444356092776315)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 897798)
        self.assertEqual(day.solve2(data), 48868319769358)
