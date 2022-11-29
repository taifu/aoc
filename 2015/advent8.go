package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	tot_string := 0
	tot_memory := 0
	tot_encoded := 0
	for n := 0; ; n++ {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			tot_string += len(str) - 1
			tot_memory += len(str) - 1 - 2 - (len(strings.Split(str, "\\\\")) - 1)
			tot_encoded += len(str) - 1 + 4 + 2*(len(strings.Split(str, "\\\\"))-1)
			str = strings.Replace(str, "\\\\", "", -1)
			tot_memory += -(len(strings.Split(str, "\\\"")) - 1)
			tot_encoded += 2 * (len(strings.Split(str, "\\\"")) - 1)
			str = strings.Replace(str, "\\\"", "", -1)
			tot_memory += -3 * (len(strings.Split(str, "\\x")) - 1)
			tot_encoded += (len(strings.Split(str, "\\x")) - 1)
		}
	}
	fmt.Println(tot_string - tot_memory)
	fmt.Println(tot_encoded - tot_string)
}
