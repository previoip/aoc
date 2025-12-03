package main

import (
	"crypto/md5"
	"encoding/hex"
	"flag"
	"fmt"
	"os"
	"reflect"
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

func leni(a []string) int {
	n := 0
	for _, i := range a {
		if !reflect.ValueOf(i).IsZero() {
			n += 1
		}
	}
	return n
}

func join(s []string) string {
	r := ""
	for _, v := range s {
		r += v
	}
	return r
}

func UnpackHash(s *string) (int, *string, error) {
	ss := (*s)[5:7]
	c := string(ss[1])
	p, e := strconv.Atoi(string(ss[0]))
	fmt.Println(*s, ss, " ", p, c, e)
	if e != nil {
		return -1, &c, e
	}
	return p, &c, nil
}

func main() {
	dataSrc := make([]string, 0)
	FetchData(&dataSrc)

	c := [8]string{}
	i := 0
	data := []byte{}
	hash := [16]byte{}
	hexc := ""
	for true {
		s := fmt.Sprintf("%s%d", dataSrc[0], i)
		data = []byte(s)
		hash = md5.Sum(data[:])
		hexc = hex.EncodeToString(hash[:])
		if strings.Compare(hexc[:5], "00000") == 0 {
			ii, cc, e := UnpackHash(&hexc)

			if e == nil && ii >= 0 && ii < len(c) && len(c[ii]) == 0 {
				fmt.Println("Match", leni(c[:])+1, "/", len(c))
				c[ii] = *cc
				fmt.Println(c[:])
			}
		}
		if leni(c[:]) > len(c)-1 {
			break
		}
		i += 1
	}

	fmt.Println("passcode:", join(c[:]))
}
