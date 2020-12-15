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
        self.solve2 = (175594, 2578)

    def test_part_1(self):
        for data, sol in zip(self.data, self.solve1):
            self.assertEqual(day.solve(data), sol)

    # Ok but slow!
    # def test_part_2(self):
    #     for data, sol in zip(self.data, self.solve2):
    #         self.assertEqual(day.solve(data, 30000000), sol)
