package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	var dim [3]int

	area_tot := 0
	ribbon_tot := 0
	dat, err := ioutil.ReadFile("src/advent/advent2.txt")
	check(err)
	result := strings.Split(string(dat), "\n")
	for i := range result {
		result := strings.Split(result[i], "x")
		if len(result) == 3 {
			for i := 0; i < 3; i++ {
				dim[i], _ = strconv.Atoi(result[i])
			}
			area1 := dim[0] * dim[1]
			area2 := dim[0] * dim[2]
			area3 := dim[1] * dim[2]
			area_min := 0
			if area1 < area2 {
				if area3 < area1 {
					area_min = area3
				} else {
					area_min = area1
				}
			} else {
				if area3 < area2 {
					area_min = area3
				} else {
					area_min = area2
				}
			}
			area_tot += area1*2 + area2*2 + area3*2 + area_min

			ribbon_tot += dim[0] * dim[1] * dim[2]
			if dim[0] > dim[1] {
				if dim[0] > dim[2] {
					ribbon_tot += 2 * (dim[1] + dim[2])
				} else {
					ribbon_tot += 2 * (dim[0] + dim[1])
				}
			} else {
				if dim[1] > dim[2] {
					ribbon_tot += 2 * (dim[0] + dim[2])
				} else {
					ribbon_tot += 2 * (dim[0] + dim[1])
				}
			}
		}
	}
	fmt.Printf("Area %d\n", area_tot)
	fmt.Printf("Ribbon %d\n", ribbon_tot)
}
