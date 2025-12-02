import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""

    def test_part_1(self) -> None:
        self.assertEqual(1227775554, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(4174379265, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 43952536386)
        self.assertEqual(day.solve2(self.data), 54486209192)
