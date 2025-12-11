import os
import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self) -> None:
        self.data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.data_example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
        self.data_example_2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

    def test_part_1(self) -> None:
        self.assertEqual(5, day.solve1(self.data_example))

    def test_part_2(self) -> None:
        self.assertEqual(2, day.solve2(self.data_example_2))

    def test_solutions(self) -> None:
        self.assertEqual(day.solve1(self.data), 590)
        self.assertEqual(day.solve2(self.data), 319473830844560)
