import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

    def test_part_1(self) -> None:
        self.assertEqual(12, day.solve1(self.data_example, 11, 7))

    def test_part_2(self) -> None:
        pass

    def test_solution(self) -> None:
        self.assertEqual(day.solve1(self.data), 216772608)

    def test_solution_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 6888)
