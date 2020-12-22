from collections import deque


def parse(data):
    return [deque(int(c) for c in cards.split('\n')[1:]) for cards in data.strip().split('\n\n')]


def points(deck):
    return sum((len(deck) - n) * card for n, card in enumerate(deck))


def dealt(decks):
    return [deck.popleft() for deck in decks]


def win(decks, cards, step):
    if step == 2 and all(len(decks[n]) >= cards[n] for n in range(2)):
        return game([deque(list(decks[0])[:cards[0]]), deque(list(decks[1])[:cards[1]])], step)
    return cards.index(max(cards))


def game(decks, step):
    previous = set()
    while all(decks):
        this_round = tuple((tuple(decks[0]), tuple(decks[1])))
        if this_round in previous:
            return 0
        previous.add(this_round)
        cards = dealt(decks)
        winner = win(decks, cards, step)
        decks[winner].extend([cards[winner], cards[1 - winner]])
    return winner


def solve(data, step=1):
    decks = parse(data)
    return points(decks[game(decks, step)])


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, step=2))
