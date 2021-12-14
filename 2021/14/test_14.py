import unittest

import day_14 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

    def test_part_1(self):
        self.assertEqual(1588, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(2188189693529, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 2233)
        self.assertEqual(day.solve2(data), 2884513602164)
