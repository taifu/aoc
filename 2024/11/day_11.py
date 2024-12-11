from collections import defaultdict


class Stones:
    def __init__(self, data: str) -> None:
        self.stones = defaultdict(int)
        for raw in data.strip().split():
            self.stones[int(raw)] = 1

    def count(self, times: int) -> None:
        for time in range(times):
            self.stones_copy = self.stones.copy()
            for stone, how_much in self.stones_copy.items():
                if not how_much:
                    continue
                self.stones[stone] -= how_much
                if stone == 0:
                    self.stones[1] += how_much
                elif len(str(stone)) % 2 == 0:
                    left, right = int(str(stone)[:len(str(stone)) // 2]), int(str(stone)[len(str(stone)) // 2:])
                    self.stones[left] += how_much
                    self.stones[right] += how_much
                else:
                    self.stones[stone * 2024] += how_much
        return sum(self.stones.values())


def solve1(data: str) -> int:
    return Stones(data).count(25)


def solve2(data: str) -> int:
    return Stones(data).count(75)


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
