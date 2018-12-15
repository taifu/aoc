from collections import deque

raw = open("input.txt").read()

raw = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""


WALL, OPEN, ELF, GOBLIN = "#", ".", "E", "G"
DELTAS = ((0, -1), (-1, 0), (1, 0), (0, 1))


class Creature:
    def __init__(self, cavern, x, y, hp, ap, char):
        self.cavern = cavern
        self.x = x
        self.y = y
        self.hp = hp
        self.ap = ap
        self.char = char

    @property
    def dead(self):
        return self.hp < 0

    def __repr__(self):
        return "{}({})".format(self.char, self.hp)

    def __eq__(self, other):
        return other.char == self.char

    def __lt__(self, other):
        return other.y > self.y or other.x > self.x

    def attackable(self):
        attackables = []
        for x, y in [(self.x + dx, self.y + dy) for dx, dy in DELTAS]:
            creature = self.cavern.get_creature(x, y)
            if creature and creature != self:
                attackables.append(creature)
        if attackables:
            return sorted(attackables)[0]
        return None

    def move_nearest(self):
        explored = set(((self.x, self.y),))
        positions = deque(tuple((p, []) for p in explored))
        while positions:
            (x, y), path = positions.popleft()
            for n, (x, y) in enumerate([(x + dx, y + dy) for dx, dy in DELTAS]):
                if x >= 0 and x < self.cavern.width and y >= 0 and y < self.cavern.height and (x, y) not in explored and self.cavern.map[y][x] in (OPEN, GOBLIN, ELF):
                    next_path = path + [DELTAS[n]]
                    explored.add((x, y))
                    cell = self.cavern.map[y][x]
                    if cell == OPEN:
                        positions.append(((x, y), next_path))
                    elif cell in (ELF, GOBLIN):
                        if cell != self.char:
                            self.cavern.map[self.y][self.x] = OPEN
                            self.x += next_path[0][0]
                            self.y += next_path[0][1]
                            self.cavern.map[self.y][self.x] = self.char
                            return
        return


class Elf(Creature):
    def __init__(self, cavern, x, y, hp=200, ap=3):
        super().__init__(cavern=cavern, x=x, y=y, hp=hp, ap=ap, char=ELF)


class Goblin(Creature):
    def __init__(self, cavern, x, y, hp=200, ap=3):
        super().__init__(cavern=cavern, x=x, y=y, hp=hp, ap=ap, char=GOBLIN)


class Cavern:
    def __init__(self, raw):
        lines = raw.split("\n")
        self.elves = []
        self.goblins = []
        self.height = len(lines)
        self.width = len(lines[0])
        self.map = [list(line) for line in lines]
        self.n_turns = 0
        self._set()

    def remove_creature(self, creature):
        self.map[creature.y][creature.x] == OPEN
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

    def _set(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == ELF:
                    self.elves.append(Elf(self, x, y))
                elif self.map[y][x] == GOBLIN:
                    self.goblins.append(Goblin(self, x, y))

    def ended(self):
        return len(self.goblins) == 0 or len(self.elves) == 0

    def outcome(self):
        import pdb; pdb.set_trace()

    def turn(self):
        deads = []
        for creature in sorted(self.elves + self.goblins):
            if creature in deads:
                continue
            attackable = creature.attackable()
            if attackable:
                attackable.hp -= creature.ap
                if attackable.dead:
                    deads.append(attackable)
                    self.remove_creature(attackable)
            elif not creature.attackable():
                creature.move_nearest()
        self.n_turns += 1


maze = Cavern(raw)


while not maze.ended():
    maze.draw()
    maze.turn()

print(maze.outcome)
