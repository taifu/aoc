package main

import (
	"bufio"
	"fmt"
	"os"
)

type Ingredient struct {
	name                                            string
	capacity, durability, flavor, texture, calories int
}

func Sum(teaspoons []int) int {
	total := 0
	for i := 0; i < len(teaspoons); i += 1 {
		total += teaspoons[i]
	}
	return total
}

type intStatefulIterator struct {
	total, length int
	counters      []int
}

func (it *intStatefulIterator) Counters() []int {
	return it.counters
}

func (it *intStatefulIterator) Next() bool {
	i := it.length - 2
	for {
		it.counters[i] += 1
		if Sum(it.counters[0:it.length-1]) <= it.total {
			break
		}
		it.counters[i] = 0
		i--
		if i < 0 {
			return false
		}
	}
	it.counters[it.length-1] = it.total - Sum(it.counters[0:it.length-1])
	if it.counters[0] > it.total {
		return false
	}
	return true
}

func NewIntStatefulIterator(total int, length int) *intStatefulIterator {
	var counters = make([]int, length)
	counters[length-1] = total
	return &intStatefulIterator{total: total, length: length, counters: counters}
}

func BestCookie(ingredients []Ingredient, teaspoons int, calories int) int {
	best := 0
	it := NewIntStatefulIterator(teaspoons, len(ingredients))
	for {
		//fmt.Println(it.Counters())
		cookie, cookie_calories := CalcCookie(ingredients, it.Counters())
		if calories <= 0 || cookie_calories == calories {
			if cookie > best {
				best = cookie
			}
		}
		if !it.Next() {
			break
		}
	}
	return best
}

func CalcCookie(ingredients []Ingredient, teaspoons []int) (int, int) {
	var capacity, durability, flavor, texture, calories int
	for i := 0; i < len(ingredients); i += 1 {
		capacity += ingredients[i].capacity * teaspoons[i]
		durability += ingredients[i].durability * teaspoons[i]
		flavor += ingredients[i].flavor * teaspoons[i]
		texture += ingredients[i].texture * teaspoons[i]
		calories += ingredients[i].calories * teaspoons[i]
	}
	if capacity <= 0 || durability <= 0 || flavor <= 0 || texture <= 0 {
		return 0, calories
	}
	return capacity * durability * flavor * texture, calories
}

func main() {
	var name string
	var capacity, durability, flavor, texture, calories int
	var ingredients []Ingredient
	in := bufio.NewReader(os.Stdin)
	for {
		if str, err := in.ReadString('\n'); err != nil {
			break
		} else {
			fmt.Sscanf(str, "%s capacity %d, durability %d, flavor %d, texture %d, calories %d\n",
				&name, &capacity, &durability, &flavor, &texture, &calories)
			name = name[:len(name)-1]
			ingredient := Ingredient{name, capacity, durability, flavor, texture, calories}
			ingredients = append(ingredients, ingredient)
		}
	}
	best := BestCookie(ingredients, 100, 0)
	fmt.Printf("%d\n", best)
	best = BestCookie(ingredients, 100, 500)
	fmt.Printf("%d\n", best)
}
