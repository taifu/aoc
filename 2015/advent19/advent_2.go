package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

var transformations = make(map[string][]string)

func isInMap(key string, set map[string][]string) bool {
	value := set[key]
	if value == nil {
		return false
	}
	return true
}

func main() {
	var original_molecule string
	in := bufio.NewReader(os.Stdin)
	status := 0
	for n := 0; ; n++ {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			if len(str) == 1 {
				status = 1
			} else if status == 1 {
				original_molecule = str[:len(str)-1]
			} else {
				result := strings.Split(str[:len(str)-1], " => ")
				to, from := result[0], result[1]
				if !isInMap(from, transformations) {
					transformations[from] = []string{to}
				} else {
					transformations[from] = append(transformations[from], to)
				}
			}
		}
	}
	for key, value := range transformations {
		if len(value) > 1 {
			fmt.Println("Bad!", key, value)
			panic("Bad!")
		}
	}
	found := false
	for max_step := 0; max_step < 20 && !found; max_step++ {
		total_transformations := 0
		molecule := original_molecule
		for step := 1; ; step++ {
			n_transformations := 0
			for key, value := range transformations {
				new_pos := 0
				for pos := 0; ; {
					new_pos = strings.Index(molecule[pos:len(molecule)], key)
					if new_pos == -1 {
						break
					}
					pos += new_pos
					molecule = molecule[:pos] + value[0] + molecule[pos+len(key):]
					pos += 1
					n_transformations += 1
				}
			}
			total_transformations += n_transformations
			if molecule == "e" {
				found = true
				fmt.Println("Found!", total_transformations)
				break
			}
			if n_transformations == 0 {
				fmt.Println("Deadlock")
				break
			}
		}
	}
	if !found {
		fmt.Println("Try again (randomization will succeed in two or three attempts")
	}
}
