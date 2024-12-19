import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        setattr(day, 'solution', None)
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

    def test_part_1(self) -> None:
        self.assertEqual(day.solve1(self.data_example, 12, 6), 22)

    def test_part_2(self) -> None:
        self.assertEqual(day.solve2(self.data_example, 6), '6,1')

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), 322)

    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), "60,21")
