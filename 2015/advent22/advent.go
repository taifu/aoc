package main

import (
	"fmt"
	"math/rand"
)

type Wizard struct {
	hit           int
	mana          int
	armor         int
	current_armor int
	current_hit   int
	current_mana  int
}

func (wizard *Wizard) Reset() {
	wizard.current_hit = wizard.hit
	wizard.current_mana = wizard.mana
	wizard.current_armor = wizard.armor
}

func NewWizard(hit, mana int) *Wizard {
	return &Wizard{hit, mana, 0, 0, 0, 0}
}

type Boss struct {
	hit         int
	damage      int
	current_hit int
}

func (boss *Boss) Reset() {
	boss.current_hit = boss.hit
}

func NewBoss(hit, damage int) *Boss {
	return &Boss{hit, damage, 0}
}

type Game struct {
	wizard         *Wizard
	boss           *Boss
	current_turn   int
	current_spells []*Spell
	winner         string
}

func (game *Game) Reset() {
	game.wizard.Reset()
	game.boss.Reset()
	ResetSpells()
	game.current_spells = []*Spell{}
	game.current_turn = 0
	game.winner = ""
}

func (game *Game) TurnWizard(new_spell *Spell) {
	if new_spell.current_timer > 0 {
		panic("Impossibile usare lo stesso spell più volte nello stesso tempo")
	}
	//fmt.Println("======================")
	//fmt.Println("Spells")
	for n := 0; n < len(game.current_spells); n++ {
		//fmt.Println("  ", game.current_spells[n].name, game.current_spells[n].current_timer)
	}
	//fmt.Println("Casting ", new_spell.name)
	//fmt.Println("Shield.current_timer", GetSpell("Shield").current_timer)
	game.current_turn += 1
	damage_to_boss := 0
	// Spells
	for n := len(game.current_spells) - 1; n >= 0; n-- {
		//spell :=
		//fmt.Println(game.current_spells[n].name, game.current_spells[n].current_timer)
		damage_to_boss += game.current_spells[n].damage
		game.wizard.current_mana += game.current_spells[n].add_mana
		game.current_spells[n].current_timer -= 1
		if game.current_spells[n].current_timer == 0 {
			//fmt.Println("armor_to_remove", game.current_spells[n].add_armor, game.current_spells[n].name)
			game.wizard.current_armor -= game.current_spells[n].add_armor
			game.current_spells = append(game.current_spells[:n], game.current_spells[n+1:]...)
		}
	}
	// Current spell
	if new_spell.timer == 1 {
		game.wizard.current_hit += new_spell.add_hit
		damage_to_boss += new_spell.instant_damage
	} else {
		game.current_spells = append(game.current_spells, new_spell)
		new_spell.current_timer = new_spell.timer
		game.wizard.current_armor += new_spell.add_armor
		//fmt.Println("armor_to_add", new_spell.add_armor)
	}
	//fmt.Println("Spells after")
	for n := 0; n < len(game.current_spells); n++ {
		//fmt.Println("  ", game.current_spells[n].name, game.current_spells[n].current_timer)
	}
	game.wizard.current_mana -= new_spell.mana_cost
	game.boss.current_hit -= damage_to_boss
	if game.wizard.current_mana < 0 {
		game.winner = "boss"
	} else if game.boss.current_hit <= 0 {
		game.winner = "wizard"
	}
	//fmt.Println("Turno", game.current_turn)
	//fmt.Println(game.wizard)
	//fmt.Println(game.boss)
}

func (game *Game) TurnBoss() {
	game.current_turn += 1
	damage_to_boss := 0
	damage_to_wizard := game.boss.damage - game.wizard.armor
	armor_to_remove := 0
	for n := len(game.current_spells) - 1; n >= 0; n-- {
		//fmt.Println(game.current_spells[n].name, game.current_spells[n].current_timer)
		damage_to_boss += game.current_spells[n].damage
		game.wizard.current_hit += game.current_spells[n].add_hit
		game.wizard.current_mana += game.current_spells[n].add_mana
		game.current_spells[n].current_timer -= 1
		if game.current_spells[n].current_timer == 0 {
			armor_to_remove = game.current_spells[n].add_armor
			//fmt.Println("armor_to_remove", armor_to_remove, game.current_spells[n].name)
			game.current_spells = append(game.current_spells[:n], game.current_spells[n+1:]...)
		}
	}
	//fmt.Println("Spells after boss")
	for n := 0; n < len(game.current_spells); n++ {
		//fmt.Println("  ", game.current_spells[n].name, game.current_spells[n].current_timer)
	}
	//fmt.Println("Spells after boss")
	damage_to_wizard -= game.wizard.current_armor
	game.wizard.current_armor -= armor_to_remove
	if damage_to_wizard < 1 {
		damage_to_wizard = 1
	}
	//fmt.Println("Turno", game.current_turn, damage_to_wizard, game.wizard.current_armor)
	//fmt.Println("to boss", damage_to_boss)
	game.boss.current_hit -= damage_to_boss
	//fmt.Println(game.boss)
	if game.boss.current_hit > 0 {
		game.wizard.current_hit -= damage_to_wizard
		if game.wizard.current_hit <= 0 {
			game.winner = "boss"
		}
	} else {
		game.winner = "wizard"
	}
	//fmt.Println("Turno", game.current_turn)
	//fmt.Println(game.wizard)
	//fmt.Println(game.boss)
}

func NewGame(wizard *Wizard, boss *Boss) *Game {
	return &Game{wizard, boss, 0, []*Spell{}, ""}
}

type Spell struct {
	name           string
	mana_cost      int
	damage         int
	add_armor      int
	timer          int
	add_hit        int
	add_mana       int
	current_timer  int
	instant_damage int
}

func (spell *Spell) Reset() {
	spell.current_timer = 0
}

var spells = []*Spell{
	&Spell{"Magic Missile", 53, 0, 0, 1, 0, 0, 0, 4},
	&Spell{"Drain", 73, 0, 0, 1, 2, 0, 0, 2},
	&Spell{"Shield", 113, 0, 7, 6, 0, 0, 0, 0},
	&Spell{"Poison", 173, 3, 0, 6, 0, 0, 0, 0},
	&Spell{"Recharge", 229, 0, 0, 5, 0, 101, 0, 0},
}

func GetSpell(name string) *Spell {
	for n := 0; n < len(spells); n++ {
		if spells[n].name == name {
			return spells[n]
		}
	}
	panic("Spell not found")
}

func ResetSpells() {
	for n := 0; n < len(spells); n++ {
		spells[n].Reset()
	}
}

func main() {
	wizard := NewWizard(50, 500)
	boss := NewBoss(58, 9)
	game := NewGame(wizard, boss)
	min_mana := 99999999
	for {
		mana_spent := 0
		spells_used := []*Spell{}
		game.Reset()
		for game.winner == "" {
			spell := spells[0]
			for {
				spell = spells[rand.Intn(len(spells))]
				if spell.current_timer == 0 {
					break
				}
			}
			spells_used = append(spells_used, spell)
			mana_spent += spell.mana_cost
			game.TurnWizard(spell)
			if game.winner != "" {
				break
			}
			game.TurnBoss()
		}
		if game.winner == "wizard" && mana_spent < min_mana {
			min_mana = mana_spent
			fmt.Println("===========")
			fmt.Println(min_mana)
			mana := 0
			for n := 0; n < len(spells_used); n++ {
				fmt.Println(spells_used[n])
				mana += spells_used[n].mana_cost
			}
			fmt.Println(mana)
		}
	}
	fmt.Println(min_mana)
}
