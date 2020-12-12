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
        acc, res = day.solve(self.data)
        self.assertEqual(res, False)
        self.assertEqual(acc, 5)

    def test_part_2(self):
        acc = day.solve2(self.data)
        self.assertEqual(acc, 8)
