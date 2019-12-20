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
            for level in range(15):
                for v1 in self.vertices_in.keys():
                    v1i = v1[:2] + 'i' + str(level)
                    v2o = v1[:2] + 'o' + str(level + 1)
                    new_edges[v1i, v2o] = Edge(v1i, v2o, 1)
                    new_edges[v2o, v1i] = Edge(v2o, v1i, 1)
                if level > 0:
                    for v1 in self.vertices_out.keys():
                        for v2 in self.vertices_in.keys():
                            if v1 != v2:
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

    """
Recurse into level 8 through LP (1 step)
Walk from LP to FD (24 steps)
Recurse into level 9 through FD (1 step)
Walk from FD to XQ (8 steps)
Recurse into level 10 through XQ (1 step)
Walk from XQ to WB (4 steps)
Return to level 9 through WB (1 step)
Walk from WB to ZH (10 steps)
Return to level 8 through ZH (1 step)
Walk from ZH to CK (14 steps)
Return to level 7 through CK (1 step)
Walk from CK to XF (10 steps)
Return to level 6 through XF (1 step)
Walk from XF to OA (14 steps)
Return to level 5 through OA (1 step)
Walk from OA to CJ (8 steps)
Return to level 4 through CJ (1 step)
Walk from CJ to RE (8 steps)
Return to level 3 through RE (1 step)
Walk from RE to IC (4 steps)
Recurse into level 4 through IC (1 step)
Walk from IC to RF (10 steps)
Recurse into level 5 through RF (1 step)
Walk from RF to NM (8 steps)
Recurse into level 6 through NM (1 step)
Walk from NM to LP (12 steps)
Recurse into level 7 through LP (1 step)
Walk from LP to FD (24 steps)
Recurse into level 8 through FD (1 step)
Walk from FD to XQ (8 steps)
Recurse into level 9 through XQ (1 step)
Walk from XQ to WB (4 steps)
Return to level 8 through WB (1 step)
Walk from WB to ZH (10 steps)
Return to level 7 through ZH (1 step)
Walk from ZH to CK (14 steps)
Return to level 6 through CK (1 step)
Walk from CK to XF (10 steps)
Return to level 5 through XF (1 step)
Walk from XF to OA (14 steps)
Return to level 4 through OA (1 step)
Walk from OA to CJ (8 steps)
Return to level 3 through CJ (1 step)
Walk from CJ to RE (8 steps)
Return to level 2 through RE (1 step)
Walk from RE to XQ (14 steps)
Return to level 1 through XQ (1 step)
Walk from XQ to FD (8 steps)
"""
    assert maze.edges['FDo1', 'FDi0'].cost == 1
    assert maze.edges['FDi0', 'ZZ'].cost == 18
    assert maze.dijkstra('AA', 'ZZ') == 396


if __name__ == "__main__":
    raw = open("input.txt").read()
    maze = Maze(raw)
    print(maze.dijkstra('AA', 'ZZ'))
    maze = Maze(raw, part=2)
    print(maze.dijkstra('AA', 'ZZ'))
