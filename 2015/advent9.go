package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var distances = make(map[string]map[string]int)
var cities []string
var shortest int
var longest int

func route(i, n int) {
	if i == n {
		length := 0
		for i := 0; i < len(cities)-1; i++ {
			length += distances[cities[i]][cities[i+1]]
		}
		if length < shortest {
			shortest = length
		}
		if length > longest {
			longest = length
		}
	} else {
		for j := i; j <= n; j++ {
			cities[i], cities[j] = cities[j], cities[i]
			route(i+1, n)
			cities[i], cities[j] = cities[j], cities[i]
		}
	}
}

func cityInCities(city string) bool {
	for _, city2 := range cities {
		if city == city2 {
			return true
		}
	}
	return false
}

func main() {
	in := bufio.NewReader(os.Stdin)
	for n := 0; ; n++ {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			result := strings.Split(str[:len(str)-1], " = ")
			distance, _ := strconv.Atoi(result[1])
			result = strings.Split(result[0], " to ")
			from := result[0]
			to := result[1]
			if _, ok := distances[from]; !ok {
				distances[from] = make(map[string]int)
			}
			if _, ok := distances[to]; !ok {
				distances[to] = make(map[string]int)
			}
			distances[from][to] = distance
			distances[to][from] = distance
			if !cityInCities(from) {
				cities = append(cities, from)
			}
			if !cityInCities(to) {
				cities = append(cities, to)
			}
		}
	}
	shortest = 999999
	route(0, len(cities)-1)
	fmt.Println("Shortest: ", shortest)
	fmt.Println("Longest: ", longest)
}
