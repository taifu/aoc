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
        self.assertEqual(day.solve1(self.data, 5), 127)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data, 127), 62)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        part1 = day.solve1(data, 25)
        self.assertEqual(part1, 133015568)
        self.assertEqual(day.solve2(data, part1), 16107959)
