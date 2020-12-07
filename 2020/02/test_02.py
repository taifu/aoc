import unittest

import day_02


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

    def test_part_1(self):
        self.assertEqual(2, day_02.solve(self.data)[0])

    def test_part_2(self):
        self.assertEqual(1, day_02.solve(self.data)[1])
