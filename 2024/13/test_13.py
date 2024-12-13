import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

    def test_part_1(self) -> None:
        self.assertEqual(480, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(875318608908, day.solve2(self.data_example))
        pass

    def test_solution(self) -> None:
        self.assertEqual(day.solve1(self.data), 35082)

    def test_solution_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 82570698600470)
