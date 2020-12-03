class Spell:
    GET = []

    def __init__(self, name, mana_cost, timer, damage=0, add_armor=0, add_mana=0, healing=0):
        self.name = name
        self.mana_cost = mana_cost
        self.timer = timer
        self.damage = damage
        self.add_armor = add_armor
        self.healing = healing
        self.add_mana = add_mana
        self.GET.append(self)

    @staticmethod
    def reset():
        for spell in Spell.GET:
            spell.current_timer = 0

class Wizard:
    def __init__(self, hit, mana):
        self.name = "wizard"
        self.hit = hit
        self.mana = mana

    def reset(self):
        self.current_hit = self.hit
        self.current_mana = self.mana
        self.current_armor = 0

class Boss:
    def __init__(self, hit, damage):
        self.name = "boss"
        self.hit = hit
        self.damage = damage

    def reset(self):
        self.current_hit = self.hit

class Game:
    def __init__(self, wizard, boss):
        self.wizard = wizard
        self.boss = boss

    def reset(self):
        Spell.reset()
        self.wizard.reset()
        self.boss.reset()
        self.current_spells = []
        self.current_turn = 0
        self.winner = ""

    def manage_spells(self, turn_wizard):
        damage_boss = 0
        for spell in self.current_spells[:]:
            if spell.current_timer == 0:
                self.wizard.current_armor += spell.add_armor
            self.wizard.current_mana += spell.add_mana
            self.wizard.hit += spell.healing
            damage_boss += spell.damage
            spell.current_timer += 1
            if spell.current_timer == spell.timer:
                spell.current_timer = 0
                self.current_spells.remove(spell)
                self.wizard.current_armor -= spell.add_armor
        self.boss.current_hit -= damage_boss

    def turn_wizard(self, spell):
        self.current_turn += 1
        if spell.current_timer > 0 and spell.current_timer < spell.timer:
            raise Exception("Impossibile usare lo stesso spell più volte contemporaneamente")
        self.wizard.current_mana -= spell.mana_cost
        if self.wizard.current_mana < 0:
            raise Exception("Mana sottozero")
        self.manage_spells(turn_wizard=True)
        if spell.timer == 1:
            self.boss.current_hit -= spell.damage
            self.wizard.current_hit += spell.healing
        else:
            self.current_spells.append(spell)
        if self.boss.current_hit <= 0:
            self.winner = "wizard"

    def turn_boss(self):
        self.current_turn += 1
        self.manage_spells(turn_wizard=False)
        if self.boss.current_hit <= 0:
            self.winner = "wizard"
        else:
            self.wizard.current_hit -= max(1, self.boss.damage - self.wizard.current_armor)
            if self.wizard.current_hit <= 0:
                self.winner = "boss"

MAGIC_MISSILE = Spell("magic missile", mana_cost=53, timer=1, damage=4)
DRAIN = Spell("drain", mana_cost=73, timer=1, damage=2, healing=2)
SHIELD = Spell("shield", mana_cost=113, timer=6, add_armor=7)
POISON = Spell("poison", mana_cost=173, timer=6, damage=3)
RECHARGE = Spell("recharge", mana_cost=229, timer=5, add_mana=101)

def test_game1():
    wizard = Wizard(10, 250)
    boss = Boss(13, 8)
    game = Game(wizard, boss)
    game.reset()
    game.turn_wizard(POISON)
    if wizard.current_hit != 10:
        print("Dopo un turno il giocatore deve avere 10 hit point")
    if wizard.current_mana != 77:
        print("Dopo un turno il giocatore deve avere 77 di mana")
    if boss.current_hit != 13:
        print("Dopo un turno il boss deve avere 10 hit point")
    game.turn_boss()
    if boss.current_hit != 10:
        print("Dopo 2 turni il boss deve avere 10 hit point")
    game.turn_wizard(MAGIC_MISSILE)
    if wizard.current_hit != 2:
        print("Dopo 3 turni il giocatore deve avere 2 hit point")
    if wizard.current_mana != 24:
        print("Dopo 3 turni il giocatore deve avere 24 di mana")
    if boss.current_hit != 3:
        print("Dopo 3 turni il boss deve avere 3 hit point")
    game.turn_boss()
    if game.winner != "wizard":
        print("Dopo 4 turni deve vincere il wizard")
    if boss.current_hit != 0:
        print("Dopo 4 turni il boss deve avere 0 hit point")

def test_game2():
    wizard = Wizard(10, 250)
    boss = Boss(14, 8)
    game = Game(wizard, boss)
    game.reset()
    game.turn_wizard(RECHARGE)
    if wizard.current_hit != 10:
        print("Dopo un turno il giocatore deve avere 10 hit point")
    if wizard.current_mana != 21:
        print("Dopo un turno il giocatore deve avere 21 di mana")
    if boss.current_hit != 14:
        print("Dopo un turno il boss deve avere 14 hit point")
    game.turn_boss()
    if boss.current_hit != 14:
        print("Dopo 2 turni il boss deve avere 14 hit point")
    if wizard.current_mana != 122:
        print("Dopo 2 turni il giocatore deve avere 122 di mana")
    game.turn_wizard(SHIELD)
    if wizard.current_hit != 2:
        print("Dopo 3 turni il giocatore deve avere 2 hit point")
    if wizard.current_mana != 110:
        print("Dopo 3 turni il giocatore deve avere 24 di mana")
    if boss.current_hit != 14:
        print("Dopo 3 turni il boss deve avere 14 hit point")
    game.turn_boss()
    if wizard.current_hit != 1:
        print("Dopo 4 turni il giocatore deve avere 1 hit point")
    if wizard.current_mana != 211:
        print("Dopo 4 turni il giocatore deve avere 211 di mana")
    game.turn_wizard(DRAIN)
    if wizard.current_mana != 239:
        print("Dopo 5 turni il giocatore deve avere 239 di mana")
    if wizard.current_hit != 3:
        print("Dopo 5 turni il giocatore deve avere 3 hit point")
    game.turn_boss()
    if wizard.current_hit != 2:
        print("Dopo 6 turni il giocatore deve avere 2 hit point")
    if wizard.current_mana != 340:
        print("Dopo 6 turni il giocatore deve avere 340 di mana")
    game.turn_wizard(POISON)
    if wizard.current_hit != 2:
        print("Dopo 7 turni il giocatore deve avere 2 hit point")
    if wizard.current_mana != 167:
        print("Dopo 7 turni il giocatore deve avere 167 di mana")
    game.turn_boss()
    if wizard.current_hit != 1:
        print("Dopo 8 turni il giocatore deve avere 1 hit point")
    if wizard.current_mana != 167:
        print("Dopo 8 turni il giocatore deve avere 167 di mana")
    game.turn_wizard(MAGIC_MISSILE)
    if game.winner != "":
        print("Non ci deve essere un vincitore")
    game.turn_boss()
    if game.winner != "wizard":
        print("Dopo tot turni deve vincere il wizard")
    if wizard.current_hit != 1:
        print("Dopo tot turni il giocatore deve avere 1 hit point")
    if wizard.current_mana != 114:
        print("Dopo tot turni il giocatore deve avere 114 di mana")
    if boss.current_hit != -1:
        print("Dopo tot turni il boss deve avere -1 hit point")

def test():
    test_game1()
    test_game2()

if __name__ == "__main__":
    import sys
    if "-t" in sys.argv:
        test()
    else:
        # Questo va (226 poison + magic missile)
        wizard = Wizard(10, 250)
        boss = Boss(13, 8)

        # Questo va 641 magic missile ['recharge', 'shield', 'drain', 'poison']
        wizard = Wizard(10, 250)
        boss = Boss(14, 8)

        wizard = Wizard(50, 500)
        boss = Boss(58, 9)

        game = Game(wizard, boss)
        min_mana = 99999999

        def manage(game, spell, others):
            global min_mana
            if wizard.current_mana < spell.mana_cost:
                return "c"
            game.turn_wizard(spell)
            r = ""
            if game.winner:
                r = "c"
            else:
                game.turn_boss()
                if game.winner:
                    r = "c"
            if r == "c":
                if game.winner == "wizard":
                    mana_spent = spell.mana_cost + sum(s.mana_cost for s in others)
                    if mana_spent < min_mana:
                        min_mana = mana_spent
                    print(min_mana, spell.name, [s.name for s in others])
                game.reset()
                for s in others:
                    x = manage(game, s, [])
                    assert x == ""
            return r

        # 1269 ['P', 'R', 'D', 'P', 'R', 'S', 'P', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M']

        for s0 in Spell.GET:
            print(s0.name)
            game.reset()
            if manage(game, s0, []):
                break
            print("t0", s0.name, wizard.current_mana)
            for s1 in Spell.GET:
                print("  t1", s0.name, s1.name, wizard.current_mana)
                print("  ", s1.name)
                if s1.current_timer > 0:
                    continue
                r = manage(game, s1, [s0])
                if r == "c":
                    continue
                if r == "b":
                    break
                for s2 in Spell.GET:
                    print("    ", s2.name)
                    if s2.current_timer > 0:
                        continue
                    r = manage(game, s2, [s0, s1])
                    if r == "c":
                        continue
                    if r == "b":
                        break
                    for s3 in Spell.GET:
                        print("      ", s3.name)
                        if s3.current_timer > 0:
                            continue
                        r = manage(game, s3, [s0, s1, s2])
                        if r == "c":
                            continue
                        if r == "b":
                            break
                        for s4 in Spell.GET:
                            print("        ", s4.name)
                            if s4.current_timer > 0:
                                continue
                            r = manage(game, s4, [s0, s1, s2, s3])
                            if r == "c":
                                continue
                            if r == "b":
                                break
                            for s5 in Spell.GET:
                                print("          ", s4.name)
                                if s5.current_timer > 0:
                                    continue
                                r = manage(game, s5, [s0, s1, s2, s3, s4])
                                if r == "c":
                                    continue
                                if r == "b":
                                    break
                                for s6 in Spell.GET:
                                    if s6.current_timer > 0:
                                        continue
                                    r = manage(game, s6, [s0, s1, s2, s3, s4, s5])
                                    if r == "c":
                                        continue
                                    if r == "b":
                                        break
                                    for s7 in Spell.GET:
                                        if s7.current_timer > 0:
                                            continue
                                        r = manage(game, s7, [s0, s1, s2, s3, s4, s5, s6])
                                        if r == "c":
                                            continue
                                        if r == "b":
                                            break
                                        for s8 in Spell.GET:
                                            if s8.current_timer > 0:
                                                continue
                                            r = manage(game, s8, [s0, s1, s2, s3, s4, s5, s6, s7])
                                            if r == "c":
                                                continue
                                            if r == "b":
                                                break
                                            for s9 in Spell.GET:
                                                if s9.current_timer > 0:
                                                    continue
                                                r = manage(game, s9, [s0, s1, s2, s3, s4, s5, s6, s7, s8])
                                                if r == "c":
                                                    continue
                                                if r == "b":
                                                    break
                                                for s10 in Spell.GET:
                                                    if s10.current_timer > 0:
                                                        continue
                                                    r = manage(game, s10, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9])
                                                    if r == "c":
                                                        continue
                                                    if r == "b":
                                                        break
                                                    for s11 in Spell.GET:
                                                        if s11.current_timer > 0:
                                                            continue
                                                        r = manage(game, s11, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])
                                                        if r == "c":
                                                            continue
                                                        if r == "b":
                                                            break
                                                        for s12 in Spell.GET:
                                                            if s12.current_timer > 0:
                                                                continue
                                                            r = manage(game, s12, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11])
                                                            if r == "c":
                                                                continue
                                                            if r == "b":
                                                                break
                                                            for s13 in Spell.GET:
                                                                if s13.current_timer > 0:
                                                                    continue
                                                                r = manage(game, s13, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12])
                                                                if r == "c":
                                                                    continue
                                                                if r == "b":
                                                                    break
                                                                for s14 in Spell.GET:
                                                                    if s14.current_timer > 0:
                                                                        continue
                                                                    r = manage(game, s14, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13])
                                                                    if r == "c":
                                                                        continue
                                                                    if r == "b":
                                                                        break
                                                                    for s15 in Spell.GET:
                                                                        if s15.current_timer > 0:
                                                                            continue
                                                                        r = manage(game, s15, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14])
                                                                        if r == "c":
                                                                            continue
                                                                        if r == "b":
                                                                            break
                                                                        for s16 in Spell.GET:
                                                                            if s16.current_timer > 0:
                                                                                continue
                                                                            r = manage(game, s16, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15])
                                                                            if r == "c":
                                                                                continue
                                                                            if r == "b":
                                                                                break
                                                                            for s17 in Spell.GET:
                                                                                if s17.current_timer > 0:
                                                                                    continue
                                                                                r = manage(game, s17, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16])
                                                                                if r == "c":
                                                                                    continue
                                                                                if r == "b":
                                                                                    break
                                                                                for s18 in Spell.GET:
                                                                                    if s18.current_timer > 0:
                                                                                        continue
                                                                                    r = manage(game, s18, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17])
                                                                                    if r == "c":
                                                                                        continue
                                                                                    if r == "b":
                                                                                        break
                                                                                    for s19 in Spell.GET:
                                                                                        if s19.current_timer > 0:
                                                                                            continue
                                                                                        r = manage(game, s19, [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18])
                                                                                        if r == "c":
                                                                                            continue
                                                                                        if r == "b":
                                                                                            break
