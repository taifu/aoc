package main

import (
	"bufio"
	"fmt"
	"os"
)

const RUNNING int = 0
const RESTING int = 1

func min(a, b int) int {
	if a > b {
		return b
	}
	return a
}

type Deer struct {
	name                 string
	km, seconds, resting int
}

func (deer Deer) Run(seconds int) int {
	run := 0
	state := RUNNING
	for seconds > 0 {
		switch state {
		case RUNNING:
			run += int(min(seconds, deer.seconds)) * deer.km
			seconds -= deer.seconds
			state = RESTING
		case RESTING:
			seconds -= deer.resting
			state = RUNNING
		}
	}
	return run
}

func BestScore(deers []Deer, seconds int) int {
	var states = make([]int, len(deers))
	var runs = make([]int, len(deers))
	var scores = make([]int, len(deers))
	for i := 0; i < len(deers); i++ {
		states[i] = deers[i].seconds
	}
	for ; seconds > 0; seconds-- {
		for i := 0; i < len(deers); i++ {
			if states[i] > 0 {
				runs[i] += deers[i].km
				states[i] -= 1
				if states[i] == 0 {
					states[i] = -deers[i].resting
				}
			} else if states[i] < 0 {
				states[i] += 1
				if states[i] == 0 {
					states[i] = deers[i].seconds
				}
			}
		}
		best_run := 0
		for i := 0; i < len(deers); i++ {
			if runs[i] > best_run {
				best_run = runs[i]
			}
		}
		for i := 0; i < len(deers); i++ {
			if runs[i] == best_run {
				scores[i] += 1
			}
		}
	}
	best_score := 0
	for i := 0; i < len(deers); i++ {
		if scores[i] > best_score {
			best_score = scores[i]
		}
	}
	return best_score
}

func main() {
	var name string
	var fly, seconds, resting int
	var deers []Deer
	best := 0
	after_seconds := 2503
	in := bufio.NewReader(os.Stdin)
	for {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			fmt.Sscanf(str, "%s can fly %d km/s for %d seconds, but then must rest for %d seconds\n",
				&name, &fly, &seconds, &resting)
			deer := Deer{name, fly, seconds, resting}
			deers = append(deers, deer)
			run := deer.Run(after_seconds)
			fmt.Printf("%s corre %d\n", deer.name, run)
			if run > best {
				best = run
			}
		}
	}
	fmt.Println("Migliore col primo punteggio:", best)
	fmt.Println("Migliore col secondo punteggio:", BestScore(deers, after_seconds))
}
