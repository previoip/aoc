package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type WholeNumber interface {
	int | int8 | int32 | int64 | uint | uint8 | uint32 | uint64
}

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

func FetchData(arr *[]string) {
	path := flag.String("p", "data.txt", "path to data")
	flag.Parse()

	d, e := os.ReadFile(*path)
	check(e)

	for _, v := range strings.Split(string(d), crlf()) {
		*arr = append(*arr, v)
	}
}

func Sums[T WholeNumber](arr *[]T) T {
	var s T
	for _, v := range *arr {
		s += v
	}
	return s
}

func Max[T WholeNumber](arr *[]T) T {
	var s T
	for _, v := range *arr {
		if v > s {
			s = v
		}
	}
	return s
}

func main() {
	dataSrc := make([]string, 0)
	FetchData(&dataSrc)

	elves := make(map[uint][]int32)
	var c uint

	for _, v := range dataSrc {
		if v == "" {
			c += 1
			continue
		}
		a, e := strconv.ParseInt(v, 10, 32)
		check(e)
		elves[c] = append(elves[c], int32(a))
	}

	sums := make([]int32, 0)
	for _, v := range elves {
		sums = append(sums, Sums(&v))
	}

	fmt.Println(Max(&sums))
}
