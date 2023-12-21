import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = open(os.path.dirname(__file__) + "/example.txt").read()

    def test_part_1(self) -> None:
        self.assertEqual(16, day.solve1(self.data_example, 6))

    def test_solution_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 3697)

    def test_solution_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 608152828731262)
