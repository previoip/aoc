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

func (v *Vec2) sub(o *Vec2) {
	v.x -= o.x
	v.y -= o.y
}

func (v *Vec2) norm() {
	if abs(v.x) > 2 {
		v.x /= abs(v.x)
		v.x *= 2
	}
	if abs(v.y) > 2 {
		v.y /= abs(v.y)
		v.y *= 2
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

	keypad := [5][5]string{
		{"X", "X", "D", "X", "X"},
		{"X", "A", "B", "C", "X"},
		{"5", "6", "7", "8", "9"},
		{"X", "2", "3", "4", "X"},
		{"X", "X", "1", "X", "X"},
	}
	cursor := Vec2{-2, 0}
	instr := make(map[string]*Vec2)
	var res string

	instr["U"] = &Vec2{0, 1}
	instr["D"] = &Vec2{0, -1}
	instr["L"] = &Vec2{-1, 0}
	instr["R"] = &Vec2{1, 0}

	fmt.Println(keypad)

	for _, l := range dataSrc {
		for _, istr := range l {
			t_vec := instr[string(istr)]
			cursor.add(t_vec)
			cursor.norm()
			t_str := keypad[cursor.y+2][cursor.x+2]
			if strings.Compare(t_str, "X") == 0 {
				cursor.sub(t_vec)
			}
		}
		res += keypad[cursor.y+2][cursor.x+2]
	}

	fmt.Println(res)
}
