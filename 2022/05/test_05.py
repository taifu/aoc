import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


    def test_part_1(self):
        self.assertEqual("CMZ", day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual("MCD", day.solve2(self.data))

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        self.assertEqual(day.solve1(data), "ZWHVFWQWW")
        self.assertEqual(day.solve2(data), "HZFZCCWWV")
