import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        day.Solution._instance = None
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """029A
980A
179A
456A
379A"""

    def test_part_1_A_1(self) -> None:
        self.assertEqual(day.solve1(self.data_example.split('\n')[0], 1), 28 * 29)

    def test_part_1_A_2(self) -> None:
        self.assertEqual(day.solve1(self.data_example.split('\n')[0], 2), 68 * 29)

    def test_part_1_B(self) -> None:
        self.assertEqual(day.solve1(self.data_example.split('\n')[1], 2), 60 * 980)

    def test_part_1(self) -> None:
        self.assertEqual(day.solve1(self.data_example), 126384)

    def test_part_1_huge(self) -> None:
        self.assertEqual(day.solve1(self.data, 100), 98342476296893145101199557260707491488174926)

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 162740)

    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 203640915832208)
