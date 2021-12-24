from collections import deque


class Amphipods:
    # Burrow
    # 1  2  3  4  5  6  7
    #      8  9 10 11
    #     12 13 14 15
    #
    #     16 17 18 19
    #     20 21 22 23
    #
    HOME = {'A': (8, 12, 16, 20), 'B': (9, 13, 17, 21), 'C': (10, 14, 18, 22), 'D': (11, 15, 19, 23)}
    RANGE_HOME = {'A': {1: (2,), 2: (), 3: (), 4: (3,), 5: (4, 3), 6: (5, 4, 3), 7: (6, 5, 4, 3)},
                  'B': {1: (2, 3), 2: (3,), 3: (), 4: (), 5: (4,), 6: (5, 4), 7: (6, 5, 4)},
                  'C': {1: (2, 3, 4), 2: (3, 4), 3: (4,), 4: (), 5: (), 6: (5,), 7: (6, 5)},
                  'D': {1: (2, 3, 4, 5), 2: (3, 4, 5), 3: (4, 5), 4: (5,), 5: (), 6: (), 7: (6,)},
                  }
    BURROW = {1: {2: 1},
              2: {1: 1, 8: 2, 3: 2},
              3: {2: 2, 8: 2, 9: 2, 4: 2},
              4: {3: 2, 9: 2, 10: 2, 5: 2},
              5: {4: 2, 10: 2, 11: 2, 6: 2},
              6: {5: 2, 11: 2, 7: 1},
              7: {6: 1},
              8: {2: 2, 3: 2, 12: 1},
              9: {3: 2, 4: 2, 13: 1},
              10: {4: 2, 5: 2, 14: 1},
              11: {5: 2, 6: 2, 15: 1},
              12: {8: 1},
              13: {9: 1},
              14: {10: 1},
              15: {11: 1}
              }
    BURROW_2 = {12: {8: 1, 16: 1},
                13: {9: 1, 17: 1},
                14: {10: 1, 18: 1},
                15: {11: 1, 19: 1},
                16: {12: 1, 20: 1},
                17: {13: 1, 21: 1},
                18: {14: 1, 22: 1},
                19: {15: 1, 23: 1},
                20: {16: 1},
                21: {17: 1},
                22: {18: 1},
                23: {19: 1}
                }
    ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    FINAL = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '',
             8: 'A', 12: 'A', 9: 'B', 13: 'B', 10: 'C', 14: 'C', 11: 'D', 15: 'D'}
    FINAL_2 = {16: 'A', 17: 'B', 18: 'C', 19: 'D',
               20: 'A', 21: 'B', 22: 'C', 23: 'D'}

    def __init__(self, data, second=False):
        raw_amphipods = [c for c in "".join(data.strip().split('\n')[2:-1]) if c.isalpha()]
        if second:
            raw_amphipods[4:4] = ['D', 'C', 'B', 'A', 'D', 'B', 'A', 'C']
            self.BURROW.update(self.BURROW_2)
            self.FINAL.update(self.FINAL_2)
        self.burrow = dict((n, raw_amphipods[n - 8] if n > 7 else '') for n in range(1, 24 if second else 16))

    def next_burrows(self, burrow, cache={}):
        key = frozenset(burrow.items())
        try:
            return cache[key]
        except KeyError:
            pass
        amphipods = ((v, k) for k, v in burrow.items() if v.isalpha())
        burrows_energies = []
        for amphipod, pos in amphipods:
            if pos < 8:
                # Try going home
                if all(burrow.get(pos_home, '') in ('', amphipod) for pos_home in self.HOME[amphipod]):
                    energy = 0
                    next_pos = pos
                    for pos_hallway in self.RANGE_HOME[amphipod][pos]:
                        if burrow[pos_hallway] == '':
                            energy += self.BURROW[next_pos][pos_hallway] * self.ENERGY[amphipod]
                            next_pos = pos_hallway
                        else:
                            break
                    else:
                        # Go home deepest pos
                        energy += self.ENERGY[amphipod]
                        for pos_home in self.HOME[amphipod]:
                            if burrow.get(pos_home, None) == '':
                                energy += self.ENERGY[amphipod]
                                last_pos_home = pos_home
                            else:
                                break
                        next_burrow = burrow.copy()
                        next_burrow[last_pos_home] = amphipod
                        next_burrow[pos] = ''
                        burrows_energies.append((next_burrow, energy))
            else:
                # Try staying home
                if pos in self.HOME[amphipod] and all(burrow.get(pos_home, amphipod) == amphipod for pos_home in self.HOME[amphipod] if pos_home > pos):
                    continue
                # Try exiting room
                next_pos = pos
                energy = 0
                while True:
                    if next_pos > 11:
                        next_pos -= 4
                        if burrow[next_pos] != '':
                            break
                        energy += self.ENERGY[amphipod]
                    elif next_pos > 7:
                        for hallway_pos, cost in self.BURROW[next_pos].items():
                            if hallway_pos < 8 and burrow[hallway_pos] == '':
                                next_burrow = burrow.copy()
                                next_burrow[hallway_pos] = amphipod
                                next_burrow[pos] = ''
                                hallway_energy = energy + cost * self.ENERGY[amphipod]
                                burrows_energies.append((next_burrow, hallway_energy))
                                # Add also walk into hallway
                                direction = 1 if hallway_pos % 2 != next_pos % 2 else -1
                                prev_pos = hallway_pos
                                while hallway_pos > 1 and hallway_pos < 7:
                                    hallway_pos += direction
                                    hallway_energy += self.BURROW[prev_pos][hallway_pos] * self.ENERGY[amphipod]
                                    prev_pos = hallway_pos
                                    if burrow[hallway_pos] == '':
                                        next_burrow = burrow.copy()
                                        next_burrow[hallway_pos] = amphipod
                                        next_burrow[pos] = ''
                                        burrows_energies.append((next_burrow, hallway_energy))
                                    else:
                                        break
                        break
                else:
                    continue

        cache[key] = burrows_energies
        return burrows_energies

    def explore(self, burrow, worst):
        burrows = deque(((burrow, 0, 0),))
        visited = {frozenset(burrow.items()): 0}
        while burrows:
            burrow, energy, moves = burrows.popleft()
            key = frozenset(burrow.items())
            for next_burrow, next_energy in self.next_burrows(burrow):
                key = frozenset(next_burrow.items())
                if energy + next_energy >= visited.get(key, worst):
                    continue
                visited[key] = energy + next_energy
                if next_burrow == self.FINAL:
                    continue
                burrows.append((next_burrow, energy + next_energy, moves + 1))
        return visited

    def energy(self, worst):
        visited = self.explore(self.burrow, worst)
        return visited[frozenset(self.FINAL.items())]


def solve1(data):
    return Amphipods(data).energy(15000)


def solve2(data):
    return Amphipods(data, True).energy(60000)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
