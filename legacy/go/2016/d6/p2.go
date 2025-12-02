package main

import (
	"flag"
	"fmt"
	"os"
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

func FetchData(slice *[]string) {
	path := flag.String("p", "data.txt", "path to data")
	flag.Parse()

	d, e := os.ReadFile(*path)
	check(e)

	for _, v := range strings.Split(string(d), crlf()) {
		*slice = append(*slice, v)
	}
}

// ===================================================

const MaxInt = int(^uint(0) >> 1)
const MinInt = -MaxInt - 1

func GetIndex[T comparable](a *[]T, b T) int {
	for n, v := range *a {
		if v == b {
			return n
		}
	}
	return -1
}

func Min(a *[]int) int {
	m := MaxInt
	for _, v := range *a {
		if v < m {
			m = v
		}
	}
	return m
}

func CountStr(s *string) (*[]string, *[]int) {
	rint := []int{}
	rstr := []string{}

	arr := strings.Split(*s, "")
	for _, a := range arr {
		if a == "-" {
			continue
		}

		i := GetIndex(&rstr, a)
		if i == -1 {
			rstr = append(rstr, a)
			rint = append(rint, 0)
			i = len(rint) - 1
		}
		rint[i] += 1
	}
	return &rstr, &rint
}

func main() {
	dataSrc := make([]string, 0)
	FetchData(&dataSrc)

	transposed := make([]string, len(dataSrc[0]))

	for _, i := range dataSrc {
		for n, j := range i {
			transposed[n] += string(j)
		}
	}

	message := ""
	for _, l := range transposed {
		a, b := CountStr(&l)
		fmt.Println(*a, *b)
		message += (*a)[GetIndex(b, Min(b))]
	}

	fmt.Println(message)
}
