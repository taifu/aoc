import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        setattr(day, 'solution', None)
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

    def test_part_1(self) -> None:
        self.assertEqual(day.solve1(self.data_example), 6)

    def test_part_2(self) -> None:
        self.assertEqual(day.solve2(self.data_example), 16)

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 347)

    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 919219286602165)
