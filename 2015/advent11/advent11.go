package main

import (
	"fmt"
)

func ComparePwd(pwd1, pwd2 []rune) bool {
	if len(pwd1) == len(pwd2) {
		for i, ch1 := range pwd1 {
			if ch1 != pwd2[i] {
				return false
			}
		}
	}
	return true
}

func ConvertCodes(codes []rune) string {
	return string(codes)
}

func ConvertPwd(pwd string) []rune {
	return []rune(pwd)
}

func TestPwd(pwd []rune) bool {
	ok1 := false
	ok2 := false
	first_pair := rune(' ')
	for i := 0; i < len(pwd); i++ {
		if pwd[i] == rune('i') || pwd[i] == rune('o') || pwd[i] == rune('l') {
			return false
		}
		if !ok1 && i < len(pwd)-2 && (int(pwd[i]) == int(pwd[i+1])-1 && int(pwd[i+1]) == int(pwd[i+2])-1) {
			ok1 = true
		} else if !ok2 && i < len(pwd)-1 && int(pwd[i]) == int(pwd[i+1]) {
			if first_pair == rune(' ') {
				first_pair = pwd[i]
			} else if first_pair != pwd[i] {
				ok2 = true
			}
		}
	}
	return ok1 && ok2
}

func GetNextPwd(pwd []rune) []rune {
	i := len(pwd) - 1
	for {
		pwd[i] += 1
		if pwd[i] <= rune('z') {
			return pwd
		}
		pwd[i] = 'a'
		i -= 1
	}
}

func NextPwd(pwd []rune) []rune {
	for {
		pwd = GetNextPwd(pwd)
		if TestPwd(pwd) {
			return pwd
		}
	}
}

func main() {
	pwd := ConvertPwd("hxbxwxba")
	pwd = NextPwd(pwd)
	fmt.Println(ConvertCodes(pwd))
	pwd = NextPwd(pwd)
	fmt.Println(ConvertCodes(pwd))
}
