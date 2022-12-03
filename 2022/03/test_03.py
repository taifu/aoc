import unittest

import day_03 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

    def test_part_1(self):
        self.assertEqual(157, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(70, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 7746)
        self.assertEqual(day.solve2(data), 2604)
