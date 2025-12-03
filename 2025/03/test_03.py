import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """987654321111111
811111111111119
234234234234278
818181911112111
"""

    def test_part_1(self) -> None:
        self.assertEqual(357, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(3121910778619, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 17445)
        self.assertEqual(day.solve2(self.data), 173229689350551)
