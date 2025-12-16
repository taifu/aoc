from math import inf
from collections import defaultdict
from itertools import product
from functools import cache


type Diagram = tuple[int, ...]
type Button = tuple[int, ...]
type Joltage = tuple[int, ...]


class Machine:
    def __init__(self, line: str) -> None:
        # Elementi della macchina
        raw_diagram, *raw_buttons, raw_joltage = line.split()
        self.diagram = tuple(1 if rd == '#' else 0 for rd in raw_diagram[1:-1])
        self.buttons = [tuple(map(int, rb[1:-1].split(','))) for rb in raw_buttons]
        self.joltage = tuple(int(p) for p in raw_joltage[1:-1].split(','))

        # Possibili pressioni (1 per bottone) che portano a un dato diagramma
        self.diagram_patterns = defaultdict[Diagram, list[Button]](list)

        # Jolt ottenibili da tutte le combinazioni di pressioni possibili (solo 1 per bottone massimo)
        self.added_joltage: dict[tuple[int, ...], Joltage] = {}

        for pressed in product((0, 1), repeat=len(self.buttons)):
            joltage = [0] * len(self.joltage)
            for i, p in enumerate(pressed):
                for j in self.buttons[i]:
                    joltage[j] += p
            parity_lights = tuple(j % 2 for j in joltage)
            self.added_joltage[pressed] = tuple(joltage)
            self.diagram_patterns[parity_lights] += [pressed]

    def get_diagram(self) -> int:
        # Per la parte 1 al massimo ogni bottone deve essere premuto una volta sola (due volte == zero volte)
        return min([sum(b) for b in self.diagram_patterns[self.diagram]])

    @cache
    def get_joltage(self, joltage_target: Joltage) -> float:
        if all(x == 0 for x in joltage_target):
            return 0
        if any(x < 0 for x in joltage_target):
            return inf

        # Considero solo le pressioni che corrispondono alla parità del target attuale
        press_count, parity_lights = inf, tuple(x % 2 for x in joltage_target)
        for pressed in self.diagram_patterns[parity_lights]:
            # La divisione per due non dà resti perché considero solo
            # le pressioni che hanno messo a zero la parità del target
            new_joltage_target = tuple((b - a) / 2 for a, b in zip(self.added_joltage[pressed], joltage_target))
            press_count = min(press_count, sum(pressed) + 2 * self.get_joltage(new_joltage_target))
        return press_count


class Factory:
    def __init__(self, data: str) -> None:
        self.machines = [Machine(line) for line in data.strip().splitlines()]

    def get_diagram(self) -> int:
        return sum(machine.get_diagram() for machine in self.machines)

    def get_joltage(self) -> int:
        return sum(int(machine.get_joltage(machine.joltage)) for machine in self.machines)


def load(data: str) -> Factory:
    return Factory(data)


def solve1(data: str) -> int:
    return load(data).get_diagram()


def solve2(data: str) -> int:
    return load(data).get_joltage()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
