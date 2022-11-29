package main

import (
    "fmt"
    "strings"
)

func main() {
    var str string
    var good int
    for {
        if _, err := fmt.Scanf("%s\n", &str); err != nil {
            fmt.Println(err)
            break
        }
        dupl := false
        repeat := false
        for i, c := range str {
            if i < len(str) - 3 && strings.Contains(str[i+2:len(str)], str[i:i+2])  {
                dupl = true
            }
            if i < len(str) - 2 && byte(c) == str[i + 2] {
                repeat = true
            }
        }
        if dupl && repeat {
            good += 1
        }
    }
    fmt.Println(good)
}

