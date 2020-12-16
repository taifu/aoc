import unittest

import day_08 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

    def test_part_1(self):
        acc, res = day.solve1(self.data)
        self.assertEqual(res, False)
        self.assertEqual(acc, 5)

    def test_part_2(self):
        acc = day.solve2(self.data)
        self.assertEqual(acc, 8)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data)[0], 1614)
        self.assertEqual(day.solve2(data), 1260)
