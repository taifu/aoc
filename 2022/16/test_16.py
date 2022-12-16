import unittest
import pytest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

    def test_part_1(self):
        self.assertEqual(1651, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(1707, day.solve2(self.data))

    def test_solution(self):
        import os
        with open(os.path.dirname(__file__) + "/input.txt") as f_data:
            data = f_data.read()
            self.assertEqual(day.solve1(data), 1789)
            #self.assertEqual(day.solve2(data), 12691026767556)
