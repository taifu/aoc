package main

import (
	"bufio"
	"fmt"
	"os"
)

const DIM = 100

var life [DIM]([DIM]int)

func neighbours(x, y int) int {
	on := 0
	for x1 := x - 1; x1 <= x+1; x1++ {
		for y1 := y - 1; y1 <= y+1; y1++ {
			if x1 >= 0 && x1 < DIM && y1 >= 0 && y1 < DIM && !(x1 == x && y1 == y) && life[x1][y1] == 1 {
				on += 1
			}
		}
	}
	return on
}

func loop() {
	four_angle_on()
	var next_life [DIM]([DIM]int)
	for x := 0; x < DIM; x++ {
		for y := 0; y < DIM; y++ {
			near_on := neighbours(x, y)
			if life[x][y] == 1 {
				if near_on == 2 || near_on == 3 {
					next_life[x][y] = 1
				}
			} else {
				if near_on == 3 {
					next_life[x][y] = 1
				}
			}
		}
	}
	life = next_life
	four_angle_on()
}

func four_angle_on() {
	life[0][0] = 1
	life[DIM-1][0] = 1
	life[0][DIM-1] = 1
	life[DIM-1][DIM-1] = 1
}

func show() {
	fmt.Println("=================")
	for x := 0; x < DIM; x++ {
		fmt.Println(life[x])
	}
}

func main() {
	in := bufio.NewReader(os.Stdin)
	for n := 0; ; n++ {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			for i := 0; i < len(str)-1; i++ {
				if str[i] == byte('#') {
					life[n][i] = 1
				} else {
					life[n][i] = 0
				}
			}
		}
	}
	four_angle_on()
	for n := 0; n < 100; n++ {
		//show()
		loop()
	}
	on := 0
	for x := 0; x < DIM; x++ {
		for y := 0; y < DIM; y++ {
			if life[x][y] == 1 {
				on += 1
			}
		}
	}
	fmt.Println(on)
}
