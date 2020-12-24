import unittest
import pytest

import day_24 as day


class TestDay(unittest.TestCase):
    def setUp(self):
        self.data = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""

    def test_parse_line(self):
        self.assertEqual(list(day.parse_line("nwwswee")), [(-1, 0, 1), (-1, 1, 0), (0, 1, -1), (1, -1, 0), (1, -1, 0)])

    def test_parse_move(self):
        self.assertEqual(day.move((1, 1, 1), day.parse_line("nwwswee")), (1, 1, 1))

    def test_part1(self):
        self.assertEqual(len(day.solve1(self.data)), 10)

    def test_part2(self):
        self.assertEqual(day.solve2(day.solve1(self.data)), 2208)

    def test_solution(self):
        import os
        data = open(os.path.dirname(__file__) + "/input.txt").read()
        blacks = day.solve1(data)
        self.assertEqual(len(blacks), 317)
        self.assertEqual(day.solve2(blacks), 3804)
