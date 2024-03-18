package main

import (
	"fmt"
	"math"
)

// 26. Remove Duplicates from sorted array
// runtime 6 ms (better than 72% of Go users) memory 6.12 MB (better than 5% of Go users)
// https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/?envType=featured-list&envId=top-interview-questions?envType=featured-list&envId=top-interview-questions
func removeDuplicates(nums []int) int {
	switch len(nums) {
	case 0:
		return 0
	case 1:
		return 1
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

// problem 28. Find the index of the first occurence in a String
// runtime 1 ms memory 2.00 MB (better than 94% of Go users)
// https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/?envType=featured-list&envId=top-interview-questions?envType=featured-list&envId=top-interview-questions
func strStr(haystack string, needle string) int {
	if len(needle) > len(haystack) {
		fmt.Println("here")
		return -1
	} else if len(haystack) == 0 || len(needle) == 0 {
		fmt.Println("here1")
		return -1
	}
	var idx int = -1

	//well the nest is horrible but, weirdly so, it's as fast and memory efficent as it can be so I'll leave it that way
	for I, val := range haystack {
		if val == rune(needle[0]) {
			var i int = I
			for a, val1 := range needle {
				if i == len(haystack) || val1 != rune(haystack[i]) {
					break
				} else if a == len(needle)-1 {
					idx = I
					return idx
				}
				i++
			}
		}
	}
	return idx
}

// it is uncorrect solution to problem 66 (correct one is the function below)
// it generally works, but breaks on very high numbers, it seems like bits overflow the variable somewhere
// I'll leave it here because that's still an interesting solution although probably way slower than the one below
func plusOne_uncorrect(digits []int64) []int64 {
	var num int64 = 0
	var expn float64 = float64(len(digits)) - 1
	for _, val := range digits {
		num += int64((float64(val) * math.Pow(10.0, expn)))
		//fmt.Println(val, num, int64((float64(val) * math.Pow(10.0, expn))), int64(num+int64((float64(val)*math.Pow(10.0, expn)))))
		expn--
	}
	num++
	for i := len(digits) - 1; num != 0; i-- {
		if i < 0 {
			temp := []int64{num % 10}
			temp = append(temp, digits...)
			digits = temp
			return digits
		}
		digits[i] = num % 10
		num -= digits[i]
		num /= 10
	}
	return digits
}

// problem 66. Plus One
// runtime 0ms (on par with 25% of the best solutions), memory 2.08 MB (better than 83% of users)
// https://leetcode.com/problems/plus-one/description/?envType=featured-list&envId=top-interview-questions?envType=featured-list&envId=top-interview-questions
func plusOne(digits []int) []int {
	var idx int = len(digits) - 1
	last := digits[idx]
	last++

	for last > 9 {
		digits[idx] = 0
		idx--
		if idx < 0 {
			temp := []int{1}
			temp = append(temp, digits...)
			digits = temp
			return digits
		}
		last = digits[idx]
		last++
	}

	digits[idx] = last
	return digits
}

func main() {
	digits := []int{9, 9, 9}
	a := plusOne(digits)
	fmt.Println(a)
}
