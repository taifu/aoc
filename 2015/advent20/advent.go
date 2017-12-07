package main

import (
	"fmt"
)

const MAX = 1000000

func main() {
	var house [MAX]int
	found := false
	for elf := 1; elf < MAX && !found; elf++ {
		for present := elf; present < MAX; present += elf {
			house[present] += elf * 10
			if house[present] >= 36000000 {
				fmt.Println(present, house[present])
				found = true
				break
			}
		}
	}
}
