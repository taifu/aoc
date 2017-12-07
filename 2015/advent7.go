package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type registry string

var NULL = registry("")

type operator_type string
type Operation struct {
	from1    registry
	from2    registry
	operator operator_type
	to       registry
}

var registries = make(map[registry]int)

func (o Operation) Solvable() bool {
	if o.Value(o.from1) != -1 {
		if o.from2 == NULL || o.Value(o.from2) != -1 {
			return true
		}
	}
	return false
}
func (o Operation) Value(reg registry) int {
	if value, ok := registries[reg]; ok {
		return value
	} else if value, err := strconv.Atoi(string(reg)); err == nil {
		return value
	}
	return -1
}
func (o Operation) Not() int {
	return 65535 - registries[o.from1]
}
func (o Operation) And() int {
	return o.Value(o.from1) & o.Value(o.from2)
}
func (o Operation) Or() int {
	return o.Value(o.from1) | o.Value(o.from2)
}
func (o Operation) Lshift() int {
	return o.Value(o.from1) << uint(o.Value(o.from2))
}
func (o Operation) Rshift() int {
	return o.Value(o.from1) >> uint(o.Value(o.from2))
}
func (o Operation) Equal() int {
	return o.Value(o.from1)
}

func main() {
	in := bufio.NewReader(os.Stdin)
	operations := make(map[int]Operation)
	for n := 0; ; n++ {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			result := strings.Split(str[:len(str)-1], " -> ")
			if value, err := strconv.Atoi(result[0]); err == nil {
				registries[registry(result[1])] = value
			} else {
				parts := strings.Split(result[0], " ")
				if len(parts) == 1 {
					operations[n] = Operation{from1: registry(parts[0]), from2: NULL, operator: operator_type("EQUAL"), to: registry(result[1])}
				} else if len(parts) == 2 {
					operations[n] = Operation{from1: registry(parts[1]), from2: NULL, operator: operator_type(parts[0]), to: registry(result[1])}
				} else {
					operations[n] = Operation{from1: registry(parts[0]), from2: registry(parts[2]), operator: operator_type(parts[1]), to: registry(result[1])}
				}
			}
		}
	}
	for {
		if len(operations) == 0 {
			break
		}
		var key_to_delete []int
		for key, operation := range operations {
			if operation.Solvable() {
				if operation.operator == "NOT" {
					registries[operation.to] = operation.Not()
				} else if operation.operator == "AND" {
					registries[operation.to] = operation.And()
				} else if operation.operator == "OR" {
					registries[operation.to] = operation.Or()
				} else if operation.operator == "RSHIFT" {
					registries[operation.to] = operation.Rshift()
				} else if operation.operator == "LSHIFT" {
					registries[operation.to] = operation.Lshift()
				} else if operation.operator == "EQUAL" {
					registries[operation.to] = operation.Equal()
				} else {
					panic(string(operation.operator))
				}
				key_to_delete = append(key_to_delete, key)
			}
		}
		for i := 0; i < len(key_to_delete); i++ {
			delete(operations, key_to_delete[i])
		}
		if _, ok := registries[registry("a")]; ok {
			break
		}
	}
	fmt.Println(registries[registry("a")])
}
