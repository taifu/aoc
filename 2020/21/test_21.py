import unittest

import day_21 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""

    def test_part1(self):
        self.assertEqual(day.solve(self.data), 5)

    def test_part2(self):
        self.assertEqual(day.solve(self.data, step=2), 'mxmxvkd,sqjhc,fvjkl')

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve(data), 2302)
        self.assertEqual(day.solve(data, step=2), 'smfz,vhkj,qzlmr,tvdvzd,lcb,lrqqqsg,dfzqlk,shp')
