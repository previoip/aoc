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

func FetchData(arr *[]string) {
	path := flag.String("p", "data.txt", "path to data")
	flag.Parse()

	d, e := os.ReadFile(*path)
	check(e)

	for _, v := range strings.Split(string(d), ", ") {
		*arr = append(*arr, v)
	}
}

type vec2 struct {
	x int
	y int
}

func (v *vec2) set(x int, y int) {
	v.x = x
	v.y = y
}

func (v *vec2) eq(o *vec2) bool {
	return v.x == o.x && v.y == o.y
}

func (v *vec2) add(o *vec2) {
	v.x += o.x
	v.y += o.y
}

func newVec2(x int, y int) *vec2 {
	v := vec2{}
	v.set(x, y)
	return &v
}

type heading struct {
	vec2
}

func (h *heading) rotate(c *string) {
	m := 0
	if *c == "R" {
		m = 1
	} else if *c == "L" {
		m = -1
	} else {
		return
	}

	if h.y == 0 {
		h.y = -m * h.x
		h.x = 0
	} else {
		h.x = m * h.y
		h.y = 0
	}
}

func absint(x int) int {
	if x < 0 {
		return -x
	} else {
		return x
	}
}

func main() {

	dataSrc := make([]string, 0)
	FetchData(&dataSrc)

	me := vec2{}
	h := heading{vec2{0, 1}}

	for _, v := range dataSrc {
		rot := string(v[0])
		incr, e := strconv.Atoi(string(v[1:]))
		check(e)

		h.rotate(&rot)
		for i := 0; i < incr; i++ {
			me.add(&h.vec2)
		}
		fmt.Println(v, h.x, h.y, me)
	}

	res := absint(me.x) + absint(me.y)
	fmt.Println(res)
}
