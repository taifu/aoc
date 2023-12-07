from typing import TypeAlias, List, Any
from collections import Counter

Mapping: TypeAlias = List[List[int]]


class Hand:
    def __init__(self, line: str, part2: bool = False):
        _cards, _bid = line.split()
        self.bid = int(_bid)
        self.indexed = "J23456789TQKA" if part2 else "23456789TJQKA"
        self.ordered = self.order(_cards)
        self.cards = self.arrange(_cards) if part2 else _cards
        self.rank = self.identify()

    def order(self, cards: str) -> List[int]:
        return [self.indexed.index(card) for card in cards]

    def arrange(self, cards: str) -> str:
        jolly = cards.count('J')
        if jolly == 5:
            return 'JJJJJ'
        if jolly > 0:
            cards = cards.replace('J', '')
            counter = Counter(cards)
            order = self.order(cards)
            if counter.most_common()[0][1] == 4 or len(counter) == 1:
                highest = cards[0]
            elif counter.most_common()[0][1] == 1:
                highest = cards[order.index(max(order))]
            elif counter.most_common()[0][1] > counter.most_common()[1][1]:
                highest = counter.most_common()[0][0]
            else:
                if self.order(counter.most_common()[0][0]) > self.order(counter.most_common()[1][0]):
                    highest = counter.most_common()[0][0]
                else:
                    highest = counter.most_common()[1][0]
            cards += highest * jolly
        return cards

    def identify(self) -> int:
        counter = Counter(self.cards)
        if len(counter) == 5:
            return 1
        elif len(counter) == 4:
            return 2
        elif len(counter) == 3:
            if counter.most_common()[0][1] == 3:
                return 4
            else:
                return 3
        elif len(counter) == 2:
            if counter.most_common()[0][1] == 3:
                return 5
            else:
                return 6
        return 7

    def __eq__(self, obj: Any) -> bool:
        return bool(self.cards == obj.cards)

    def __lt__(self, obj: Any) -> bool:
        if self.rank == obj.rank:
            return bool(self.ordered < obj.ordered)
        return bool(self.rank < obj.rank)


class Deck:
    def __init__(self, data: str, part2: bool = False):
        self.hands = sorted([Hand(line, part2=part2) for line in data.splitlines()])

    def total(self) -> int:
        return sum((n + 1) * hand.bid for n, hand in enumerate(sorted(self.hands)))


def solve1(data: str) -> int:
    return Deck(data).total()


def solve2(data: str) -> int:
    return Deck(data, part2=True).total()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))