package main

import "testing"

var Jsons = []string{"[1,2,3]", "{\"a\":2,\"b\":4}", "[[[3]]]", "{\"a\":{\"b\":4},\"c\":-1}", "{\"a\":[-1,1]}", "[-1,{\"a\":1}]", "[]", "{}"}
var Results = []int{6, 6, 3, 3, 0, 0, 0, 0}

func TestJsonSum(t *testing.T) {
	for i := 0; i < len(Results); i++ {
		sum := JsonSum(Jsons[i])
		if false && sum != Results[i] {
			t.Fatalf("Sum di %s dovrebbe essere %d e non %d", Jsons[i], Results[i], sum)
		}
	}
}
