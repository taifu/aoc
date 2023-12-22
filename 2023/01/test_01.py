import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
        self.data_example_2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    def test_part_1(self) -> None:
        self.assertEqual(142, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(281, day.solve2(self.data_example_2))

    def test_part_special(self) -> None:
        self.assertEqual(18, day.solve2("oneight"))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 56397)
        self.assertEqual(day.solve2(self.data), 55701)
