import unittest

import day_05 as day


class TestDay(unittest.TestCase):
    def test_row_col_1(self):
        line = """BFFFBBFRRR"""
        row, col = 70, 7
        self.assertEqual((row, col), day.row_col(line))

    def test_id_1(self):
        row, col = 70, 7
        self.assertEqual(567, day.calc_id(row, col))

    def test_row_col_2(self):
        line = """FFFBBBFRRR"""
        row, col = 14, 7
        self.assertEqual((row, col), day.row_col(line))

    def test_row_id_2(self):
        row, col = 14, 7
        self.assertEqual(119, day.calc_id(row, col))

    def test_row_col_3(self):
        line = """BBFFBBFRLL"""
        row, col = 102, 4
        self.assertEqual((row, col), day.row_col(line))

    def test_row_id_3(self):
        row, col = 102, 4
        self.assertEqual(820, day.calc_id(row, col))
