package main

import (
	"fmt"
)

var cities = []string{"A", "B", "C", "D"}

func route(i, n int) {
	if i == n {
		fmt.Println(cities)
	} else {
		for j := i; j <= n; j++ {
			cities[i], cities[j] = cities[j], cities[i]
			route(i+1, n)
			cities[i], cities[j] = cities[j], cities[i]
		}
	}
}

func main() {
	route(0, len(cities)-1)
}
