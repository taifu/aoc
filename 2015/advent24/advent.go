package main

import (
	"fmt"
	"strconv"
	"strings"
)

func load(input string) []int {
	items := []int{}
	for _, s := range strings.Split(input, " ") {
		value, _ := strconv.Atoi(s)
		items = append(items, value)
	}
	return items
}

func duplicate(items []int) []int {
	return append([]int(nil), items...)
}

func find_n_partitions(items []int, length int) chan []int {
	c := make(chan []int)
	go func() {
		for i := 0; i < len(items); i++ {
			if length == 1 {
				c <- []int{items[i]}
			} else {
				for new_partition := range find_n_partitions(items[:i], length-1) {
					c <- append([]int{items[i]}, new_partition...)
				}
			}
		}
		close(c)
	}()
	return c
}

func sum(items []int) int {
	tot := 0
	for i := 0; i < len(items); i++ {
		tot += items[i]
	}
	return tot
}

func quantum(items []int) uint64 {
	q := uint64(1)
	for i := 0; i < len(items); i++ {
		q *= uint64(items[i])
	}
	return q
}

func divide(items []int, n int) uint64 {
	weigth := sum(items) / n
	min_q := quantum(items)
	min_length := 0
	for length := 1; length < len(items); length++ {
		for partition := range find_n_partitions(items, length) {
			if sum(partition) == weigth {
				min_length = length
				q := quantum(partition)
				if q < min_q {
					min_q = q
				}
			}
		}
		if min_length == length {
			break
		}
	}
	return min_q
}

func main() {
	if q := divide(load(example), 3); q != 99 {
		fmt.Println("example quantum entanglement should be 99 instead of", q)
	} else {
		q := divide(load(input), 3)
		fmt.Println("q.e.:", q) // Output:
	}
	if q := divide(load(example), 4); q != 44 {
		fmt.Println("example quantum entanglement should be 44 instead of", q)
	} else {
		q := divide(load(input), 4)
		fmt.Println("q.e.:", q) // Output:
	}
}

const (
	example = `1 2 3 4 5 7 8 9 10 11`
	input   = `1 2 3 7 11 13 17 19 23 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 101 103 107 109 113`
)
