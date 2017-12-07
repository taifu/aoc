package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"strconv"
)

func DeepSumOld(i interface{}) int {
	v := reflect.ValueOf(i)
	fmt.Println("DeepSum", v)
	fmt.Println("DeepSum", i, reflect.TypeOf(i).Kind())
	//fmt.Println("v.String() ", v.String())
	tot := int(0)
	value, err := strconv.Atoi(v.String())
	if err == nil {
		tot += value
	} else {
		switch reflect.TypeOf(i).Kind() {
		case reflect.Map:
			fmt.Println("Map", v)
			for _, key := range v.MapKeys() {
				tot += DeepSum(v.MapIndex(key))
			}
		case reflect.Slice:
			fmt.Println("Slice", v, v.Len())
			for i := 0; i < v.Len(); i++ {
				fmt.Println("Deeppo", v.Index(i))
				tot += DeepSum(v.Index(i))
			}
		case reflect.Struct:
			fmt.Println("Struct", v)
		default:
			fmt.Println("Boh", reflect.TypeOf(i).Kind())
		}
	}
	/*
		fmt.Println(reflect.TypeOf(i))
		fmt.Println(reflect.TypeOf(reflect.ValueOf(i)))
		//fmt.Println(reflect.TypeOf(reflect.Value{i}))
		switch v := i.(type) {
		case string:
			fmt.Println("string", v)
		case []int:
			fmt.Println("int[]", v)
		default:
			fmt.Println("boh...", v)
		}
	*/
	return tot
}

func DeepSum(i reflect.Value) int {
	tot := 0
	v := reflect.ValueOf(i)
	switch reflect.TypeOf(i).Kind() {
	case reflect.Map:
		fmt.Println("Map", v)
		for _, key := range v.MapKeys() {
			tot += DeepSum(v.MapIndex(key))
		}
	case reflect.Slice:
		fmt.Println("Slice", v, v.Len())
		for i := 0; i < v.Len(); i++ {
			tot += DeepSum(v.Index(i))
		}
	case reflect.Struct:
		fmt.Println("Struct", v)
		tot += DeepSum(reflect.ValueOf(v))
	default:
		fmt.Println("Boh", v.Type, v.Kind)
	}
	return tot
}

func JsonSum(jsonstr string) int {
	var result map[string]interface{}
	if err := json.Unmarshal([]byte(jsonstr), &result); err != nil {
		var result2 []interface{}
		if err := json.Unmarshal([]byte(jsonstr), &result2); err != nil {
			panic(err)
		} else {
			//fmt.Println(result2)
			return DeepSum(reflect.ValueOf(result2))
		}
	} else {
		//fmt.Println(result)
		return DeepSum(reflect.ValueOf(result))
	}
	return 0

	/*
		var dat interface{}
		byt := []byte(jsonstr)
		if err := json.Unmarshal(byt, &dat); err != nil {
			panic(err)
		}
		return DeepSum(dat)
	*/
}

func main() {
	in := bufio.NewReader(os.Stdin)
	if str, err := in.ReadString('\n'); err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(JsonSum(str))
	}
}
