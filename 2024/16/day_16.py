import heapq
from typing import TypeAlias, List, Tuple, Generator, Set, Optional  # noqa: F401

Position: TypeAlias = Tuple[int, int]
Direction: TypeAlias = Tuple[int, int]

E, S, W, N = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIRECTIONS = (E, S, W, N)
COSTS = {E: {E: 1, S: 1000, N: 1000},
         W: {W: 1, S: 1000, N: 1000},
         N: {N: 1, W: 1000, E: 1000},
         S: {S: 1, W: 1000, E: 1000},
         }


class Solution:
    def __init__(self, raw: str) -> None:
        self.map = set()
        for y, line in enumerate(raw.splitlines()[1:]):
            for x, char in enumerate(line[1:-1]):
                if char in ('S', 'E', '.'):
                    if char == 'S':
                        self.start = (x, y)
                        continue
                    self.map.add((x, y))
                    if char == 'E':
                        self.end = (x, y)
        self.size = len(line) - 2
        self.explore()
        self.cost_shortest_path: int = int(min(self.visited.get((self.end, direction), float('inf')) for direction in DIRECTIONS))

    def draw(self, visited: Set[Position]) -> None:
        print("#" * (self.size + 2))
        for y in range(self.size):
            line = ""
            for x in range(self.size):
                if (x, y) == self.start:
                    line += "S"
                elif (x, y) == self.end:
                    line += "E"
                elif (x, y) in visited:
                    line += "O"
                elif (x, y) in self.map:
                    line += "."
                else:
                    line += "#"
            print("#" + line + "#")
        print("#" * (self.size + 2))
        print()

    def explore(self) -> None:
        stack: List[Tuple[int, Position, Position]] = []
        heapq.heappush(stack, (0, self.start, E))
        self.visited = {(self.start, E): 0}

        while stack:
            length, pos, direction = heapq.heappop(stack)
            try:
                if self.visited[(pos, direction)] < length:
                    continue
            except KeyError:
                pass

            for next_direction, cost in COSTS[direction].items():
                # Forward
                if next_direction == direction:
                    next_pos = (pos[0] + next_direction[0], pos[1] + next_direction[1])
                    if next_pos not in self.map:
                        continue
                # Turn ±90°
                else:
                    next_pos = pos
                next_length = length + cost

                if self.visited.get((next_pos, next_direction), float('inf')) <= next_length:
                    continue
                self.visited[next_pos, next_direction] = next_length
                heapq.heappush(stack, (next_length, next_pos, next_direction))

    def count(self) -> int:
        return self.cost_shortest_path

    def count2(self) -> int:
        stack = [k for k, v in self.visited.items() if k[0] == self.end and v == self.cost_shortest_path]

        shortest_path_cells = set()

        while stack:
            pos, direction = stack.pop(0)

            shortest_path_cells.add(pos)

            for next_direction, cost in COSTS[direction].items():
                if next_direction == direction:
                    next_pos = (pos[0] - next_direction[0], pos[1] - next_direction[1])
                else:
                    next_pos = pos
                if (next_pos, next_direction) in self.visited and self.visited[(next_pos, next_direction)] + cost == self.visited[(pos, direction)]:
                    stack.append((next_pos, next_direction))

        return len(shortest_path_cells)


solution = None


def solve1(data: str) -> int:
    global solution
    if solution is None:
        solution = Solution(data)
    assert solution
    return solution.count()


def solve2(data: str) -> int:
    global solution
    if solution is None:
        solution = Solution(data)
    assert solution
    return solution.count2()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
