package main

import (
	"bufio"
	"fmt"
	"os"
)

var happiest int
var saddest int
var happiness = make(map[string]map[string]int)
var people []string

func route(i, n int) {
	if i == n {
		happy := happiness[people[0]][people[len(people)-1]]
		happy += happiness[people[len(people)-1]][people[0]]
		for i := 1; i < len(people); i++ {
			happy += happiness[people[i-1]][people[i]]
			happy += happiness[people[i]][people[i-1]]
		}
		if happy < saddest {
			saddest = happy
		}
		if happy > happiest {
			happiest = happy
		}
	} else {
		for j := i; j <= n; j++ {
			people[i], people[j] = people[j], people[i]
			route(i+1, n)
			people[i], people[j] = people[j], people[i]
		}
	}
}

func personInPeople(person string) bool {
	for _, person2 := range people {
		if person == person2 {
			return true
		}
	}
	return false
}

func main() {
	in := bufio.NewReader(os.Stdin)
	for {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			var who, whom, lose_gain string
			var units int
			fmt.Sscanf(str, "%s would %s %d happiness units by sitting next to %s.\n", &who, &lose_gain, &units, &whom)
			whom = whom[:len(whom)-1]
			if lose_gain == "lose" {
				units = -units
			}
			if _, ok := happiness[who]; !ok {
				happiness[who] = make(map[string]int)
			}
			if !personInPeople(whom) {
				people = append(people, whom)
			}
			happiness[who][whom] = units
		}
	}
	happiest = 0
	saddest = 0
	route(0, len(happiness)-1)
	fmt.Println(happiest)
	//fmt.Println(saddest)
}
