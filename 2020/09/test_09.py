import unittest

import day_09 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""

    def test_part_1(self):
        res = day.solve(self.data, 5)
        self.assertEqual(res, 127)

    def test_part_2(self):
        res = day.solve2(self.data, 127)
        self.assertEqual(res, 62)
