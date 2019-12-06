from collections import defaultdict, deque


INF = float('inf')


class Graph:
    def __init__(self, maps):
        self.edges_directed = {}
        self.edges = defaultdict(list)
        self.vertices = set()
        for edge in maps.strip().split("\n"):
            edge_orbited, edge_orbiting = edge.split(")")
            assert edge_orbiting not in self.edges_directed
            self.edges_directed[edge_orbiting] = edge_orbited
            self.edges[edge_orbiting].append((edge_orbited, 1))  # cost always 1
            self.edges[edge_orbited].append((edge_orbiting, 1))
            self.vertices.add(edge_orbited)
            self.vertices.add(edge_orbiting)

    def explore(self, edge):
        if edge not in self.edges_directed:
            return 0
        return 1 + self.explore(self.edges_directed[edge])

    def count(self):
        tot_path = 0
        for edge_orbiting in self.edges_directed:
            tot_path += self.explore(edge_orbiting)
        return tot_path

    def shortest_path(self, source, dest):
        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node
        # and to infinity for other nodes.
        distances = {vertex: INF for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])

            # 6. Stop, if the smallest distance
            # among the unvisited nodes is infinity.
            if distances[current_vertex] == INF:
                break

            # 4. Find unvisited neighbors for the current node
            # and calculate their distances through the current node.
            for neighbour, cost in self.edges[current_vertex]:
                alternative_route = distances[current_vertex] + cost

                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

            # 5. Mark the current node as visited
            # and remove it from the unvisited set.
            vertices.remove(current_vertex)

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path


def test_orbits():
    maps = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
    assert Graph(maps).count() == 42
    maps = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
    assert len(Graph(maps).shortest_path("YOU", "SAN")) == 4 + 3


if __name__ == "__main__":
    graph = Graph(open("input.txt").read())
    print(graph.count())
    print(len(graph.shortest_path("YOU", "SAN")) - 3)
