package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
)

type Vec2 struct {
	x int
	y int
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func (v *Vec2) eq(o *Vec2) bool {
	return v.x == o.x && v.y == o.y
}

func (v *Vec2) add(o *Vec2) {
	v.x += o.x
	v.y += o.y
}

func (v *Vec2) norm() {
	if v.x != 0 {
		v.x /= abs(v.x)
	}
	if v.y != 0 {
		v.y /= abs(v.y)
	}
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
	dataSrc := make([]string, 0)
	FetchData(&dataSrc)

	keypad := [3][3]string{
		{"7", "8", "9"},
		{"4", "5", "6"},
		{"1", "2", "3"},
	}
	cursor := Vec2{0, 0}
	instr := make(map[string]*Vec2)
	var res string

	instr["U"] = &Vec2{0, 1}
	instr["D"] = &Vec2{0, -1}
	instr["L"] = &Vec2{-1, 0}
	instr["R"] = &Vec2{1, 0}

	fmt.Println(keypad)

	for _, l := range dataSrc {
		for _, istr := range l {
			cursor.add(instr[string(istr)])
			cursor.norm()
		}
		fmt.Println(cursor)
		res += keypad[cursor.y+1][cursor.x+1]
	}

	fmt.Println(res)
}
