package main

import (
	"testing"
)

func TestHit(t *testing.T) {
	var player = NewPlayer("player", 8, 5, 5)
	player.Reset()
	player.Hit(31)
	if player.current_hit != -23 {
		t.Fatalf("Current hit deve essere -23", player)
	}
}

func TestHitGame(t *testing.T) {
	var player = NewPlayer("player", 8, 5, 5)
	var boss = NewPlayer("boss", 12, 7, 2)
	var game = Game{player, boss}
	game.player1.Reset()
	game.player1.Hit(21)
	if game.player1.current_hit != -13 {
		t.Fatalf("Current hit deve essere -13", player)
	}
	if player.current_hit != -13 {
		t.Fatalf("Current hit deve essere -13", player)
	}
}

func TestGame(t *testing.T) {
	var player = NewPlayer("player", 8, 5, 5)
	var boss = NewPlayer("boss", 12, 7, 2)
	var game = Game{player, boss}

	winner := game.Run()
	if winner.name != player.name {
		t.Fatalf("Il vincitore deve essere ", player)
	}
	if game.player2.IsAlive() {
		t.Fatalf("Il boss deve essere morto")
	}
	if !game.player1.IsAlive() {
		t.Fatalf("Il player deve essere vivo")
	}
	if game.player1.Health() != 2 {
		t.Fatalf("Il player deve avere 2 hit rimasti")
	}
	game.Run()
	if game.player1.Health() != 2 {
		t.Fatalf("Dopo un ulteriore run il player deve ancora avere 2 hit rimasti")
	}
}

func TestGameWithItem(t *testing.T) {
	var player = NewPlayer("player", 8, 1, 5)
	var boss = NewPlayer("boss", 12, 7, 0)
	var game = Game{player, boss}

	player.AddItem(GetItem(weapons, "Dagger"))
	boss.AddItem(GetItem(armors, "Chainmail"))
	winner := game.Run()
	if winner.name != player.name {
		t.Fatalf("Il vincitore deve essere ", player)
	}
	if game.player2.IsAlive() {
		t.Fatalf("Il boss deve essere morto")
	}
	if !game.player1.IsAlive() {
		t.Fatalf("Il player deve essere vivo")
	}
	if game.player1.Health() != 2 {
		t.Fatalf("Il player deve avere 2 hit rimasti")
	}
	game.Run()
	if game.player1.Health() != 2 {
		t.Fatalf("Dopo un ulteriore run il player deve ancora avere 2 hit rimasti")
	}
}
