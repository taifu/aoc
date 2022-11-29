package main

import (
    "fmt"
    "bufio"
    "os"
    "strings"
)

func main() {
    var x1, y1, x2, y2 int
    var lights [1000][1000] int
    in := bufio.NewReader(os.Stdin)
    for {
        if str, err := in.ReadString('\n'); err != nil {
            fmt.Println(err)
            break
        } else {
            toggle := false
            on := false
            if strings.HasPrefix(str, "toggle ") {
                toggle = true
                str = str[7:]
            } else if strings.HasPrefix(str, "turn on ") {
                on = true
                str = str[8:]
            } else {
                str = str[9:]
            }
            f := func(x int) int {
                if x == 0 {
                    return 0
                }
                return x - 1
            }
            if toggle {
                f = func(x int) int {
                    return x + 2
                }
            } else if on {
                f = func(x int) int {
                    return x + 1
                }
            }
            fmt.Sscanf(str, "%d,%d through %d,%d\n", &x1, &y1, &x2, &y2)
            for x := x1; x<=x2; x++ {
                for y := y1; y<=y2; y++ {
                    lights[x][y] = f(lights[x][y])
                }
            }
        }
    }
    light_on := 0
    for x := 0; x<1000; x++ {
        for y := 0; y<1000; y++ {
            light_on += lights[x][y]
        }
    }
    fmt.Println(light_on)
}

