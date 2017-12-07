package main

import (
	"fmt"
)

var combinations = 0
var combinations_min = 0
var best_min = 9999

func sum(numbers []int) int {
	total := 0
	for i := 0; i < len(numbers); i += 1 {
		total += numbers[i]
	}
	return total
}

func subset_sum(numbers []int, target int, partial []int) {
	s := sum(partial)

	// check if the partial sum is equals to target
	if s == target {
		if len(partial) < best_min {
			best_min = len(partial)
			combinations_min = 1
		} else if len(partial) == best_min {
			combinations_min += 1
		}
		combinations += 1
		//print "sum(%s)=%s" % (partial, target)
	}
	if s >= target {
		return // if we reach the number why bother to continue
	}

	for i := 0; i < len(numbers); i++ {
		n := numbers[i]
		remaining := numbers[i+1 : len(numbers)]
		subset_sum(remaining, target, append(partial, n))
	}
}

func main() {
	subset_sum([]int{50, 44, 11, 49, 42, 46, 18, 32, 26, 40, 21, 7, 18, 43, 10, 47, 36, 24, 22, 40}, 150, []int{})
	fmt.Println(combinations)
	fmt.Println(best_min, combinations_min)
}
