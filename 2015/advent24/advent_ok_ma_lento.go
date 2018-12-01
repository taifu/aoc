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

func find_two_partitions_with_sum(items []int, sum int) chan [][]int {
	c := make(chan [][]int)
	go func() {
		for i := 0; i < len(items); i++ {
			if items[i] == sum {
				c <- append([][]int{{items[i]}}, append(duplicate(items[:i]), items[i+1:]...))
			} else if items[i] < sum {
				for new_partition := range find_two_partitions_with_sum(append(duplicate(items[:i]), items[i+1:]...), sum-items[i]) {
					c <- [][]int{append(new_partition[0], items[i]), new_partition[1]}
				}
			}
		}
		close(c)
	}()
	return c
}

func quantum(items []int) uint64 {
	q := uint64(1)
	for i := 0; i < len(items); i++ {
		q *= uint64(items[i])
	}
	return q
}

func divide(items []int) uint64 {
	sum := 0
	for i := 0; i < len(items); i++ {
		sum += items[i]
	}
	sum = sum / 3
	min_q := quantum(items)
	min_length := len(items)
	for partition1 := range find_two_partitions_with_sum(items, sum) {
		if len(partition1[0]) < min_length {
			min_length = len(partition1[0])
			min_q = quantum(partition1[0])
			fmt.Println(min_q)
		} else if len(partition1[0]) == min_length {
			q := quantum(partition1[0])
			if q < min_q {
				min_q = q
				fmt.Println(min_q)
			}
		}
	}
	return min_q
}

func main() {
	if q := divide(load(example)); q != 99 {
		fmt.Println("example quantum entanglement should be 99 instead of", q)
	} else {
		q := divide(load(input))
		fmt.Println("q.e.:", q) // Output:
	}
}

const (
	example = `1 2 3 4 5 7 8 9 10 11`
	input   = `1 2 3 7 11 13 17 19 23 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 101 103 107 109 113`
)
