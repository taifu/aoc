import unittest
from operator import add, mul

import day_19 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data1 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""
        self.data2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""

    def test_parse(self):
        rules, messages = day.parse(self.data1)
        self.assertEqual(rules, {0: [[4, 1, 5]], 1: [[2, 3], [3, 2]], 2: [[4, 4], [5, 5]], 3: [[4, 5], [5, 4]], 4: 'a', 5: 'b'})
        self.assertEqual(messages, ['ababbb', 'bababa', 'abbbab', 'aaabbb', 'aaaabbb'])

    def test_find_root_1(self):
        rules, messages = day.parse(self.data1)
        self.assertEqual(day.find_root(rules), 0)

    def test_find_root_2(self):
        rules, messages = day.parse(self.data2)
        self.assertEqual(day.find_root(rules), 0)

    def test_solve1(self):
        self.assertEqual(day.solve(self.data1), 2)

    def test_solve2_1(self):
        self.assertEqual(day.solve(self.data2), 3)

    def test_solve2_2(self):
        self.assertEqual(day.solve(self.data2, substitute={8: [[42], [42, 8]], 11: [[42, 31], [42, 11, 31]]}), 12)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve(data), 102)
        self.assertEqual(day.solve(data, substitute={8: [[42], [42, 8]], 11: [[42, 31], [42, 11, 31]]}), 318)
