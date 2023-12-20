import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = open(os.path.dirname(__file__) + "/example.txt").read()
        self.data_example_2 = open(os.path.dirname(__file__) + "/example2.txt").read()

    def test_part_1(self) -> None:
        self.assertEqual(32000000, day.solve1(self.data_example))

    def test_part_1_2(self) -> None:
        self.assertEqual(11687500, day.solve1(self.data_example_2))

    def test_solution_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 817896682)

    def test_solution_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 250924073918341)
