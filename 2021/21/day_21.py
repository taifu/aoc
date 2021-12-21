from collections import defaultdict
import itertools


class Game:
    def __init__(self, data):
        self.places = [int(line[-1]) - 1 for line in data.strip().split('\n')]
        count_dirac = defaultdict(int)
        for dices in itertools.product([1, 2, 3], repeat=3):
            value = sum(dices)
            count_dirac[value] += 1
        self.dirac = tuple(count_dirac.items())

    def play_det(self):
        places, scores = self.places, [0, 0]
        turns = dice = 0
        while max(scores) < 1000:
            roll = dice * 3 + 6 - 100 * max(0, dice - 97)
            dice = (dice + 3) % 100
            places[turns % 2] = (places[turns % 2] + roll) % 10
            scores[turns % 2] += places[turns % 2] + 1
            turns += 1
        return turns * 3 * min(scores)

    def play_dirac(self, turn=0, scores=[0, 0], places=None, cache={}):
        if places is None:
            places = self.places
        key = turn, tuple(scores), tuple(places)
        try:
            return cache[key]
        except KeyError:
            pass
        wins = [0, 0]
        for roll, times in self.dirac:
            new_places, new_scores = places.copy(), scores.copy()
            new_places[turn] = (new_places[turn] + roll) % 10
            new_scores[turn] += new_places[turn] + 1
            if new_scores[turn] >= 21:
                wins[turn] += times
            else:
                new_wins = self.play_dirac(1 - turn, new_scores, new_places)
                wins = [wins[n] + times * new_wins[n] for n in range(2)]
        cache[key] = wins
        return wins


def solve1(data):
    return Game(data).play_det()


def solve2(data):
    return max(Game(data).play_dirac())


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
