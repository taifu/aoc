import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        setattr(day, 'solution', None)
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
        self.data_example_2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

    def test_example_1(self) -> None:
        day.solve1("Register A: 0\nRegister B: 0\nRegister C: 9\n\nProgram: 2,6")
        self.assertEqual(day.solution.registers[1], 1)

    def test_example_2(self) -> None:
        day.solve1("Register A: 10\nRegister B: 0\nRegister C: 0\n\nProgram: 5,0,5,1,5,4")
        self.assertEqual(day.solution.output, [0, 1, 2])

    def test_example_3(self) -> None:
        day.solve1("Register A: 2024\nRegister B: 0\nRegister C: 0\n\nProgram: 0,1,5,4,3,0")
        self.assertEqual(day.solution.registers[0], 0)
        self.assertEqual(day.solution.output, [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0])

    def test_example_4(self) -> None:
        day.solve1("Register A: 0\nRegister B: 29\nRegister C: 0\n\nProgram: 1,7")
        self.assertEqual(day.solution.registers[1], 26)

    def test_example_5(self) -> None:
        day.solve1("Register A: 0\nRegister B: 2024\nRegister C: 43690\n\nProgram: 4,0")
        self.assertEqual(day.solution.registers[1], 44354)

    def test_part_1(self) -> None:
        self.assertEqual(day.solve1(self.data_example), "4,6,3,5,6,3,5,2,1,0")

    def test_solutions_1(self) -> None:
        self.assertEqual(day.solve1(self.data), "3,5,0,1,5,1,5,1,0")

    def test_solutions_2(self) -> None:
        self.assertEqual(day.solve2(self.data), 107413700225434)
