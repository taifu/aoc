import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

    def test_part_1(self) -> None:
        self.assertEqual(40, day.solve1(self.data_example, 10))

    def test_part_2(self) -> None:
        self.assertEqual(25272, day.solve2(self.data_example))

    def test_solutions(self) -> None:
        day.playground = None
        self.assertEqual(day.solve1(self.data), 123234)
        self.assertEqual(day.solve2(self.data), 9259958565)
