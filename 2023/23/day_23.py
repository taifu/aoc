from typing import TypeAlias, Union
from collections import deque, defaultdict


POSITION: TypeAlias = Union[complex, int]


class Maze:
    def __init__(self, raw: str, part2: bool = False):
        self.map = dict((complex(x, y), char)
                        for y, line in enumerate(raw.splitlines()[1:-1])
                        for x, char in enumerate(line[1:-1]))
        self.size = int((len(self.map))**0.5)
        assert self.size ** 2 == len(self.map)
        self.start: POSITION = 0
        self.end: POSITION = complex(self.size - 1, self.size - 1)
        self.explore(part2)

    def around(self, position: POSITION, last_position: POSITION) -> list[tuple[POSITION, str, bool]]:
        next_positions = []
        for direction in (-1, 1, -1j, 1j):
            next_position = position + direction
            if next_position == last_position:
                continue
            if (next_position.real >= 0 and next_position.real < self.size and next_position.imag >= 0
                and next_position.imag < self.size and self.map[next_position] != '#'):  # noqa: 503
                char = self.map[next_position]
                if char != '#':
                    if char != '.':
                        if next_position.imag > position.imag:
                            against = char == '^'
                        elif next_position.imag < position.imag:
                            against = char == 'v'
                        elif next_position.real > position.real:
                            against = char == '<'
                        else:
                            assert next_position.real < position.real
                            against = char == '>'
                    else:
                        against = False
                    next_positions.append((next_position, self.map[next_position], against))
        return next_positions

    def explore(self, part2: bool) -> None:
        self.graph: dict[POSITION, set[tuple[POSITION, int]]] = defaultdict(set)
        path = deque(((self.start, '.', self.start),))
        while path:
            position, last_char, last_position = path.popleft()
            previous_position, next_position = last_position, position
            cost = 0
            while True:
                next_positions = self.around(next_position, last_position)
                (next_position, next_char, _), last_position = next_positions[0], next_position
                cost += 1
                if next_char == '.':
                    assert len(next_positions) == 1, next_positions
                    if next_positions[0][0] == self.end:
                        break
                    continue
                break
            if next_positions[0][0] == self.end:
                self.graph[previous_position].add((next_positions[0][0], cost + 1))
                self.graph[self.end].add((previous_position, cost + 2))
                break
            slide_position = next_position
            next_positions = self.around(next_position, last_position)
            assert len(next_positions) == 1
            next_position, node_char, against = next_positions[0]
            assert node_char == '.'
            cost += 1
            self.graph[previous_position].add((next_position, cost + 1))
            if next_position not in self.graph:
                next_positions, last_position = self.around(next_position, slide_position), next_position
                for new_position, next_char, new_against in next_positions:
                    if (new_position, next_char, last_position) not in path:
                        assert next_char in '>v'
                        if part2 or not new_against:
                            path.append((new_position, next_char, last_position),)
            if previous_position != self.start and part2:
                self.graph[next_position].add((previous_position, cost + 1))
        # Remove start/end edge
        self.start, start_cost = self.graph[self.start].pop()
        self.end, end_cost = self.graph[self.end].pop()
        self.start_end_cost = start_cost + end_cost

    def longest(self) -> int:
        # Stack for DFS, each element is a tuple (node, current_length, path)
        stack, longest_path_length = deque([(self.start, 0, [self.start])]), 0

        while stack:
            current, current_length, visited = stack.pop()

            if current == self.end and current_length > longest_path_length:
                longest_path_length = current_length

            for neighbor, weight in self.graph[current]:
                # Each node is visited at most once
                if neighbor not in visited:
                    next_length = current_length + weight
                    stack.append((neighbor, next_length, visited + [neighbor]))

        return longest_path_length + self.start_end_cost


def solve1(data: str) -> int:
    return Maze(data).longest()


def solve2(data: str) -> int:
    return Maze(data, True).longest()
    pass


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
