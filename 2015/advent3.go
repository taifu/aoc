package main

import "fmt"

func main() {
    var c rune
    var x, y int
    houses := make(map[string]int)
    for {
        houses[fmt.Sprintf("%d_%d", x, y)] += 1
        if _, err := fmt.Scanf("%c", &c); err != nil {
            fmt.Println(err)
            break
        }
        if c == '^' {
            y += 1
        } else if c == 'v' {
            y -= 1
        } else if c == '>' {
            x += 1
        } else if c == '<' {
            x -= 1
        }
    }
    fmt.Printf("%d\n", len(houses))
}
