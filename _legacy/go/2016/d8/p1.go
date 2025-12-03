package main

import (
	"flag"
	"fmt"
	"os"
	"regexp"
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

func FetchData(slice *[]string, path *string) {
	d, e := os.ReadFile(*path)
	check(e)

	for _, v := range strings.Split(string(d), crlf()) {
		*slice = append(*slice, v)
	}
}

func InitArgvPath() {
	path := flag.String("p", "data.txt", "path to data")
	flag.Parse()

	pt := "test_data.txt"
	if len(*path)-len(pt) > 0 && len((*path)[len(*path)-len(pt):]) >= len(pt) && strings.Compare((*path)[len(*path)-len(pt):], pt) == 0 {
		isTest = true
	}

	dataSrc = make([]string, 0)
	FetchData(&dataSrc, path)
}

func InitArgvRaw() {
	dataSrc = make([]string, 0)
}

// ===================================================

// globals
var (
	dataSrc []string
	isTest  bool
	re_inst regexp.Regexp
)

// init
func Init() {
	InitArgvPath()
	re_inst = *regexp.MustCompile(`(rotate|rect)\s(?:(?:(\d+)x(\d+))|(?:(row|column)\s(x|y)\=(\d+)\sby\s(\d+)))`)
}

type Screen struct {
	buf [][]bool
	w   uint
	h   uint
}

func (s *Screen) Peek() {
	for _, r := range s.buf {
		for _, c := range r {
			cc := "."
			if c {
				cc = "#"
			}
			fmt.Print(cc, " ")
		}
		fmt.Println()
	}
}

func (s *Screen) CountA() int {
	n := 0
	for _, r := range s.buf {
		for _, v := range r {
			if v {
				n += 1
			}
		}
	}
	return n
}

func (s *Screen) DrawRect(x, y, w, h uint) {
	var i, j uint
	for j = y; j < y+h; j++ {
		for i = x; i < x+w; i++ {
			s.buf[j][i] = true
		}
	}
}

func (s *Screen) Rotate(d_enum string, offset, incr uint) {
	if incr == 0 {
		return
	}

	var i, j uint
	var t bool

	if d_enum == "row" || d_enum == "y" {
		incr %= s.w
		offset %= s.h

		t = s.buf[offset][s.w-1]
		for i = 0; i < incr; i++ {
			for j = 1; j < s.w; j++ {
				s.buf[offset][s.w-j] = s.buf[offset][s.w-j-1]
			}
			s.buf[offset][0] = t
			t = s.buf[offset][s.w-1]
		}

	} else if d_enum == "column" || d_enum == "x" {
		incr %= s.h
		offset %= s.w

		t = s.buf[s.h-1][offset]
		for i = 0; i < incr; i++ {
			for j = 1; j < s.h; j++ {
				s.buf[s.h-j][offset] = s.buf[s.h-j-1][offset]
			}
			s.buf[0][offset] = t
			t = s.buf[s.h-1][offset]
		}

	}

}

func NewScreen(w uint, h uint) Screen {
	n := Screen{w: w, h: h}
	n.buf = make([][]bool, h)
	var i uint
	for i = 0; i < h; i++ {
		n.buf[i] = make([]bool, w)
	}
	return n
}

// main
func main() {
	Init()

	var w, h uint
	w, h = 50, 6
	if isTest {
		w, h = 7, 3
	}

	screen := NewScreen(w, h)

	for _, v := range dataSrc {
		r_a := re_inst.FindAllStringSubmatch(v, -1)
		if r_a == nil {
			fmt.Println("could not parse input string")
			continue
		}
		r_g := r_a[0][1:]

		if r_g[0] == "rect" {
			a, e := strconv.ParseUint(r_g[1], 10, 32)
			check(e)
			b, e := strconv.ParseUint(r_g[2], 10, 32)
			check(e)
			screen.DrawRect(0, 0, uint(a), uint(b))
		}

		if r_g[0] == "rotate" {
			direction := r_g[3]
			ofset, e := strconv.ParseUint(r_g[5], 10, 32)
			check(e)
			incr, e := strconv.ParseUint(r_g[6], 10, 32)
			check(e)
			screen.Rotate(direction, uint(ofset), uint(incr))

		}
		fmt.Println(r_g)
		screen.Peek()
		fmt.Println()
	}

	fmt.Println("Part 1 Answer: Lit Cells Count: ", screen.CountA())
	fmt.Println("Part 2 Answer:")
	screen.Peek()
}
