package main

import (
	"fmt"
)

type Item struct {
	name   string
	cost   int
	damage int
	armor  int
}

type Player struct {
	name        string
	hit         int
	damage      int
	armor       int
	current_hit int
	gold_spent  int
	items       []Item
}

func (player *Player) Reset() {
	player.current_hit = player.hit
}

func (player *Player) Hit(damage int) {
	player.current_hit -= damage
}

func (player Player) Health() int {
	return player.current_hit
}

func (player *Player) AddItem(item Item) {
	player.items = append(player.items, item)
	player.gold_spent += item.cost
}

func (player *Player) DeleteItem(item Item) {
	for n := 0; n < len(player.items); n++ {
		if player.items[n].name == item.name {
			player.items = append(player.items[:n], player.items[n+1:]...)
			player.gold_spent -= item.cost
		}
	}
}

func NewPlayer(name string, hit, damage, armor int) *Player {
	return &Player{name, hit, damage, armor, 0, 0, nil}
}

func (player Player) IsAlive() bool {
	return player.Health() > 0
}

type Game struct {
	player1, player2 *Player
}

func (game Game) GetDamage(player1, player2 *Player) (damage int) {
	damage = player1.damage - player2.armor
	for n := 0; n < len(player1.items); n++ {
		damage += player1.items[n].damage
	}
	for n := 0; n < len(player2.items); n++ {
		damage -= player2.items[n].armor
	}
	if damage < 1 {
		damage = 1
	}
	return
}

func (game Game) Reset() {
	game.player1.Reset()
	game.player2.Reset()
}

func (game Game) Run() *Player {
	game.Reset()
	for game.player1.IsAlive() && game.player2.IsAlive() {
		game.player2.Hit(game.GetDamage(game.player1, game.player2))
		if game.player2.IsAlive() {
			game.player1.Hit(game.GetDamage(game.player2, game.player1))
		}
	}
	if game.player1.IsAlive() {
		return game.player1
	}
	return game.player2
}

func GetItem(items []Item, name string) (item Item) {
	for n := 0; n < len(items); n++ {
		if items[n].name == name {
			item = items[n]
		}
	}
	return
}

// Exactly 1
var weapons = []Item{
	{"Dagger", 8, 4, 0},
	{"Shortsword", 10, 5, 0},
	{"Warhammer", 25, 6, 0},
	{"Longsword", 40, 7, 0},
	{"Greataxe", 74, 8, 0},
}

// 0 or 1
var armors = []Item{
	{"Leather", 13, 0, 1},
	{"Chainmail", 31, 0, 2},
	{"Splintmail", 53, 0, 3},
	{"Bandedmail", 75, 0, 4},
	{"Platemail", 102, 0, 5},
}

// 0 or 1 or 2
var rings = []Item{
	{"Damage +1", 25, 1, 0},
	{"Damage +2", 50, 2, 0},
	{"Damage +3", 100, 3, 0},
	{"Defense +1", 20, 0, 1},
	{"Defense +2", 40, 0, 2},
	{"Defense +3", 80, 0, 3},
}

var min_gold = 99999999999
var max_gold = 0

func (game Game) CheckGold() {
	winner := game.Run()
	if winner.name == game.player1.name {
		if winner.gold_spent < min_gold {
			min_gold = winner.gold_spent
		}
	} else {
		if game.player1.gold_spent > max_gold {
			max_gold = game.player1.gold_spent
		}
	}
}

func main() {
	var player = NewPlayer("player", 100, 0, 0)
	var boss = NewPlayer("boss", 100, 8, 2)
	var game = Game{player, boss}
	for n_weapon := 0; n_weapon < len(weapons); n_weapon++ {
		player.AddItem(weapons[n_weapon])
		game.CheckGold()
		for n_armor := -1; n_armor < len(armors); n_armor++ {
			if n_armor >= 0 {
				player.AddItem(armors[n_armor])
			}
			game.CheckGold()
			for n_ring1 := 0; n_ring1 < len(rings); n_ring1++ {
				player.AddItem(rings[n_ring1])
				game.CheckGold()
				for n_ring2 := n_ring1 + 1; n_ring2 < len(rings); n_ring2++ {
					player.AddItem(rings[n_ring2])
					game.CheckGold()
					player.DeleteItem(rings[n_ring2])
				}
				player.DeleteItem(rings[n_ring1])
			}
			if n_armor >= 0 {
				player.DeleteItem(armors[n_armor])
			}
		}
		player.DeleteItem(weapons[n_weapon])
	}
	fmt.Println(min_gold)
	fmt.Println(max_gold)
}
