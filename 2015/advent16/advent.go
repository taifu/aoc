package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func stringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func FindSue(sues map[string]map[string]int, features map[string]int, greater []string, fewer []string) {
	var sues_ok []string
	var sues_ok2 []string
	for sue, values := range sues {
		sue_ok := true
		sue_ok2 := true
		for feature, quantity := range features {
			value, ok := values[feature]
			if ok {
				if value != quantity {
					sue_ok = false
				}
				if stringInSlice(feature, greater) {
					if value <= quantity {
						sue_ok2 = false
					}
				} else if stringInSlice(feature, fewer) {
					if value >= quantity {
						sue_ok2 = false
					}
				} else if value != quantity {
					sue_ok2 = false
				}
			}
		}
		if sue_ok {
			sues_ok = append(sues_ok, sue)
		}
		if sue_ok2 {
			sues_ok2 = append(sues_ok2, sue)
		}
	}
	fmt.Println(sues_ok)
	fmt.Println(sues_ok2)
}

func main() {
	var name string
	var sues = make(map[string]map[string]int)
	in := bufio.NewReader(os.Stdin)
	for {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			parts := strings.Split(str, " ")
			name = parts[1][:len(parts[1])-1]
			sues[name] = make(map[string]int)
			for i := 2; i < len(parts); i += 2 {
				feature := parts[i][:len(parts[i])-1]
				quantity, _ := strconv.Atoi(parts[i+1][:len(parts[i+1])-1])
				sues[name][feature] = quantity
			}
		}
	}
	FindSue(sues, map[string]int{
		"children":    3,
		"cats":        7,
		"samoyeds":    2,
		"pomeranians": 3,
		"akitas":      0,
		"vizslas":     0,
		"goldfish":    5,
		"trees":       3,
		"cars":        2,
		"perfumes":    1,
	}, []string{"cats", "trees"}, []string{"pomeranians", "goldfish"})
}
