package main

import (
	"fmt"
)

func main() {
	var step = 50
	str := []int{3, 1, 1, 3, 3, 2, 2, 1, 1, 3}
	for i := 0; i < step; i++ {
		last_chr := str[0]
		new_str := []int{}
		for n, counter := 1, 1; n <= len(str); n++ {
			next_chr := -1
			if n < len(str) {
				next_chr = str[n]
			}
			if last_chr != next_chr {
				new_str = append(new_str, counter, last_chr)
				counter = 0
			}
			last_chr = next_chr
			counter++
		}
		str = new_str
	}
	fmt.Println(len(str))
}
