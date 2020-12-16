import unittest

import day_07 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
        self.data2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

    def test_part_1(self):
        self.assertEqual(4, day.solve(self.data)[0])

    def test_part_2_1(self):
        self.assertEqual(32, day.solve(self.data)[1])

    def test_part_2_2(self):
        self.assertEqual(126, day.solve(self.data2)[1])

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        part1, part2 = day.solve(data)
        self.assertEqual(part1, 103)
        self.assertEqual(part2, 1469)
