import unittest
day = __import__('day_' + __file__[-5:-3])


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

    def test_part_1(self):
        self.assertEqual(10605, day.solve1(self.data))

    def test_part_2(self):
        self.assertEqual(2713310158, day.solve2(self.data))

    def test_solution(self):
        import os
        with open(os.path.dirname(__file__) + "/input.txt") as f_data:
            data = f_data.read()
            self.assertEqual(day.solve1(data), 90294)
            self.assertEqual(day.solve2(data), 18170818354)
