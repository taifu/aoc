package main

import "fmt"

func main() {
    var c rune
    var x, y, xb, yb int
    houses := make(map[string]int)
    flip_flop := 1
    for {
        houses[fmt.Sprintf("%d_%d", x, y)] += 1
        houses[fmt.Sprintf("%d_%d", xb, yb)] += 1
        if _, err := fmt.Scanf("%c", &c); err != nil {
            break
        }
        if flip_flop == 1 {
            if c == '^' {
                y += 1
            } else if c == 'v' {
                y -= 1
            } else if c == '>' {
                x += 1
            } else if c == '<' {
                x -= 1
            }
        } else {
            if c == '^' {
                yb += 1
            } else if c == 'v' {
                yb -= 1
            } else if c == '>' {
                xb += 1
            } else if c == '<' {
                xb -= 1
            }
        }
        flip_flop = -flip_flop
    }
    fmt.Printf("%d\n", len(houses))
}
