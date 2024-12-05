from collections import defaultdict
from typing import TypeAlias


Page: TypeAlias = int


class Manual:
    def __init__(self, data: str) -> None:
        raw_rules, raw_prints = data.split('\n\n')
        self.rules = defaultdict(set)
        for rule in raw_rules.splitlines():
            after, before = [int(p) for p in rule.split('|')]
            self.rules[after].add(before)
        self.all_befores: dict[tuple[Page, ...], dict[Page, set[Page]]] = {}
        self.all_afters: dict[tuple[Page, ...], dict[Page, set[Page]]] = {}
        for prints in raw_prints.splitlines():
            pages = tuple(int(p) for p in prints.split(','))
            self.all_befores[pages] = {}
            self.all_afters[pages] = {}
            for n, page in enumerate(pages):
                if n > 0:
                    self.all_befores[pages][page] = set(pages[:n])
                if n < len(pages) - 1:
                    self.all_afters[pages][page] = set(pages[n + 1:])
        self.explore()

    def explore(self) -> None:
        self.right_order_pages = []
        self.wrong_order_pages = []
        for pages, afters in self.all_afters.items():
            ok = True
            for page, after in afters.items():
                if after > self.rules[page]:
                    ok = False
                    break
            else:
                for page, befores in self.all_befores[pages].items():
                    for page_before in befores:
                        if page_before in self.rules[page]:
                            ok = False
                            break
                    else:
                        continue
                    break
            if ok:
                self.right_order_pages.append(pages)
            else:
                self.wrong_order_pages.append(list(pages))

    def count(self) -> int:
        return sum(pages[(len(pages) - 1) // 2] for pages in self.right_order_pages)

    def count2(self) -> int:
        total = 0
        for wrong_pages in self.wrong_order_pages:
            right_pages = []
            while wrong_pages:
                for page in wrong_pages:
                    if set(wrong_pages) - self.rules[page] == set([page]):
                        right_pages.append(page)
                        wrong_pages.remove(page)
                        break
            total += right_pages[(len(right_pages) - 1) // 2]
        return total


def solve1(data: str) -> int:
    return Manual(data).count()


def solve2(data: str) -> int:
    return Manual(data).count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
