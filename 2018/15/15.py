from collections import deque


raw = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""
# 47 * 590 = 27730
# 29 * 172 = 4988

raw = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""
# 37 * 982 = 36334

raw = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""
# 46 * 859 = 39514
# 33 * 948 = 31284

raw = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""
# 35 * 793 = 27755
# 37 * 94 = 3478

raw = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""
# 54 * 536 = 28944
# 39 * 166 = 6474

raw = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""
# 20 * 937 = 18740
# 30 * 38 = 1140

raw = open("input.txt").read()


WALL, OPEN, ELF, GOBLIN = "#", ".", "E", "G"
DELTAS = ((0, -1), (-1, 0), (1, 0), (0, 1))


class Creature:
    def __init__(self, cavern, x, y, ap, hp, char):
        self.cavern = cavern
        self.x = x
        self.y = y
        self.ap = ap
        self.hp = hp
        self.char = char

    @property
    def dead(self):
        return self.hp <= 0

    def __repr__(self):
        return "{}({} {}.{})".format(self.char, self.hp, self.x, self.y)

    def __lt__(self, other):
        return other.y > self.y or (other.y == self.y and other.x > self.x)

    def attackable(self):
        attackables = []
        for x, y in [(self.x + dx, self.y + dy) for dx, dy in DELTAS]:
            creature = self.cavern.get_creature(x, y)
            if creature and creature.char != self.char:
                attackables.append(creature)
        if attackables:
            min_hp = min(creature.hp for creature in attackables)
            return sorted(creature for creature in attackables if creature.hp == min_hp)[0]
        return None

    def go(self, next_dir):
        self.cavern.map[self.y][self.x] = OPEN
        self.x += next_dir[0]
        self.y += next_dir[1]
        self.cavern.map[self.y][self.x] = self.char

    def move_nearest(self):
        explored = set(((self.x, self.y),))
        positions = deque(tuple((p, []) for p in explored))
        nearest, best_path = set(), float("inf")
        while positions:
            (x, y), path = positions.popleft()
            for n, (x, y) in enumerate([(x + dx, y + dy) for dx, dy in DELTAS]):
                if x >= 0 and x < self.cavern.width and y >= 0 and y < self.cavern.height and (x, y) not in explored and self.cavern.map[y][x] in (OPEN, GOBLIN, ELF):
                    next_path = path + [DELTAS[n]]
                    explored.add((x, y))
                    cell = self.cavern.map[y][x]
                    if cell == OPEN:
                        if len(next_path) <= best_path:
                            positions.append(((x, y), next_path))
                    elif cell in (ELF, GOBLIN):
                        if cell != self.char:
                            if len(next_path) <= best_path:
                                if len(next_path) < best_path:
                                    best_path = len(next_path)
                                    nearest = set()
                                next_dir = next_path[0]
                                nearest.add((self.cavern.get_creature(x, y), next_dir))
        if nearest:
            next_dir = sorted(nearest)[0][1]
            self.go(next_dir)
        return


class Elf(Creature):
    def __init__(self, cavern, x, y, ap=3, hp=200):
        super().__init__(cavern=cavern, x=x, y=y, ap=ap, hp=hp, char=ELF)


class Goblin(Creature):
    def __init__(self, cavern, x, y, ap=3, hp=200):
        super().__init__(cavern=cavern, x=x, y=y, ap=ap, hp=hp, char=GOBLIN)


class Cavern:
    def __init__(self, raw, ap_elf=3):
        lines = raw.split("\n")
        self.elves = []
        self.goblins = []
        self.map = [list(line) for line in lines if line]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.n_turns = 0
        self._set(ap_elf)

    def remove_creature(self, creature):
        self.map[creature.y][creature.x] = OPEN
        try:
            self.elves.remove(creature)
        except ValueError:
            self.goblins.remove(creature)

    def get_creature(self, x, y):
        try:
            if self.map[y][x] == ELF:
                creatures = self.elves
            elif self.map[y][x] == GOBLIN:
                creatures = self.goblins
            else:
                creatures = ()
            for creature in creatures:
                if creature.x == x and creature.y == y:
                    return creature
        except IndexError:
            pass
        return None

    def draw(self):
        print()
        print("Turn {}".format(self.n_turns))
        for line in self.map:
            print("".join(line))
        print()
        for creatures in (self.elves, self.goblins):
            print(" ".join(repr(creature) for creature in sorted(creatures)))
        print()

    def _set(self, ap_elf):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == ELF:
                    self.elves.append(Elf(self, x, y, ap_elf))
                elif self.map[y][x] == GOBLIN:
                    self.goblins.append(Goblin(self, x, y))

    def ended(self):
        return len(self.goblins) == 0 or len(self.elves) == 0

    def outcome(self, output=False):
        tot = sum(creature.hp for creature in self.goblins + self.elves)
        if output:
            print(self.n_turns)
            print(tot)
        return tot * self.n_turns

    def turn(self):
        deads = []
        for creature in sorted(self.elves + self.goblins):
            if creature in deads:
                continue
            if not creature.attackable():
                if self.ended():
                    return False
                creature.move_nearest()
            attackable = creature.attackable()
            if attackable:
                attackable.hp -= creature.ap
                if attackable.dead:
                    deads.append(attackable)
                    self.remove_creature(attackable)
        self.n_turns += 1
        return True

    def go(self, draw=False):
        while maze.turn():
            if draw:
                maze.draw()


maze = Cavern(raw)
n_elves = len(maze.elves)

maze.go()

print(maze.outcome())

ap = 4
while True:
    maze = Cavern(raw, ap)
    maze.go()
    if n_elves == len(maze.elves):
        print(maze.outcome())
        break
    ap += 1
