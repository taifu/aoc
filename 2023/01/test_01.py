import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
        self.data_2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    def test_part_1(self):
        self.assertEqual(142, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(281, day.solve2(self.data_2))

    def test_part_special(self):
        self.assertEqual(18, day.solve2("oneight"))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 56397)
        self.assertEqual(day.solve2(data), 55701)
