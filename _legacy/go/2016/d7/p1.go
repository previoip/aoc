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

func IsABBA(s *string) bool {
	l := len(*s)
	if l%2 != 0 || len(*s) < 4 {
		return false
	}

	l /= 2

	c1 := (*s)[l-1] == (*s)[l]
	c2 := (*s)[l-2] == (*s)[l+1]

	n1 := (*s)[l-1] != (*s)[l+1]
	n2 := (*s)[l-2] != (*s)[l]

	return c1 && c2 && n1 && n2
}

func ConvoluteABBA(s *string) bool {
	l := len(*s)

	if l < 4 {
		return false
	}

	if l > 4 {
		l -= 4
	} else {
		l = 0
	}

	for j := 0; j <= l; j++ {
		ss := (*s)[j : j+4]
		if IsABBA(&ss) {
			return true
		}
	}
	return false
}

func TCheckSliceMembers[T comparable](sl *[]T, f func(*T) bool) bool {
	for _, v := range *sl {
		if f(&v) {
			return true
		}
	}
	return false
}

func CheckSliceTStringMember(sl *[]string, f func(*string) bool) bool {
	return TCheckSliceMembers(sl, f)
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

	tsl_n := 0
	for _, ip := range ipaddrs {
		if CheckSliceTStringMember(&ip.hypernets, ConvoluteABBA) {
			continue
		}
		if CheckSliceTStringMember(&ip.supernets, ConvoluteABBA) {
			tsl_n += 1
			fmt.Print("supports TSL: ")
			fmt.Println(ip.hypernets, ip.supernets)
		}
	}
	fmt.Println("IPs count supports TSL:", tsl_n)
}
