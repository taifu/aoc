from itertools import permutations
from collections import deque


class Map:
    def pos_to_xy(self, vertex):
        pos = self.raw.find(vertex)
        return pos % (self.width + 1), pos // (self.width + 1)

    def __init__(self, raw):
        self.raw = raw
        self.map = [list(row.strip()) for row in raw.split("\n")]
        self.width = len(self.map[0])
        self.keys = set(c for c in raw if c.islower())
        self.vertices = ['@'] + list(self.keys)
        self.edges = {}
        for n, vertex1 in enumerate(self.vertices[:-1]):
            for vertex2 in self.vertices[n + 1:]:
                shortest, doors, keys = self.path(vertex1, vertex2)
                self.edges[(vertex1, vertex2)] = shortest, set(doors), set(keys)
                self.edges[(vertex2, vertex1)] = shortest, set(doors), set(keys)

    def path(self, vertex1, vertex2):
        vertex1_position = self.pos_to_xy(vertex1)
        queue = deque([(vertex1_position, 0, [], [])])
        visited = set()
        shortest = None
        while queue:
            position, length, doors, keys = queue.popleft()
            visited.add(position)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_position = position[0] + dx, position[1] + dy
                if next_position not in visited:
                    next_cell = self.map[next_position[1]][next_position[0]]
                    if next_cell == vertex2:
                        if shortest is None or length + 1 < shortest[0]:
                            shortest = length + 1, doors, keys
                    elif next_cell != '#':
                        queue.append((next_position, length + 1,
                                      doors + ([] if not next_cell.isupper() else [next_cell.lower()]),
                                      keys + ([] if not next_cell.islower() else [next_cell])))
        return shortest

    def explore(self, vertex, keys, length=0):
        if length > self.bests.get(keys, length + 1):
            return
        self.bests[keys] = length
        keys_set = set(keys)
        for next_vertex in self.keys - keys_set:
            next_length, next_doors, next_keys = self.edges[vertex, next_vertex]
            if next_doors <= keys_set.union(next_keys):
                self.explore(next_vertex, tuple(sorted(keys_set.union(next_keys).union(set([next_vertex])))), length + next_length)

    def steps(self):
        self.bests = {}
        self.explore('@', ())
        return self.bests[tuple(sorted(self.keys))]


def test_p18_1():
    assert Map("""#########
#b.A.@.a#
#########""").steps() == 8


def test_p18_2():
    assert Map("""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""").steps() == 86


def test_p18_3():
    assert Map("""########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""").steps() == 132


def test_p18_4():
    assert Map("""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""").steps() == 136


def test_p18_5():
    assert Map("""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""").steps() == 81


if __name__ == "__main__":
    print(Map(open("input.txt").read()).steps())
