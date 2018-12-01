package main

import (
	"fmt"
	"testing"
)

func TestGame1(t *testing.T) {
	wizard := NewWizard(10, 250)
	boss := NewBoss(13, 8)
	game := NewGame(wizard, boss)
	game.Reset()
	game.TurnWizard(GetSpell("Poison"))
	if wizard.current_hit != 10 {
		t.Fatalf("Dopo un turno il giocatore deve avere 10 hit point")
	}
	if wizard.current_mana != 77 {
		t.Fatalf("Dopo un turno il giocatore deve avere 77 di mana")
	}
	if boss.current_hit != 13 {
		t.Fatalf("Dopo un turno il boss deve avere 10 hit point")
	}
	game.TurnBoss()
	if boss.current_hit != 10 {
		t.Fatalf("Dopo 2 turni il boss deve avere 10 hit point")
	}
	game.TurnWizard(GetSpell("Magic Missile"))
	if wizard.current_hit != 2 {
		t.Fatalf("Dopo 3 turni il giocatore deve avere 2 hit point")
	}
	if wizard.current_mana != 24 {
		t.Fatalf("Dopo 3 turni il giocatore deve avere 24 di mana")
	}
	if boss.current_hit != 3 {
		t.Fatalf("Dopo 3 turni il boss deve avere 3 hit point")
	}
	game.TurnBoss()
	if game.winner != "wizard" {
		t.Fatalf("Dopo 4 turni deve vincere il wizard")
	}
	if boss.current_hit != 0 {
		t.Fatalf("Dopo 4 turni il boss deve avere 0 hit point")
	}
}

func TestGame2(t *testing.T) {
	wizard := NewWizard(10, 250)
	boss := NewBoss(14, 8)
	game := NewGame(wizard, boss)
	game.Reset()
	game.TurnWizard(GetSpell("Recharge"))
	if wizard.current_hit != 10 {
		t.Fatalf("Dopo un turno il giocatore deve avere 10 hit point")
	}
	if wizard.current_mana != 21 {
		t.Fatalf("Dopo un turno il giocatore deve avere 21 di mana")
	}
	if boss.current_hit != 14 {
		t.Fatalf("Dopo un turno il boss deve avere 14 hit point")
	}
	game.TurnBoss()
	if boss.current_hit != 14 {
		t.Fatalf("Dopo 2 turni il boss deve avere 14 hit point")
	}
	if wizard.current_mana != 122 {
		t.Fatalf("Dopo 2 turni il giocatore deve avere 122 di mana")
	}
	game.TurnWizard(GetSpell("Shield"))
	if wizard.current_hit != 2 {
		t.Fatalf("Dopo 3 turni il giocatore deve avere 2 hit point")
	}
	if wizard.current_mana != 110 {
		t.Fatalf("Dopo 3 turni il giocatore deve avere 24 di mana")
	}
	if boss.current_hit != 14 {
		t.Fatalf("Dopo 3 turni il boss deve avere 14 hit point")
	}
	game.TurnBoss()
	if wizard.current_hit != 1 {
		t.Fatalf("Dopo 4 turni il giocatore deve avere 1 hit point")
	}
	if wizard.current_mana != 211 {
		t.Fatalf("Dopo 4 turni il giocatore deve avere 211 di mana")
	}
	game.TurnWizard(GetSpell("Drain"))
	if wizard.current_mana != 239 {
		t.Fatalf("Dopo 5 turni il giocatore deve avere 239 di mana")
	}
	if wizard.current_hit != 3 {
		t.Fatalf("Dopo 5 turni il giocatore deve avere 3 hit point")
	}
	game.TurnBoss()
	if wizard.current_hit != 2 {
		t.Fatalf("Dopo 6 turni il giocatore deve avere 2 hit point")
	}
	if wizard.current_mana != 340 {
		t.Fatalf("Dopo 6 turni il giocatore deve avere 340 di mana")
	}
	game.TurnWizard(GetSpell("Poison"))
	if wizard.current_hit != 2 {
		t.Fatalf("Dopo 7 turni il giocatore deve avere 2 hit point")
	}
	if wizard.current_mana != 167 {
		t.Fatalf("Dopo 7 turni il giocatore deve avere 167 di mana")
	}
	game.TurnBoss()
	if wizard.current_hit != 1 {
		t.Fatalf("Dopo 8 turni il giocatore deve avere 1 hit point")
	}
	if wizard.current_mana != 167 {
		t.Fatalf("Dopo 8 turni il giocatore deve avere 167 di mana")
	}
	game.TurnWizard(GetSpell("Magic Missile"))
	if game.winner != "" {
		t.Fatalf("Non ci deve essere un vincitore")
	}
	game.TurnBoss()
	if game.winner != "wizard" {
		t.Fatalf("Dopo tot turni deve vincere il wizard")
	}
	if wizard.current_hit != 1 {
		t.Fatalf("Dopo tot turni il giocatore deve avere 1 hit point")
	}
	if wizard.current_mana != 114 {
		t.Fatalf("Dopo tot turni il giocatore deve avere 114 di mana")
	}
	if boss.current_hit != -1 {
		t.Fatalf("Dopo tot turni il boss deve avere -1 hit point")
	}
}

func TestGame3(t *testing.T) {
	wizard := NewWizard(50, 500)
	boss := NewBoss(58, 9)
	game := NewGame(wizard, boss)
	game.Reset()
	game.TurnWizard(GetSpell("Recharge"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnWizard(GetSpell("Shield"))
	game.TurnBoss()
	game.TurnWizard(GetSpell("Magic Missile"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	game.TurnWizard(GetSpell("Poison"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	game.TurnWizard(GetSpell("Recharge"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	game.TurnWizard(GetSpell("Magic Missile"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	game.TurnWizard(GetSpell("Magic Missile"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	game.TurnWizard(GetSpell("Poison"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	game.TurnWizard(GetSpell("Magic Missile"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	game.TurnWizard(GetSpell("Magic Missile"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
	game.TurnWizard(GetSpell("Magic Missile"))
	fmt.Println("wizard hit", wizard.current_hit, "mana", wizard.current_mana)
	game.TurnBoss()
}
