package main

import (
	"fmt"
	"io/ioutil"
	//"strings"
	//"strconv"
)

func main() {
	dat, _ := ioutil.ReadFile("src/advent/advent1.txt")
	floor := 0
	first := true
	for i, ch := range dat {
		if ch == '(' {
			floor += 1
		} else if ch == ')' {
			floor -= 1
		}
		if floor == -1 && first {
			fmt.Printf("Floor -1: %d\n", i+1)
			first = false
		}
	}
	fmt.Printf("Floor: %d\n", floor)
}
