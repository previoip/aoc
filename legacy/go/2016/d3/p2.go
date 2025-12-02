package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func crlf() string {
	ps := fmt.Sprintf("%v", os.PathSeparator)
	lf := "\n"
	if ps != "/" {
		lf = "\r\n"
	}
	return lf
}

func UnpackInput(v string) *[3]int {
	t := [3]int{}
	for i := 0; i < 3; i++ {
		t_v := v[5*i : (5*i)+5]
		t_a, e := strconv.Atoi(strings.Trim(t_v, " "))
		check(e)
		t[i] = t_a
	}
	return &t
}

func IsTris(arr *[3]int) bool {
	permute := [3][2]int{{arr[1], arr[2]}, {arr[0], arr[2]}, {arr[0], arr[1]}}
	for n, a := range permute {
		if arr[n] >= a[0]+a[1] {
			return false
		}
	}
	return true
}

func FetchData(slice *[]string) {
	path := flag.String("p", "data.txt", "path to data")
	flag.Parse()

	d, e := os.ReadFile(*path)
	check(e)

	for _, v := range strings.Split(string(d), crlf()) {
		*slice = append(*slice, v)
	}
}

func main() {
	fmt.Println("no")
}
