package main

import "fmt"

func is_valid_parentheses(s string) bool {
	var temp byte = ']'
	var dict = map[byte]byte{'[': temp, '{': '}', '(': ')'}
	var a, b, c, d, e, f int = 0, 0, 0, 0, 0, 0
	for _, val := range s {
		switch val {
		case '[':
			a++
		case ']':
			b++
		case '{':
			c++
		case '}':
			d++
		case '(':
			e++
		case ')':
			f++
		}
	}
	if a != b || c != d || e != f {
		return false
	}

	switch s[0] {
	case ']', '}', ')':
		return false
	}
	switch s[len(s)-1] {
	case '[', '{', '(':
		return false
	}

	for i, val := range s {
		switch val {
		case '[', '{', '(':
			switch byte(s[i+1]) {
			case dict[s[i]], '[', '(', '{':
				continue
			default:
				return false
			}
		}
	}
	return true
}

func removeDuplicates(nums []int) int {
	if len(nums) < 2 {
		return 0
	}
	var length int = len(nums)
	temp := []int{}
	dup := []int{}

	for i, val := range nums {
		if i == len(nums)-1 {
			temp = append(temp, val)
			break
		}

		if val == nums[i+1] {
			dup = append(dup, -1)
			length--
		} else {
			temp = append(temp, val)
		}
	}

	nums = append(nums[:0], temp...)
	nums = append(nums, dup...)
	return length
}

func main() {
	arr := []int{0, 0, 1, 1, 1, 2, 2, 3, 4, 4}
	a := removeDuplicates(arr)
	fmt.Printf("%d\n%d", a, arr)

}
