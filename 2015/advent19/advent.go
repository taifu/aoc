package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

var molecule string
var transformations = make(map[string][]string)
var target = make(map[string]bool)

func isInMap(key string, set map[string][]string) bool {
	value := set[key]
	if value == nil {
		return false
	}
	return true
}

func main() {
	in := bufio.NewReader(os.Stdin)
	status := 0
	for n := 0; ; n++ {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			if len(str) == 1 {
				status = 1
			} else if status == 1 {
				molecule = str
			} else {
				result := strings.Split(str[:len(str)-1], " => ")
				from, to := result[0], result[1]
				if !isInMap(from, transformations) {
					transformations[from] = []string{to}
				} else {
					transformations[from] = append(transformations[from], to)
				}
			}
		}
	}
	for key, value := range transformations {
		new_pos := 0
		for pos := 0; ; {
			new_pos = strings.Index(molecule[pos:len(molecule)], key)
			if new_pos == -1 {
				break
			}
			pos += new_pos
			for _, repl := range value {
				//fmt.Println("===========")
				//fmt.Println(molecule)
				//fmt.Println(key, value, pos)
				//fmt.Println(molecule[:pos] + repl + molecule[pos+len(key):])
				target[molecule[:pos]+repl+molecule[pos+len(key):]] = true
			}
			pos += 1
		}

	}
	fmt.Println(len(target))
	//fmt.Println(molecule)
	//fmt.Println(transformations)
}
