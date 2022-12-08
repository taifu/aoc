import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """30373
25512
65332
33549
35390"""

    def test_part_1(self):
        self.assertEqual(21, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(8, day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 1827)
        self.assertEqual(day.solve2(data), 335580)
