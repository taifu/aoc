from collections import deque


class Vertex:
    def __init__(self, char, x_y):
        self.char = char
        self.position = x_y
        self.x = x_y[0]
        self.y = x_y[1]


class Map:
    def pos_to_xy(self, vertex):
        return self.index_to_xy(self.raw.find(vertex))

    def index_to_xy(self, index):
        return index % (self.width + 1), index // (self.width + 1)

    def show(self):
        for row in self.map:
            print("".join(row))

    def __init__(self, raw):
        self.raw = raw
        self.map = [list(row.strip()) for row in raw.split("\n")]
        self.width = len(self.map[0])
        self.keys = frozenset(c for c in raw if c.islower())
        self.robots = [Vertex(str(n), self.index_to_xy(n)) for n, c in enumerate(self.raw) if c == '@']
        self.robots_keys = dict((robot.char, frozenset()) for robot in self.robots)
        self.vertices = dict((c, Vertex(c, self.pos_to_xy(c))) for c in self.keys)
        self.all = self.robots + list(self.vertices.values())
        self.edges = {}
        for n, vertex1 in enumerate(self.all[:-1]):
            for vertex2 in self.all[n + 1:]:
                found = self.path(vertex1, vertex2)
                if found is not None:
                    if vertex1.char in self.robots_keys:
                        self.robots_keys[vertex1.char] = self.robots_keys[vertex1.char].union([vertex2.char])
                    shortest, doors, keys = found
                    self.edges[(vertex1.char, vertex2.char)] = shortest, frozenset(doors), frozenset(keys)
                    self.edges[(vertex2.char, vertex1.char)] = shortest, frozenset(doors), frozenset(keys)

    def path(self, vertex1, vertex2):
        queue = deque([(vertex1.position, 0, [], [])])
        visited = set()
        shortest = None
        while queue:
            position, length, doors, keys = queue.popleft()
            visited.add(position)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_position = position[0] + dx, position[1] + dy
                if next_position not in visited:
                    next_cell = self.map[next_position[1]][next_position[0]]
                    if next_cell == vertex2.char:
                        if shortest is None or length + 1 < shortest[0]:
                            shortest = length + 1, doors, keys
                    elif next_cell != '#':
                        queue.append((next_position, length + 1,
                                      doors + ([] if not next_cell.isupper() else [next_cell.lower()]),
                                      keys + ([] if not next_cell.islower() else [next_cell])))
        return shortest

    def explore_recursive(self, vertex, keys, length=0):
        if length > self.bests.get(keys, length + 1):
            return
        self.bests[keys] = length
        for next_vertex_key in self.keys - keys:
            next_vertex = self.vertices[next_vertex_key]
            next_length, next_doors, next_keys = self.edges[vertex.char, next_vertex.char]
            if next_doors <= keys.union(next_keys):
                self.explore_recursive(next_vertex, keys.union(next_keys).union([next_vertex_key]), length + next_length)

    def reduce_frozensets(self, fsets):
        all_fset = frozenset()
        for f in fsets:
            all_fset = all_fset.union(f)
        return all_fset

    def explore(self):
        self.bests = {}
        queue = deque(((0, self.robots, frozenset()),))
        while queue:
            length, vertices, all_keys = queue.popleft()
            if length > self.bests.get(all_keys, length + 1):
                continue
            self.bests[all_keys] = length
            for n, robot in enumerate(self.robots):
                for next_vertex_key in self.robots_keys[robot.char] - all_keys:
                    next_vertex = self.vertices[next_vertex_key]
                    next_length, doors, next_keys = self.edges[vertices[n].char, next_vertex.char]
                    if doors <= all_keys.union(next_keys):
                        queue.append((length + next_length,
                                      vertices[:n] + [next_vertex] + vertices[n + 1:],
                                      all_keys.union(next_keys).union(next_vertex_key)))

    def steps_recursive(self):
        # Recursive
        self.bests = {}
        self.explore_recursive(self.robots[0], frozenset())
        return self.bests[self.keys]

    def steps(self):
        self.explore()
        return self.bests[self.keys]


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


def test_p18_6():
    assert Map("""#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#.b#
#######""").steps() == 8


def test_p18_7():
    assert Map("""###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############""").steps() == 24


def test_p18_8():
    assert Map("""#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############""").steps() == 32


if __name__ == "__main__":
    raw = open("input.txt").read()
    map1 = Map(raw)
    map1.show()
    print(map1.steps())
    pos = raw.find('@')
    raw = raw[:pos - 1] + '###' + raw[pos + 2:]
    len_row = len(map1.map[0])
    for delta in (-len_row - 1, len_row + 1):
        raw = raw[:pos + delta - 1] + '@#@' + raw[pos + delta + 2:]
    map2 = Map(raw)
    map2.show()
    print(map2.steps())
