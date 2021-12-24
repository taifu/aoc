import unittest

import day_24 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data_1 = """inp x
mul x -1
"""

        self.data_2 = """inp z
inp x
mul z 3
eql z x
"""

    def test_part_1_1(self):
        self.assertEqual(day.ALU(self.data_1).run([10])['x'], -10)

    def test_part_1_2(self):
        self.assertEqual(day.ALU(self.data_2).run([10, 30])['z'], 1)
        self.assertEqual(day.ALU(self.data_2).run([10, 29])['z'], 0)
        self.assertEqual(day.ALU(self.data_2).run([10, 31])['z'], 0)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), "96299896449997")
        self.assertEqual(day.solve2(data), "31162141116841")
