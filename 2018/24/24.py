import re

raw = open("input.txt").read().strip()

raw_example = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""


INFECTION = "Infection"
IMMUNE = "Immune"

ATTACKS = ("fire", "cold", "bludgeoning", "slashing", "radiation")


class Group:
    def __init__(self, name, army, line, boost):
        self.name = "group {}".format(name)
        self.army = army
        parts = re.search('^(?P<units>\d+) units each with '
                          '(?P<hit_points>\d+) hit points (?P<weak_immune>\([^\)]+\) )?'
                          'with an attack that does (?P<attack_power>\d+) '
                          '(?P<attack>\w+) damage at initiative (?P<initiative>\d+)$', line).groupdict()
        self.weak = self.immune = set()
        for label, value in parts.items():
            if label == 'weak_immune':
                if value:
                    for sub_part in value.strip("() ").split("; "):
                        setattr(self, sub_part.split(' ')[0], set(sub_part.split(" to ")[1].split(", ")))
            else:
                setattr(self, label, int(value) if value.isdigit() else value)
        self.attack_power += boost

    def damage_from(self, other):
        return other.damage_to(self)

    def damage_to(self, other):
        if self.attack in other.immune:
            damage = 0
        else:
            damage = self.effective_power
            if self.attack in other.weak:
                damage *= 2
        return damage

    @property
    def effective_power(self):
        return self.attack_power * self.units

    def __repr__(self):
        return "{} {}".format(self.army, self.name)


class Army:
    def __init__(self, name, boost):
        self.name = name
        self.boost = boost
        self.groups = []

    def add_group(self, line):
        self.groups.append(Group(len(self.groups) + 1, self, line, self.boost))

    def __repr__(self):
        return self.name.title()

    def target(self, other):
        other_groups = set(other.groups)
        for group in sorted(self.groups, key=lambda x: (-x.effective_power, -x.initiative)):
            group.target = None
            if other_groups:
                target = sorted(other_groups, key=lambda x: (-x.damage_from(group), -x.effective_power, -x.initiative))[0]
                if target.damage_from(group):
                    group.target = target
                    other_groups.remove(group.target)


class Battle:
    def __init__(self, raw, boost=0):
        self.boost = boost
        self._read(raw)

    def _read(self, raw):
        lines = raw.split("\n")
        while lines:
            line = lines.pop(0)
            if not line:
                continue
            if line[:len(IMMUNE)] == IMMUNE:
                current_army = self.immune_system = Army(IMMUNE, self.boost)
            elif line[:len(INFECTION)] == INFECTION:
                current_army = self.infection = Army(INFECTION, 0)
            else:
                current_army.add_group(line)

    def go(self):
        while True:
            self.immune_system.target(self.infection)
            self.infection.target(self.immune_system)
            deads_tot = 0
            for group in sorted(self.immune_system.groups + self.infection.groups, key=lambda x: -x.initiative):
                target = group.target
                if group.units > 0 and target:
                    damage = group.damage_to(target)
                    deads = damage // target.hit_points
                    target.units -= deads
                    deads_tot += deads
                    if target.units <= 0:
                        target.units = 0
                        target.army.groups.remove(target)
            if not self.immune_system.groups or deads_tot == 0:
                return self.infection
            elif not self.infection.groups:
                return self.immune_system


battle = Battle(raw)
# battle = Battle(raw_example)

winner = battle.go()
print(sum(group.units for group in winner.groups))

boost_low, boost_high = 0, 10000000
while True:
    if boost_high - boost_low < 2:
        break
    boost = (boost_high + boost_low) // 2
    battle = Battle(raw, boost)
    winner = battle.go()
    if winner.name == IMMUNE:
        boost_high = boost
    else:
        boost_low = boost

if winner.name == INFECTION:
    incr = 1
else:
    incr = -1

while True:
    boost += incr
    battle = Battle(raw, boost)
    next_winner = battle.go()
    if next_winner.name != winner.name:
        print(sum(group.units for group in (next_winner.groups if next_winner.name == IMMUNE else winner)))
        break
    winner = next_winner
