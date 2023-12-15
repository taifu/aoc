from collections import defaultdict, OrderedDict


class Step:
    def __init__(self, line: str):
        self.chars = list(line)

    def hash(self, chars: list[str] = []) -> int:
        value = 0
        for char in chars or self.chars:
            value += ord(char)
            value = (value * 17) % 256
        return value

    def hashmap(self) -> tuple[str, int, str, int]:
        chars = self.chars if self.chars[-1].isdigit() else self.chars + ['0']
        return ''.join(chars[:-2]), self.hash(chars[:-2]), chars[-2], int(chars[-1])


class Sequence:
    def __init__(self, raw: str):
        self.steps = [Step(line) for line in raw.strip().split(',')]

    def hash(self) -> int:
        return sum(step.hash() for step in self.steps)

    def hashmap(self) -> int:
        boxes: defaultdict[int, OrderedDict[str, int]] = defaultdict(OrderedDict)
        for step in self.steps:
            label, box, op, focal = step.hashmap()
            if op == '=':
                boxes[box][label] = focal
            elif label in boxes[box]:
                del boxes[box][label]
        return sum((box + 1) * n * boxes[box][label] for box in range(256)
                   for n, label in enumerate(boxes.get(box, {}), start=1))


def solve1(data: str) -> int:
    return Sequence(data).hash()


def solve2(data: str) -> int:
    return Sequence(data).hashmap()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
