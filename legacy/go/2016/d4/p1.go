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

var (
	re regexp.Regexp
)

type Room struct {
	name     string
	sector   int
	checksum string
}

func GetIndex[T comparable](a *[]T, b T) int {
	for n, v := range *a {
		if v == b {
			return n
		}
	}
	return -1
}

func UnpackRoom(s *string) (*Room, error) {
	res := re.FindAllStringSubmatch(*s, 1)[0]

	if res == nil {
		return nil, errors.New("match is null")
	}

	room := &Room{}
	sector, e := strconv.Atoi(res[2])

	if e != nil {
		return nil, e
	}

	room.sector = sector
	room.name = res[1]
	room.checksum = res[3]

	return room, nil
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

// https://stackoverflow.com/questions/30226438/generate-all-permutations-in-go
func genPerm[T comparable](array []T, n int, result *[][]T) {
	if n == 1 {
		dst := make([]T, len(array))
		copy(dst, array[:])
		*result = append(*result, dst)
	} else {
		for i := 0; i < n; i++ {
			genPerm(array, n-1, result)
			if n%2 == 0 {
				array[0], array[n-1] = array[n-1], array[0]
			} else {
				array[i], array[n-1] = array[n-1], array[i]
			}
		}
	}
}

func join(s *[]string) string {
	r := ""
	for _, v := range *s {
		r += v
	}
	return r
}

func FlushBuffPerm(strsl *[]string, buff *string) {
	s := strings.Split(*buff, "")
	p := [][]string{}
	lb := len(*buff)

	genPerm(s, lb, &p)

	nn := len(*strsl) * len(p)
	for i := 0; i < nn-1; i++ {
		*strsl = append(*strsl, (*strsl)[i%len(*strsl)])
	}

	for i := 0; i < nn; i++ {
		(*strsl)[i%len(*strsl)] += join(&p[i%len(p)])
	}

	*buff = ""
}

func GenCksPerm(s *string) *[]string {
	perm := []string{""}
	buff := ""
	sstr, sint := CountStr(s)

	t := 0
	for i := len(*sint) - 1; i >= 0; i-- {
		if t <= (*sint)[i] {
			t = (*sint)[i]
		} else {
			(*sint)[i] = 0
		}
	}

	t = MaxInt
	for n, v := range *sint {
		if v == 0 {
			continue
		}
		if v < t {
			t = v
			// flush buff
			FlushBuffPerm(&perm, &buff)
			buff = ""
		}
		buff += (*sstr)[n]
	}
	FlushBuffPerm(&perm, &buff)

	return &perm
}

func main() {
	re = *regexp.MustCompile(`^([\w\-]*)\-(\d{3})\[(\w{5})\]`)

	dataSrc := make([]string, 0)
	FetchData(&dataSrc)

	rooms := make([]*Room, len(dataSrc))

	for i, a := range dataSrc {
		r, e := UnpackRoom(&a)
		check(e)
		rooms[i] = r
	}

	var v_sums int
	var flag bool

	for _, v := range rooms {

		cks := GenCksPerm(&v.name)
		for _, css := range *cks {
			if len(css) > 4 {
				if strings.Compare(css[:5], v.checksum) == 0 {
					flag = true
				}
			}
		}

		if flag {
			v_sums += v.sector
		}
		flag = false
	}
	fmt.Println(v_sums)
	fmt.Println("data does not produce correct answer")
}
