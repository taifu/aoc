from collections import deque, defaultdict, OrderedDict
from itertools import combinations
from operator import itemgetter


class Wires:
    def __init__(self, raw: str) -> None:
        self.graph: OrderedDict[str, list[str]] = OrderedDict()
        self.nodes = set()

        for line in raw.splitlines():
            wires = line.replace(':', '').split(' ')
            wire_from = wires[0]
            self.nodes.add(wire_from)
            for wire_to in wires[1:]:
                self.nodes.add(wire_to)
                try:
                    self.graph[wire_from].append(wire_to)
                except KeyError:
                    self.graph[wire_from] = [wire_to]
                try:
                    self.graph[wire_to].append(wire_from)
                except KeyError:
                    self.graph[wire_to] = [wire_from]

    def bfs_shortest_path(self, start: str, end: str = "") -> dict[str, list[str]]:
        # A queue to manage the nodes to be checked, starts with the start node
        queue = deque([start])

        # A set to skip already managed nodes
        seen = set([start])

        # A dictionary to track distances to each node and the path taken
        paths: dict[str, list[str]] = {vertex: [] for vertex in self.graph}
        paths[start] = [start]

        while queue:
            vertex = queue.popleft()

            for neighbor in self.graph[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    paths[neighbor] = paths[vertex] + [neighbor]
                    queue.append(neighbor)

                    if neighbor == end:
                        return paths

        return paths

    def split(self) -> int:
        nodes = sorted(self.nodes)
        bridges: dict[tuple[str, str], int] = defaultdict(int)
        if len(self.graph) > 100:
            # Heuristic: check only (len(graph) - 1) pairs of nodes
            for node1, node2 in zip(nodes, nodes[1:]):
                paths = self.bfs_shortest_path(node1, node2)
                for node1, node2 in zip(paths[node2], paths[node2][1:]):
                    if node1 > node2:
                        node2, node1 = node1, node2
                    bridges[node1, node2] += 1
        else:
            # Check all pairs of nodes
            for node1, node2 in sorted(combinations(nodes, 2)):
                paths = self.bfs_shortest_path(node1, node2)
                for node1, node2 in zip(paths[node2], paths[node2][1:]):
                    if node1 > node2:
                        node2, node1 = node1, node2
                    bridges[node1, node2] += 1

        bottlenecks = sorted(bridges.items(), key=itemgetter(1), reverse=True)
        removed: set[tuple[str, str]] = set()
        for count in range(3):
            node1, node2 = bottlenecks[count][0]
            removed.add((node1, node2))
            self.graph[node1].remove(node2)
            self.graph[node2].remove(node1)
        paths = self.bfs_shortest_path(nodes[0], nodes[1])
        detached = sum(1 for k, v in paths.items() if len(v) == 0)
        if detached not in (0, len(self.graph)):
            return (len(nodes) - detached) * detached
        raise Exception("Not found")


def solve1(data: str) -> int:
    return Wires(data).split()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
