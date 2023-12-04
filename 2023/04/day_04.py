class Card:
    def __init__(self, line: str):
        parts = line.split(':')
        self._id = int(parts[0].split(' ')[-1])
        parts = parts[1].split('|')
        self.numbers = [set(int(n) for n in parts[k].split()) for k in (0, 1)]

    @property
    def wins(self) -> int:
        return len(self.numbers[1].intersection(self.numbers[0]))

    @property
    def value(self) -> int:
        return int(2**(self.wins - 1)) if self.wins else 0


class Cards:
    def __init__(self, data: str) -> None:
        cards = [Card(line) for line in data.splitlines()]
        self.deck = dict((card._id, card) for card in cards)
        self.cache: dict[int, int] = {}

    def count(self, card: Card) -> int:
        try:
            return self.cache[card._id]
        except KeyError:
            key = card._id
            tot = 1 + sum(self.count(self.deck[id_])
                          for id_ in range(card._id + 1, card._id + card.wins + 1))
            self.cache[key] = tot
            return tot


def solve1(data: str) -> int:
    return sum(card.value for card in Cards(data).deck.values())


def solve2(data: str) -> int:
    cards = Cards(data)
    return sum(cards.count(card) for card in cards.deck.values())


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
