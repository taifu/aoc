import unittest

import day_25 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """5764801
17807724
"""

    def test_part1(self):
        card, door = day.parse(self.data)
        size_card = day.loop_size(card)
        size_door = day.loop_size(door)
        self.assertEqual(size_card, 8)
        self.assertEqual(size_door, 11)
        enc_card = day.transform(card, size_door)
        enc_door = day.transform(door, size_card)
        self.assertEqual(enc_card, enc_door)
        self.assertEqual(enc_card, 14897079)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve(data), 5414549)
