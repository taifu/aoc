package main

import "testing"

func TestComet(t *testing.T) {
	deer := Deer{"Comet", 14, 10, 127}
	run := deer.Run(1000)
	run_ok := 1120
	if run != run_ok {
		t.Fatalf("%s deve correre %d invece che %d", deer.name, run_ok, run)
	}
}

func TestDancer(t *testing.T) {
	deer := Deer{"Dancer", 16, 11, 162}
	run := deer.Run(1000)
	run_ok := 1056
	if run != run_ok {
		t.Fatalf("%s deve correre %d invece che %d", deer.name, run_ok, run)
	}
}

func TestBoth(t *testing.T) {
	deer1 := Deer{"Comet", 14, 10, 127}
	deer2 := Deer{"Dancer", 16, 11, 162}
	deers := []Deer{deer1, deer2}
	score := BestScore(deers, 1000)
	score_ok := 689
	if score != score_ok {
		t.Fatalf("Il migliore deve aver preso %d punti invece che %d", score_ok, score)
	}
}
