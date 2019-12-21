from collections import deque


INFINITY = float('inf')
DELTA = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Edge:
    def __init__(self, start, end, cost):
        self.start = start
        self.end = end
        self.cost = cost

    def __repr__(self):
        return "Edge {}-{} [{}]".format(self.start, self.end, self.cost)


class Maze:
    def __init__(self, raw, part=1):
        self.rows = [row for row in raw.split("\n") if row.strip()]
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.part = part
        self.interpret()

    def get(self, x, y):
        if self.width > x >= 0 and self.height > y >= 0:
            return self.rows[y][x]
        return ''

    def breadth_first_search(self, start, goal):
        queue = deque([[start]])
        all_paths = {}
        goal_path = None
        while queue:
            path = queue.popleft()
            pos = path[-1]
            if pos not in all_paths:
                for dx, dy in DELTA:
                    next_pos = (pos[0] + dx, pos[1] + dy)
                    if next_pos in all_paths:
                        continue
                    cell = self.get(*next_pos)
                    if cell == '.':
                        new_path = path + [next_pos]
                        if next_pos == goal:
                            goal_path = new_path
                            break
                        queue.append(new_path)
                all_paths[pos] = path
        return goal_path

    def outside(self, x, y):
        return x in (2, self.width - 3) or y in (2, self.height - 3)

    def interpret(self):
        self.edges = {}
        self.vertex_aa = None
        self.vertex_zz = None
        self.vertices_out = {}
        self.vertices_in = {}
        for y, row in enumerate(self.rows):
            for x, c in enumerate(row):
                if c.isalpha():
                    name = None
                    for dx, dy in DELTA:
                        c2 = self.get(x + dx, y + dy)
                        if c2.isalpha() and (dx > 0 or dy > 0):
                            name = c + c2
                            pos_name = (x + dx, y + dy)
                    if name:
                        if pos_name[1] == y:
                            yps = [y]
                            xps = [min(pos_name[0], x) - 1, max(pos_name[0], x) + 1]
                        else:
                            yps = [min(pos_name[1], y) - 1, max(pos_name[1], y) + 1]
                            xps = [x]
                        for yp in yps:
                            for xp in xps:
                                p = self.get(xp, yp)
                                if p == '.':
                                    if name in 'AA':
                                        self.vertex_aa = {name: (xp, yp)}
                                    elif name == 'ZZ':
                                        self.vertex_zz = {name: (xp, yp)}
                                    else:
                                        if self.outside(xp, yp):
                                            which_vertices = self.vertices_out
                                        else:
                                            name += "0"
                                            which_vertices = self.vertices_in
                                        if name not in which_vertices:
                                            which_vertices[name] = (xp, yp)
        from_vertices = list(self.vertices_in.items()) + list(self.vertices_out.items()) + list(self.vertex_aa.items()) + list(self.vertex_zz.items())
        for v1, pos1 in from_vertices:
            for v2, pos2 in from_vertices:
                if v1 != v2:
                    cost = self.breadth_first_search(pos1, pos2)
                    if cost:
                        self.edges[v1, v2] = Edge(v1, v2, len(cost) - 1)
                        self.edges[v2, v1] = Edge(v2, v1, len(cost) - 1)
        for v1, pos1 in self.vertices_out.items():
            v2 = v1 + "0"
            pos2 = self.vertices_in.get(v2, None)
            if pos2:
                self.edges[v1, v2] = Edge(v1, v2, 1)
                self.edges[v2, v1] = Edge(v2, v1, 1)
        if self.part == 2:
            new_edges = {}
            for level in range(40):
                for v1 in self.vertices_in.keys():
                    v1i = v1[:2] + 'i' + str(level)
                    v2o = v1[:2] + 'o' + str(level + 1)
                    new_edges[v1i, v2o] = Edge(v1i, v2o, 1)
                    new_edges[v2o, v1i] = Edge(v2o, v1i, 1)
                    for v2 in self.vertices_in.keys():
                        if v1[:2] != v2[:2]:
                            edge = self.edges.get((v1, v2), None)
                            if edge:
                                v1i = v1[:2] + 'i' + str(level)
                                v2i = v2[:2] + 'i' + str(level)
                                new_edges[v1i, v2i] = Edge(v1i, v2i, edge.cost)
                                new_edges[v2i, v1i] = Edge(v2i, v1i, edge.cost)
                if level > 0:
                    for v1 in self.vertices_out.keys():
                        for v2 in self.vertices_out.keys():
                            if v1[:2] != v2[:2]:
                                edge = self.edges.get((v1, v2), None)
                                if edge:
                                    v1o = v1[:2] + 'o' + str(level)
                                    v2o = v2[:2] + 'o' + str(level)
                                    new_edges[v1o, v2o] = Edge(v1o, v2o, edge.cost)
                                    new_edges[v2o, v1o] = Edge(v2o, v1o, edge.cost)
                        for v2 in self.vertices_in.keys():
                            if v1[:2] != v2[:2]:
                                edge = self.edges.get((v1, v2), None)
                                if edge:
                                    v1o = v1[:2] + 'o' + str(level)
                                    v2i = v2[:2] + 'i' + str(level)
                                    new_edges[v1o, v2i] = Edge(v1o, v2i, edge.cost)
                                    new_edges[v2i, v1o] = Edge(v2i, v1o, edge.cost)
                else:
                    for v1 in ('AA', 'ZZ'):
                        for v2 in self.vertices_in.keys():
                            if v1 != v2:
                                edge = self.edges.get((v1, v2), None)
                                if edge:
                                    v2i = v2[:2] + 'i0'
                                    if v1 == 'AA':
                                        new_edges[v1, v2i] = Edge(v1, v2i, edge.cost)
                                    else:
                                        new_edges[v2i, v1] = Edge(v2i, v1, edge.cost)
            self.edges = new_edges

    def dijkstra(self, source, destination):
        vertices = {e.start for e in self.edges.values()} | {e.end for e in self.edges.values()}
        distances = {vertex: INFINITY for vertex in vertices}
        previous = {vertex: None for vertex in vertices}
        distances[source] = 0
        neighbours = {vertex: set() for vertex in vertices}
        for edge in self.edges.values():
            neighbours[edge.start].add((edge.end, edge.cost))

        while vertices:
            u = min(vertices, key=lambda vertex: distances[vertex])
            vertices.remove(u)
            if distances[u] == INFINITY or u == destination:
                break
            for v, cost in neighbours[u]:
                alt = distances[u] + cost
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u

        s, u = deque(), destination
        while previous[u]:
            s.appendleft(u)
            u = previous[u]
        s.appendleft(u)
        return distances.get(destination, INFINITY)


def test_1():
    raw = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """
    maze = Maze(raw)
    assert maze.dijkstra('AA', 'ZZ') == 23


def test_2():
    raw = """                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """
    maze = Maze(raw)
    assert maze.height == 37
    assert maze.width == 35
    assert maze.dijkstra('AA', 'ZZ') == 58


def test_3():
    raw = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """
    maze = Maze(raw, part=2)
    assert maze.edges['AA', 'XFi0'].cost == 16
    assert maze.edges['XFi0', 'XFo1'].cost == 1
    assert maze.edges['XFo1', 'CKi1'].cost == 10
    assert maze.edges['CKi1', 'CKo2'].cost == 1
    assert maze.edges['CKo2', 'ZHi2'].cost == 14
    assert maze.edges['ZHi2', 'ZHo3'].cost == 1
    assert maze.edges['ZHo3', 'WBi3'].cost == 10
    assert maze.edges['WBi3', 'WBo4'].cost == 1
    assert maze.edges['WBo4', 'ICi4'].cost == 10
    assert maze.edges['ICi4', 'ICo5'].cost == 1
    assert maze.edges['ICo5', 'RFi5'].cost == 10
    assert maze.edges['RFi5', 'RFo6'].cost == 1
    assert maze.edges['RFo6', 'NMi6'].cost == 8
    assert maze.edges['NMi6', 'NMo7'].cost == 1
    assert maze.edges['NMo7', 'LPi7'].cost == 12
    assert maze.edges['LPi7', 'LPo8'].cost == 1
    assert maze.edges['LPo8', 'FDi8'].cost == 24
    assert maze.edges['FDi8', 'FDo9'].cost == 1
    assert maze.edges['FDo9', 'XQi9'].cost == 8
    assert maze.edges['XQi9', 'XQo10'].cost == 1
    assert maze.edges['XQo10', 'WBo10'].cost == 4
    assert maze.edges['WBo10', 'WBi9'].cost == 1
    assert maze.edges['WBi9', 'ZHo9'].cost == 10
    assert maze.edges['ZHo9', 'ZHi8'].cost == 1
    assert maze.edges['ZHi8', 'CKo8'].cost == 14
    assert maze.edges['CKo8', 'CKi7'].cost == 1
    assert maze.edges['CKi7', 'XFo7'].cost == 10
    assert maze.edges['XFo7', 'XFi6'].cost == 1
    assert maze.edges['XFi6', 'OAo6'].cost == 14
    assert maze.edges['OAo6', 'OAi5'].cost == 1
    assert maze.edges['OAi5', 'CJo5'].cost == 8
    assert maze.edges['CJo5', 'CJi4'].cost == 1
    assert maze.edges['CJi4', 'REo4'].cost == 8
    assert maze.edges['REo4', 'REi3'].cost == 1
    assert maze.edges['REi3', 'ICi3'].cost == 4
    assert maze.edges['ICi3', 'ICo4'].cost == 1
    assert maze.edges['ICo4', 'RFi4'].cost == 10
    assert maze.edges['RFi4', 'RFo5'].cost == 1
    assert maze.edges['RFo5', 'NMi5'].cost == 8
    assert maze.edges['NMi5', 'NMo6'].cost == 1
    assert maze.edges['NMo6', 'LPi6'].cost == 12
    assert maze.edges['LPi6', 'LPo7'].cost == 1
    assert maze.edges['LPo7', 'FDi7'].cost == 24
    assert maze.edges['FDi7', 'FDo8'].cost == 1
    assert maze.edges['FDo8', 'XQi8'].cost == 8
    assert maze.edges['XQi8', 'XQo9'].cost == 1
    assert maze.edges['XQo9', 'WBo9'].cost == 4
    assert maze.edges['WBo9', 'WBi8'].cost == 1
    assert maze.edges['WBi8', 'ZHo8'].cost == 10
    assert maze.edges['ZHo8', 'ZHi7'].cost == 1
    assert maze.edges['ZHi7', 'CKo7'].cost == 14
    assert maze.edges['CKo7', 'CKi6'].cost == 1
    assert maze.edges['CKi6', 'XFo6'].cost == 10
    assert maze.edges['XFo6', 'XFi5'].cost == 1
    assert maze.edges['XFi5', 'OAo5'].cost == 14
    assert maze.edges['OAo5', 'OAi4'].cost == 1
    assert maze.edges['OAi4', 'CJo4'].cost == 8
    assert maze.edges['CJo4', 'CJi3'].cost == 1
    assert maze.edges['CJi3', 'REo3'].cost == 8
    assert maze.edges['REo3', 'REi2'].cost == 1
    assert maze.edges['REi2', 'XQo2'].cost == 14
    assert maze.edges['XQo2', 'XQi1'].cost == 1
    assert maze.edges['XQi1', 'FDo1'].cost == 8
    assert maze.edges['FDo1', 'FDi0'].cost == 1
    assert maze.edges['FDi0', 'ZZ'].cost == 18
    assert maze.dijkstra('AA', 'ZZ') == 396


if __name__ == "__main__":
    raw = open("input.txt").read()
    maze = Maze(raw)
    print(maze.dijkstra('AA', 'ZZ'))
    maze = Maze(raw, part=2)
    print(maze.dijkstra('AA', 'ZZ'))
