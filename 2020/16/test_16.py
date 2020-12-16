import unittest

import day_16 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""
        self.data2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""

    def test_parse1(self):
        data = self.data1
        rules, your_ticket, nearby_tickets = day.parse(data)
        self.assertEqual(rules, {'class': [1, 3, 5, 7], 'row': [6, 11, 33, 44], 'seat': [13, 40, 45, 50]})
        self.assertEqual(your_ticket, [7, 1, 14])
        self.assertEqual(nearby_tickets, [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]])

    def test_parse2(self):
        data = self.data2
        rules, your_ticket, nearby_tickets = day.parse(data)
        self.assertEqual(rules, {'class': [0, 1, 4, 19], 'row': [0, 5, 8, 19], 'seat': [0, 13, 16, 19]})
        self.assertEqual(your_ticket, [11, 12, 13])
        self.assertEqual(nearby_tickets, [[3, 9, 18], [15, 1, 5], [5, 14, 9]])

    def test_part_1(self):
        data = self.data1
        self.assertEqual(day.solve(data, second_part=False)[0], 71)

    def test_part_2(self):
        data = self.data2
        self.assertEqual(day.solve(data)[2], {'row': 0, 'class': 1, 'seat': 2})
        _, _, p3 = day.solve(data)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        part1, part2, _ = day.solve(data)
        self.assertEqual(part1, 23054)
        self.assertEqual(part2, 51240700105297)
