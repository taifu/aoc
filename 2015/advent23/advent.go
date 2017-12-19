package main

import (
	"fmt"
	"strconv"
	"strings"
)

const (
	A   = "a"
	B   = "b"
	HLF = "hlf"
	TPL = "tpl"
	INC = "inc"
	JMP = "jmp"
	JIE = "jie"
	JIO = "jio"
)

type (
	register string
	step     struct {
		instruction string
		reg         register
		jump        int
	}
	program []step
)

func load(input string) program {
	prg := program{}
	for _, s := range strings.Split(input, "\n") {
		parts := strings.Split(s, " ")
		if len(parts) == 3 {
			jump, _ := strconv.Atoi(parts[2])
			prg = append(prg, step{parts[0], register(parts[1][:1]), jump})
		} else {
			if jump, err := strconv.Atoi(parts[1]); err == nil {
				prg = append(prg, step{parts[0], "", jump})
			} else {
				prg = append(prg, step{parts[0], register(parts[1]), 0})
			}
		}
	}
	return prg
}

func compute(prg program, start_a, start_b int) (a, b int) {
	a = start_a
	b = start_b
	for n_step := 0; n_step < len(prg); {
		step := prg[n_step]
		switch step.instruction {
		case HLF:
			if step.reg == A {
				a = a / 2
			} else {
				b = b / 2
			}
			n_step += 1
		case TPL:
			if step.reg == A {
				a = a * 3
			} else {
				b = b * 3
			}
			n_step += 1
		case INC:
			if step.reg == A {
				a += 1
			} else {
				b += 1
			}
			n_step += 1
		case JMP:
			n_step += step.jump
		case JIE:
			if step.reg == A {
				if a%2 == 0 {
					n_step += step.jump
				} else {
					n_step += 1
				}
			} else if step.reg == B {
				if b%2 == 0 {
					n_step += step.jump
				} else {
					n_step += 1
				}
			} else {
				panic(step)
			}
		case JIO:
			if step.reg == A {
				if a == 1 {
					n_step += step.jump
				} else {
					n_step += 1
				}
			} else if step.reg == B {
				if b == 1 {
					n_step += step.jump
				} else {
					n_step += 1
				}
			} else {
				panic(step)
			}
		default:
			panic(step)
		}
	}
	return
}

func main() {
	if a, b := compute(load(example), 0, 0); a != 2 {
		fmt.Println("example a register should be 2", a, b)
	} else {
		_, b := compute(load(input), 0, 0)
		fmt.Println("b:", b) // Output:
		_, b = compute(load(input), 1, 0)
		fmt.Println("b:", b) // Output:
		//fmt.Println("longest:", l)  // Output: 736
	}
}

const (
	example = `inc a
jio a, +2
tpl a
inc a`
	input = `jio a, +19
inc a
tpl a
inc a
tpl a
inc a
tpl a
tpl a
inc a
inc a
tpl a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
jmp +23
tpl a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
inc a
tpl a
inc a
tpl a
inc a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
tpl a
inc a
jio a, +8
inc b
jie a, +4
tpl a
inc a
jmp +2
hlf a
jmp -7`
)
