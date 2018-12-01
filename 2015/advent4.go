package main

import (
    "crypto/md5"
    "fmt"
    "io"
    "strings"
)

func main() {
    key := "ckczppom"
    for i := 1; ; i++ {
       h := md5.New()
       io.WriteString(h, fmt.Sprintf("%s%d", key, i))
       if strings.HasPrefix(fmt.Sprintf("%x", h.Sum(nil)), "000000") {
           fmt.Println(i)
           break
       }
    }
}
