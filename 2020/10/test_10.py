import unittest

import day_10 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """16
10
15
5
1
11
7
19
6
12
4
"""
        self.data_larger = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""

    def test_part_1(self):
        differences = day.solve1(self.data)
        self.assertEqual(differences[1], 7)
        self.assertEqual(differences[3], 5)

    def test_part_1_larger(self):
        differences = day.solve1(self.data_larger)
        self.assertEqual(differences[1], 22)
        self.assertEqual(differences[3], 10)

    def test_part_2(self):
        self.assertEqual(day.solve2(self.data), 8)

    def test_part_2_larger(self):
        self.assertEqual(day.solve2(self.data_larger), 19208)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        differences = day.solve1(data)
        self.assertEqual(differences[1] * differences[3], 2664)
        self.assertEqual(day.solve2(data), 148098383347712)
