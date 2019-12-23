class Deck:
    CUT, INC, NEW = range(3)

    def __init__(self, size, raw, virtual=False):
        self.size = size
        self.moves = [(Deck.NEW, None) if "new" in move else
                      (Deck.INC, int(move.split(" ")[-1].strip())) if " inc" in move else
                      (Deck.CUT, int(move.split(" ")[-1].strip()))
                      for move in raw if move.strip()]
        if not virtual:
            self.cards = list(range(size))

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a, m):
        # https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def reverse(self, position, steps):
        # x = position
        # a = multiplier
        # b = delta
        multiplier = 1
        delta = 0
        for move, value in reversed(self.moves):
            if move == Deck.NEW:
                # self.size -(ax + b) -1 => -ax -b + self.size - 1
                multiplier = -multiplier
                delta = self.size - 1 - delta
            elif move == Deck.INC:
                # (ax + b) * pow(...) => a*pow(...)x +b*pow(...)
                multiplier = multiplier * pow(value, self.size - 2, self.size)
                delta = delta * pow(value, self.size - 2, self.size)
            elif move == Deck.CUT:
                # (ax + b) + value => ax + b + value
                delta += value
        # ((ax + b) steps times) % size
        # 1 = (ax + b)
        # 2 = a*(ax + b) + b => a^2x + ab + b
        # 3 = a*(a^2x + ab + b) + b => a^3x + a^2b + a*b + b
        # 4 = a*(a^3x + a^2b + a*b + b) + b => a^4x + a^3b + a^2b + a*b + b
        #
        # a^4x + a^3b + a^2b + a*b + b => a^4x + b * (a^3 + a^2 + a^1 + a^0)
        #
        # https://en.wikipedia.org/wiki/Geometric_progression#Geometric_series
        # (a^3 + a^2 + a^1 + a^0) => (1 - a^3)/(1 - a)
        #

        # if steps == 1:
        #     return (multiplier * position + delta) % self.size
        # if steps == 2:
        #     return (multiplier**2 * position + multiplier * delta + delta) % self.size

        # https://stackoverflow.com/a/3530661
        # https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
        return (position * pow(multiplier, steps, self.size) + delta * (1 - pow(multiplier, steps, self.size)) * (self.modinv(1 - multiplier, self.size))) % self.size

    def process(self):
        for move, value in self.moves:
            if move == Deck.NEW:
                self.cards = self.cards[::-1]
            elif move == Deck.INC:
                cards = self.cards[:]
                for n in range(self.size):
                    cards[(n * value) % self.size] = self.cards[n]
                self.cards = cards
            elif move == Deck.CUT:
                self.cards = self.cards[value:] + self.cards[:value]


def do_test(size, raw):
    data = raw.strip().split("\n")
    deck = Deck(size, data[:-1])
    deck.process()
    assert deck.cards == [int(n.strip()) for n in data[-1].split(":")[-1].split(" ") if n.strip()]


def test_p1():
    do_test(10, """deal with increment 7
deal into new stack
deal into new stack
Result: 0 3 6 9 2 5 8 1 4 7""")


def test_p2():
    do_test(10, """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
Result: 9 2 5 8 1 4 7 0 3 6""")


def test_p3():
    raw = """deal into new stack
cut 5
deal with increment 3
""".split("\n")
    deck = Deck(17, raw)
    assert deck.reverse(0, 0) == 0
    assert deck.reverse(16, 1) == 0
    assert deck.reverse(15, 1) == 6
    assert deck.reverse(14, 1) == 12
    assert deck.reverse(1, 1) == 5
    assert deck.reverse(0, 1) == 11
    assert deck.reverse(13, 2) == 5
    assert deck.reverse(4, 2) == 4


def investigate(raw, card, size, steps, save_all=True):
    deck = Deck(size, raw)
    positions = [None for n in range(steps)]
    positions[0] = card
    results = positions[:]
    with open("results.csv", "w") as output:
        for n in range(1, steps):
            print(n)
            if save_all:
                output.write(";".join(str(card) for card in deck.cards) + "\n")
            deck.process()
            positions[n] = deck.cards[card]
            results[n] = deck.cards.index(card)
        if not save_all:
            output.write("\n".join("{};{}".format(results[n], positions[n]) for n in range(steps)))


if __name__ == "__main__":
    raw = open("input.txt").read().strip().split("\n")

    deck = Deck(10007, raw)
    deck.process()
    print(deck.cards.index(2019))

    deck = Deck(119315717514047, raw, virtual=True)
    print(deck.reverse(2020, 101741582076661))
