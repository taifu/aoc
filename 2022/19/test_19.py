import os
import pytest
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.real_data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data = """Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.
"""
        self.data_2 = """Blueprint 17: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 2 ore and 7 clay. Each geode robot costs 3 ore and 8 obsidian.
Blueprint 21: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 4 ore and 6 clay. Each geode robot costs 3 ore and 11 obsidian.
Blueprint 27: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 10 clay. Each geode robot costs 3 ore and 10 obsidian.
Blueprint 30: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 11 clay. Each geode robot costs 4 ore and 8 obsidian.
"""

    def test_part_1(self):
        self.assertEqual(33, day.solve1(self.data))

    def test_part_test_euristic(self):
        self.assertEqual(11, day.Blueprint(day.load(self.data_2)[0]).best(24))
        self.assertEqual(7, day.Blueprint(day.load(self.data_2)[1]).best(24))
        self.assertEqual(5, day.Blueprint(day.load(self.data_2)[2]).best(24))
        self.assertEqual(3, day.Blueprint(day.load(self.data_2)[3]).best(24))

    @pytest.mark.slow
    def test_part_2(self):
        # 56 * 62 = 3472
        self.assertEqual(56, day.Blueprint(day.load(self.data)[0]).best(32))
        self.assertEqual(62, day.Blueprint(day.load(self.data)[1]).best(32))

    @pytest.mark.slow
    def test_solution_part_1(self):
        self.assertEqual(1150, day.solve1(self.real_data))

    @pytest.mark.slow
    def test_solution_part_2(self):
        self.assertEqual(37367, day.solve2(self.real_data))
