package main

import (
	"errors"
	"flag"
	"fmt"
	"os"
	"regexp"
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

var re regexp.Regexp

func _init() {
	re = *regexp.MustCompile(`\[(\w*)\]`)
}

type IPV7 struct {
	supernets []string
	hypernets []string
}

func UnpackIPV7Address(s *string) (*IPV7, error) {
	hnets_g := re.FindAllStringSubmatch(*s, -1)
	hnets := []string{}

	if hnets_g == nil || len(hnets_g) < 1 {
		return nil, errors.New("could not parse string")
	}

	for _, v := range hnets_g {
		hnets = append(hnets, v[1])
	}

	snets := strings.Split(re.ReplaceAllString(*s, "|???|"), "|???|") //???

	ip := IPV7{}
	ip.hypernets = hnets
	ip.supernets = snets

	return &ip, nil
}

func IsXYX(s *string) bool {
	if len(*s) != 3 {
		return false
	}
	return (*s)[0] == (*s)[2] && (*s)[0] != (*s)[1]
}

func ConvoluteXYX(s *string) (bool, *[]string) {
	l := len(*s)
	pairs := []string{}

	if l < 3 {
		return false, &pairs
	}

	if l > 3 {
		l -= 3
	} else {
		l = 0
	}

	f := false
	for j := 0; j <= l; j++ {
		ss := (*s)[j : j+3]
		if IsXYX(&ss) {
			f = true
			pairs = append(pairs, ss)
		}
	}
	return f, &pairs
}

func TGetMatchesSliceMembers[T comparable](sl *[]T, f func(*T) (bool, *[]T)) (bool, *[]T) {
	ret := []T{}
	fl := false
	for _, v := range *sl {
		b, r := f(&v)
		if b {
			fl = true
			ret = append(ret, *r...)
		}
	}
	return fl, &ret
}

func GetMatchesSliceTStringMembers(sl *[]string, f func(*string) (bool, *[]string)) (bool, *[]string) {
	return TGetMatchesSliceMembers(sl, f)
}

func SliceSharesMember[T comparable](s1 *[]T, s2 *[]T) bool {
	for _, a := range *s1 {
		for _, b := range *s2 {
			if a == b {
				return true
			}
		}
	}
	return false
}

func ssswap(s *string) {
	if len(*s) != 3 {
		e := errors.New("wee")
		panic(e)
	}
	if !IsXYX(s) {
		e := errors.New("weeee")
		panic(e)
	}

	a, b := string((*s)[0]), string((*s)[1])
	(*s) = b + a + b
}

func main() {
	_init()
	dataSrc := make([]string, 0)
	FetchData(&dataSrc)
	ipaddrs := []IPV7{}

	for _, s := range dataSrc {
		ip, e := UnpackIPV7Address(&s)
		check(e)
		ipaddrs = append(ipaddrs, *ip)
	}

	ssl_n := 0

	for _, ip := range ipaddrs {
		b_hyper, m_hyper := GetMatchesSliceTStringMembers(&ip.hypernets, ConvoluteXYX)
		b_super, m_super := GetMatchesSliceTStringMembers(&ip.supernets, ConvoluteXYX)

		if !b_hyper && !b_super {
			continue
		}

		for i := 0; i < len(*m_super); i++ {
			ssswap(&(*m_super)[i]) // mate
		}

		fmt.Println(m_hyper, m_super)

		if SliceSharesMember(m_hyper, m_super) {
			ssl_n += 1
		}

	}
	fmt.Println("IPs count supports SSL:", ssl_n)
}
