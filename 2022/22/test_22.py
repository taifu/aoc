import os
import pytest
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.real_data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
        grid, _ = day.load(self.real_data.replace(day.WALL, day.OPEN))
        self.board = day.Board(grid, cube=True)
        self.width = self.board.width

    def check_wrap(self, current, turns=0, steps=1):
        self.board.current = current
        for n in range(turns):
            self.board.move(day.TURN_LEFT)
        self.board.move(steps)
        return self.board.direction, self.board.current

    def test_part_1(self):
        self.assertEqual(6032, day.solve1(self.data))

    def test_part_cube_wrap_1_6(self):
        self.assertEqual((1, 1j * (3 * self.width)), self.check_wrap(self.width, turns=1))

    def test_part_cube_wrap_1_4(self):
        self.assertEqual((1, 1j * (3 * self.width - 1)), self.check_wrap(self.width, turns=2))

    def test_part_cube_wrap_2_5(self):
        self.assertEqual((-1, 2 * self.width - 1 + 1j * (self.width * 3 - 1)), self.check_wrap(self.width * 3 - 1))

    def test_part_cube_wrap_2_6(self):
        self.assertEqual((-1j, 1j * (4 * self.width - 1)), self.check_wrap(self.width * 2, turns=1))

    def test_part_cube_wrap_2_3(self):
        self.assertEqual((-1, self.width * 2 - 1 + 1j * self.width), self.check_wrap(self.width * 2 + 1j * (self.width - 1), turns=3))

    def test_part_cube_wrap_3_4(self):
        self.assertEqual((1j, 1j * (2 * self.width)), self.check_wrap(self.width + 1j * self.width, turns=2))

    def test_part_cube_wrap_3_2(self):
        self.assertEqual((-1j, self.width * 2 + 1j * (self.width - 1)), self.check_wrap(self.width * 2 - 1 + 1j * self.width))

    def test_part_cube_wrap_4_3(self):
        self.assertEqual((1, self.width + 1j * self.width), self.check_wrap(1j * (self.width * 2), turns=1))

    def test_part_cube_wrap_4_1(self):
        self.assertEqual((1, self.width), self.check_wrap(1j * (self.width * 3 - 1), turns=2))

    def test_part_cube_wrap_5_2(self):
        self.assertEqual((-1, self.width * 3 - 1 + 1j * (self.width - 1)), self.check_wrap(self.width * 2 - 1 + 1j * (self.width * 2)))

    def test_part_cube_wrap_5_6(self):
        self.assertEqual((-1, self.width - 1 + 1j * (self.width * 4 - 1)), self.check_wrap(self.width * 2 - 1 + 1j * (self.width * 3 - 1), turns=3))

    def test_part_cube_wrap_6_1(self):
        self.assertEqual((1j, self.width), self.check_wrap(1j * (self.width * 3), turns=2))

    def test_part_cube_wrap_6_2(self):
        self.assertEqual((1j, self.width * 2), self.check_wrap(1j * (self.width * 4 - 1), turns=3))

    def test_part_cube_wrap_6_5(self):
        self.assertEqual((-1j, self.width + 1j * (self.width * 3 - 1)), self.check_wrap(self.width - 1 + 1j * self.width * 3))

    def test_solution_part_1(self):
        self.assertEqual(36518, day.solve1(self.real_data))

    def test_solution_part_2(self):
        self.assertEqual(143208, day.solve2(self.real_data))
