from collections import deque
from collections import defaultdict
from operator import itemgetter


class Wires:
    def __init__(self, raw: str) -> None:
        self.graph = defaultdict(set)
        self.nodes = set()

        for line in raw.splitlines():
            wires = line.replace(':', '').split(' ')
            wire_from = wires[0]
            self.nodes.add(wire_from)
            for wire_to in wires[1:]:
                self.nodes.add(wire_to)
                self.graph[wire_from].add(wire_to)
                self.graph[wire_to].add(wire_from)

    def bfs_shortest_path(self, start: str, end: str) -> tuple[dict[str, float], dict[str, list[str]]]:
        # A queue to manage the nodes to be checked, starts with the start node
        queue = deque([start])

        # A dictionary to track distances to each node and the path taken
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[start] = 0
        paths: dict[str, list[str]] = {vertex: [] for vertex in self.graph}
        paths[start] = [start]

        while queue:
            vertex = queue.popleft()

            for neighbor in self.graph[vertex]:
                if distances[neighbor] == float('infinity'):
                    distances[neighbor] = distances[vertex] + 1
                    paths[neighbor] = paths[vertex] + [neighbor]
                    queue.append(neighbor)

                    if neighbor == end:
                        return distances, paths

        return distances, paths

    def split(self) -> int:
        nodes = list(self.nodes)
        bridges: dict[tuple[str, str], int] = defaultdict(int)
        for node1, node2 in zip(nodes, nodes[1:]):
            _, paths = self.bfs_shortest_path(node1, node2)
            for node1, node2 in zip(paths[node2], paths[node2][1:]):
                bridges[(node1, node2)] += 1

        first_six = sorted(bridges.items(), key=itemgetter(1), reverse=True)[:6]
        removed = set()
        for (node1, node2), _ in first_six:
            if node1 > node2:
                node1, node2, = node2, node1
            if (node1, node2) not in removed:
                removed.add((node1, node2))
                self.graph[node1].remove(node2)
                self.graph[node2].remove(node1)

        _, paths = self.bfs_shortest_path(node1, "")
        detached = sum(1 for k, v in paths.items() if len(v) == 0)
        return (len(nodes) - detached) * detached


def solve1(data: str) -> int:
    return Wires(data).split()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
