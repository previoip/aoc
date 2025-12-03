package main

import (
	"errors"
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
	dataSrc   []string
	isTest    bool
	re_marker regexp.Regexp
)

// init
func Init() {
	InitArgvPath()
	re_marker = *regexp.MustCompile(`\((-?\d+)x(-?\d+)\)`)
	// isTest = true
}

func TestPrintln(a ...any) {
	if isTest {
		fmt.Println(a...)
	}
}

type StringReader struct {
	s      *string
	cursor int
	l      int
}

func (r *StringReader) Read(size int) (string, error) {
	if r.AtEOL() {
		return "", errors.New("reader out of range")
	}

	if size+r.cursor > r.l {
		size = r.l - r.cursor
	}

	defer func() {
		r.cursor += size
	}()

	return (*r.s)[r.cursor : r.cursor+size], nil
}

func (r *StringReader) AtEOL() bool {
	if r.cursor >= r.l {
		return true
	}
	return false
}

func (r *StringReader) SetBuf(s *string) {
	r.s = s
	r.l = len(*s)
}

func (r *StringReader) Seek(n int, mode uint) {
	if mode == 0 {
		r.cursor = n
		return
	}

	if mode == 1 {
		r.cursor += n
	}

	if r.AtEOL() {
		r.cursor = r.l - 1
	}

	if r.cursor < 0 {
		r.cursor = 0
	}
}

func (r *StringReader) Peek() int {
	return r.cursor
}

func (r *StringReader) Repr() string {
	return fmt.Sprintf("%d / %d", r.cursor, r.l)
}

func ComputeDecompSize(sr *StringReader) int {
	size_s := 0
	b := ""
	for !sr.AtEOL() {
		TestPrintln("\t\t\t", sr.Repr())
		c, e := sr.Read(1)
		check(e)
		b += c
		if re_marker.MatchString(b) {
			TestPrintln("   sub: ", b)
			size_s += 1
			m_i := re_marker.FindStringIndex(b)
			m_v := re_marker.FindAllStringSubmatch((b)[m_i[0]:m_i[1]], 1)[0][1:]

			m_l := m_i[1] - m_i[0]
			size_s -= m_l

			ll, e := strconv.Atoi(m_v[0])
			check(e)
			nt, e := strconv.Atoi(m_v[1])
			check(e)
			curr_ckpt := sr.Peek()
			nb, e := sr.Read(ll)
			check(e)

			llt := ll
			if re_marker.MatchString(nb) {
				sr.Seek(curr_ckpt, 0)
				ll = ComputeDecompSize(sr)
				TestPrintln("      ll: ", ll)
				sr.Seek(curr_ckpt+llt, 0)
			}
			size_s += ll * nt
			TestPrintln("   sub: ", b, "|", nb, m_v)
			TestPrintln("   mul: ", ll, nt, ll*nt)
			b = ""
		} else {
			size_s += 1
		}
		TestPrintln("   str size: ", size_s, b)
	}
	return size_s
}

// main
func main() {
	Init()
	for _, line := range dataSrc {
		reader := new(StringReader)
		reader.SetBuf(&line)
		res := ComputeDecompSize(reader)
		TestPrintln(line, " --> ", res)
		TestPrintln()

		fmt.Println("sizeof: ", res)
		break
	}
}
