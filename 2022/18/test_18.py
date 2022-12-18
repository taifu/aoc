import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

    def test_part_1(self):
        self.assertEqual(64, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(58, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(4400, day.solve1(data))
        self.assertEqual(2522, day.solve2(data))
