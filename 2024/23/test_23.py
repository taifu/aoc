import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        day.Solution._instance = None
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

    def test_part_1(self) -> None:
        self.assertEqual(day.solve1(self.data_example), 7)

    def test_part_2(self) -> None:
        self.assertEqual(day.solve2(self.data_example), 'co,de,ka,ta')

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 1419)

    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), "af,aq,ck,ee,fb,it,kg,of,ol,rt,sc,vk,zh")
