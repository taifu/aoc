from dataclasses import dataclass


R, G, B = range(3)
COLORS = {R: 0, G: 0, B: 0}


class Move:
    def __init__(self, raw: str) -> None:
        self.colors = COLORS.copy()
        for parts in raw.strip().split(","):
            part = parts.split()
            self.colors[{"red": R, "green": G, "blue": B}[part[1]]] = int(part[0])


@dataclass
class Game:
    moves: list[Move]

    def __post_init__(self) -> None:
        self._set_colors()

    def _set_colors(self) -> None:
        self.colors = COLORS.copy()
        for move in self.moves:
            for color in COLORS.keys():
                self.colors[color] = max(self.colors[color], move.colors[color])

    def power(self) -> int:
        return self.colors[R] * self.colors[G] * self.colors[B]


def load(data: str) -> dict[int, Game]:
    games = {}
    for line in data.strip().split("\n"):
        parts = line.split(":")
        id_ = int(parts[0].split()[1])
        games[id_] = Game([Move(raw) for raw in parts[1].split(";")])
    return games


def solve1(data: str) -> int:
    return sum(id_ for id_, game in load(data).items()
               if all(game.colors[color] <= {R: 12, G: 13, B: 14}[color]
                      for color in (R, G, B)))


def solve2(data: str) -> int:
    return sum(game.power() for game in load(data).values())


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
