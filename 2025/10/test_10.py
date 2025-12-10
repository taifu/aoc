import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

    def test_part_1(self) -> None:
        self.assertEqual(7, day.solve1(self.data_example))

    def _test_part_2(self) -> None:
        self.assertEqual(24, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 502)
        # self.assertEqual(day.solve2(self.data), 1560475800)
