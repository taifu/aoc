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
        fmt.Println(str)
        if ! (strings.Contains(str, "ab") || strings.Contains(str, "cd") || strings.Contains(str, "pq") || strings.Contains(str, "xy")) {
            vowels := 0
            row2 := false
            for i, c := range str {
                if strings.Contains("aeiou", string(c)) {
                    vowels += 1
                }
                if i < len(str) - 1 && byte(c) == str[i + 1] {
                    row2 = true
                }
            }
            if vowels >= 3 && row2 {
                good += 1
            }
        }
    }
    fmt.Println(good)
}

