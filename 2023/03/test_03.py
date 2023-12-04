import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

    def test_part_1(self) -> None:
        self.assertEqual(4361, day.solve1(self.data))

    def test_part_2(self) -> None:
        self.assertEqual(467835, day.solve2(self.data))

    def test_solution(self) -> None:
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), 544664)
        self.assertEqual(day.solve2(data), 84495585)
