package main

import (
	"reflect"
	"testing"
)

// Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
// Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

var ingredients = []Ingredient{
	Ingredient{"butterscotch", -1, -2, 6, 3, 8},
	Ingredient{"Cinnamon", 2, 3, -2, -1, 3}}

func TestBest(t *testing.T) {
	best_ok := 62842880
	best := BestCookie(ingredients, 100)
	if best != best_ok {
		t.Fatalf("Il meglio di %s deve essere %d invece che %d", ingredients, best_ok, best)
	}
}

func TestCalc(t *testing.T) {
	calc := CalcCookie(ingredients, []int{44, 56})
	calc_ok := 62842880
	if calc != calc_ok {
		t.Fatalf("Il calcolo di %s deve essere %d invece che %d", ingredients, calc_ok, calc)
	}
}

func TestCounter(t *testing.T) {
	var it_next_ok []int
	it := NewIntStatefulIterator(3, 3)
	it_next_ok = []int{0, 0, 3}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{0, 1, 2}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{0, 2, 1}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{0, 3, 0}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{1, 0, 2}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{1, 1, 1}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{1, 2, 0}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{2, 0, 1}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{2, 1, 0}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	it.Next()
	it_next_ok = []int{3, 0, 0}
	if !reflect.DeepEqual(it.Counters(), it_next_ok) {
		t.Fatalf("Error in it.Next ", it.Counters(), it_next_ok)
	}
	if it.Next() {
		t.Fatalf("Error in it.Next: non termina")
	}
}
