package main

import (
	"crypto/md5"
	"encoding/hex"
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

func main() {
	dataSrc := make([]string, 0)
	FetchData(&dataSrc)
	c := ""
	j := 0
	i := 0
	for true {
		s := fmt.Sprintf("%s%d", dataSrc[0], i)
		data := []byte(s)
		hash := md5.Sum(data[:])
		hexc := hex.EncodeToString(hash[:])
		if strings.Compare(hexc[:5], "00000") == 0 {
			fmt.Println("Match", string(hexc[5]), hexc)
			c += string(hexc[5])
			j += 1
		}

		if j > 7 {
			break
		}

		i += 1
	}

	fmt.Println("passcode:", c)

}
