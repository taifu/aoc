from collections import Counter


class Hand:
    def __init__(self, line: str, part2: bool = False):
        _cards, _bid = line.split()
        self.bid = int(_bid)
        self.indexed = "J23456789TQKA" if part2 else "23456789TJQKA"
        self.ordered = self.order(_cards)
        self.cards = self.arrange(_cards) if part2 else _cards
        self.rank = self.identify()

    def index(self, card: str) -> int:
        return self.indexed.index(card)

    def order(self, cards: str) -> list[int]:
        return [self.index(card) for card in cards]

    def arrange(self, cards: str) -> str:
        jolly = cards.count('J')
        if 0 < jolly < 5:
            cards = cards.replace('J', '')
            counter, order = Counter(cards), self.order(cards)
            if counter.most_common()[0][1] == 4 or len(counter) == 1:
                highest = cards[0]
            elif counter.most_common()[0][1] == 1:
                highest = cards[order.index(max(order))]
            elif counter.most_common()[0][1] > counter.most_common()[1][1]:
                highest = counter.most_common()[0][0]
            else:
                highest = cards[0 if self.index(cards[0]) > self.index(cards[1]) else 1]
            cards += highest * jolly
        return cards

    def identify(self) -> int:
        counter = Counter(self.cards)
        rank2 = 10 - 2 * len(counter)
        # Tris or two pair
        if rank2 == 4 and counter.most_common()[0][1] != 3:
            rank2 -= 1
        # Full house or Poker
        elif rank2 == 6 and counter.most_common()[0][1] != 3:
            rank2 += 1
        return rank2

    def __lt__(self, obj: object) -> bool:
        if not isinstance(obj, Hand):
            return NotImplemented
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
