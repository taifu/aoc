import unittest

import day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """abc

a
b
c

ab
ac

a
a
a
a

b
"""

    def test_part_1(self):
        self.assertEqual(11, day.part1(self.data)[0])

    def test_part_2(self):
        self.assertEqual(6, day.part1(self.data)[1])
