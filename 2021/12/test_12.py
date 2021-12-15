import unittest
import pytest

import day_12 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data_1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
        self.data_2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
        self.data_3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

    def test_part_1_1(self):
        self.assertEqual(10, day.solve1(self.data_1))

    def test_part_1_2(self):
        self.assertEqual(19, day.solve1(self.data_2))

    def test_part_1_3(self):
        self.assertEqual(226, day.solve1(self.data_3))

    def test_part_2_1(self):
        self.assertEqual(36, day.solve2(self.data_1))

    def test_part_2_2(self):
        self.assertEqual(103, day.solve2(self.data_2))

    def test_part_2_3(self):
        self.assertEqual(3509, day.solve2(self.data_3))

    @pytest.mark.slow
    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 4186)
        self.assertEqual(day.solve2(data), 92111)
