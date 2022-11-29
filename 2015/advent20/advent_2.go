package main

import (
	"fmt"
)

const MAX = 1000000

func main() {
	var house [MAX]int
	found := false
	for elf := 1; elf < MAX && !found; elf++ {
		present := elf
		for count := 0; count < 50 && present < MAX; count++ {
			house[present] += elf * 11
			if house[present] >= 36000000 {
				fmt.Println(present, house[present])
				found = true
				break
			}
			present += elf
		}
	}
}
