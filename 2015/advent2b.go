package main

import (
    "fmt"
    "sort"
)

func main() {
    var d, l [3]int
    var paper, ribbon int
    for {
        if _, err := fmt.Scanf("%dx%dx%d\n", &d[0], &d[1], &d[2]); err != nil {
            fmt.Println(err)
            break
        } else {
            l[0], l[1], l[2] = d[0]*d[1], d[1]*d[2], d[2]*d[0]
            sort.Ints(d[:])
            sort.Ints(l[:])
            paper += 3*l[0] + 2*l[1] + 2*l[2]
            ribbon += 2*d[0] + 2*d[1] + d[0]*d[1]*d[2]
        }
    }
    fmt.Println("paper:", paper)
    fmt.Println("ribbon:", ribbon)
}
