package main

import "testing"

// hijklmmn meets the first requirement (because it contains the straight hij) but fails the second requirement requirement (because it contains i and l).
func TestPwdOk1(t *testing.T) {
	pwd := "hijklmmn"
	if TestPwd(ConvertPwd(pwd)) {
		t.Fatalf("Password %s dovrebbe essere ko", pwd)
	}
}

// abbceffg meets the third requirement (because it repeats bb and ff) but fails the first requirement.
func TestPwdOk2(t *testing.T) {
	pwd := "abbceffg"
	if TestPwd(ConvertPwd(pwd)) {
		t.Fatalf("Password %s dovrebbe essere ko", pwd)
	}
}

// abbcegjk fails the third requirement, because it only has one double letter (bb).
func TestPwdKo3(t *testing.T) {
	pwd := "aabbcegjk"
	if TestPwd(ConvertPwd(pwd)) {
		t.Fatalf("Password %s dovrebbe essere ko", pwd)
	}
}

// The next password after abcdefgh is abcdffaa
func TestNextPwd1(t *testing.T) {
	pwd1 := "abcdefgh"
	pwd2 := "abcdffaa"
	next_pwd := NextPwd(ConvertPwd(pwd1))
	if !ComparePwd(next_pwd, ConvertPwd(pwd2)) {
		t.Fatalf("Next password %s dovrebbe essere %s e non %s", pwd1, pwd2, string(next_pwd))
	}
}

// The next password after ghijklmn is ghjaabcc, because you eventually skip all the passwords that start with ghi..., since i is not allowed.
func TestNextPwd2(t *testing.T) {
	pwd1 := "ghijklmn"
	pwd2 := "ghjaabcc"
	next_pwd := NextPwd(ConvertPwd(pwd1))
	if !ComparePwd(next_pwd, ConvertPwd(pwd2)) {
		t.Fatalf("Next password %s dovrebbe essere %s e non %s", pwd1, pwd2, string(next_pwd))
	}
}
