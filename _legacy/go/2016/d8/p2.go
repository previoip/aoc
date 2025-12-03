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
)

// init
func Init() {
	InitArgvPath()
}

// main
func main() {
	Init()
	fmt.Println("See part 1")
}
