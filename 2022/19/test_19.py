import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.
"""

    def test_part_1(self):
        self.assertEqual(33, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(56, day.Blueprint(day.load(self.data)[0]).best(32))
        self.assertEqual(62, day.Blueprint(day.load(self.data)[1]).best(32))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(1150, day.solve1(data))
        self.assertEqual(37367, day.solve2(data))
