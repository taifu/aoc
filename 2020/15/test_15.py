import unittest

import day_15 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = ("0,3,6",
                     "1,3,2",
                     "2,1,3",
                     "1,2,3",
                     "2,3,1",
                     "3,2,1",
                     "3,1,2")
        self.solve1 = (436, 1, 10, 27, 78, 438, 1836)
        self.solve2 = (175594, 2578, 3544142, 261214, 175594, 18, 362)
        self.solve2_30000 = (7717, 13, 5124, 0, 42, 22, 10)

    def test_part_1(self):
        for data, sol in zip(self.data, self.solve1):
            self.assertEqual(day.solve(data), sol)

    def test_part_2(self):
        for data, sol, sol_quick in zip(self.data, self.solve2, self.solve2_30000):
            # Ok but slow!
            # self.assertEqual(day.solve(data, 30000000), sol)
            self.assertEqual(day.solve(data, 30000), sol_quick)

    def test_solution(self):
        data = "0,13,1,8,6,15"
        self.assertEqual(day.solve(data), 1618)
        # Ok but slow!
        # self.assertEqual(day.solve(data, n=30000000), 548531)
        self.assertEqual(day.solve(data, n=100000), 336)
