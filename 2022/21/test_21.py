import os
import pytest
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.real_data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.real_data_val = open(os.path.dirname(__file__) + "/input-val.txt").read()
        self.data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

    def test_part_1(self):
        self.assertEqual(152, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(301, day.solve2(self.data))

    def test_solution_part_val_2(self):
        self.assertEqual(3712643961892, day.solve2(self.real_data_val))

    def test_solution_part_1(self):
        self.assertEqual(158661812617812, day.solve1(self.real_data))

    def test_solution_part_2(self):
        self.assertEqual(3352886133831, day.solve2(self.real_data))
