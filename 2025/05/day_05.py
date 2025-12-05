import bisect


type Ingredient = int
type Ingredients = tuple[Ingredient, ...]
type Range = list[int]
type Ranges = list[Range]


class Inventory:
    def __init__(self, data: str) -> None:
        part = data.strip().split('\n\n')
        self.ranges: Ranges = self.merge_sorted_ranges(sorted(tuple(int(p) for p in rang.split('-'))
                                                              for rang in part[0].split('\n')))
        self.starts: tuple[int, ...] = tuple(rang[0] for rang in self.ranges)
        self.ingredients: Ingredients = tuple(int(ing) for ing in part[1].split('\n'))

    def merge_sorted_ranges(self, ranges: list[tuple[int, ...]]) -> Ranges:
        merged: Ranges = []
        for start, end in ranges:
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
        return merged

    def freshes(self) -> int:
        count = 0
        for ingr in self.ingredients:
            pos = bisect.bisect_right(self.starts, ingr) - 1
            if pos >= 0 and self.ranges[pos][0] <= ingr <= self.ranges[pos][1]:
                count += 1
        return count

    def all_freshes(self) -> int:
        return sum((rang[1] - rang[0] + 1) for rang in self.ranges)


def load(data: str) -> Inventory:
    return Inventory(data)


def solve1(data: str) -> int:
    return load(data).freshes()


def solve2(data: str) -> int:
    return load(data).all_freshes()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
