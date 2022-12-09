import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

        self.data_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

    def test_part_1(self):
        self.assertEqual(13, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(36, day.solve2(self.data_2))

    def test_solution(self):
        import os
        with open(os.path.dirname(__file__) + "/input.txt") as f_data:
            data = f_data.read()
            self.assertEqual(day.solve1(data), 6067)
            self.assertEqual(day.solve2(data), 2471)
