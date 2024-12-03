import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
        self.data_example2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

    def test_part_1(self) -> None:
        self.assertEqual(161, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(48, day.solve2(self.data_example2))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 159833790)
        self.assertEqual(day.solve2(self.data), 89349241)
