package main

import "fmt"

//26. Remove Duplicates from sorted array
//runtime 6 ms (better than 72% of Go users) memory 6.12 mb (better than 5% of Go users)
//https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/?envType=featured-list&envId=top-interview-questions?envType=featured-list&envId=top-interview-questions
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

//problem 28. Find the index of the first occurence in a String
//runtime 1 ms memory 2.00 mb (better than 94% of Go users)
//https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/?envType=featured-list&envId=top-interview-questions?envType=featured-list&envId=top-interview-questions
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

func main() {
	a := strStr("hello", "ll")
	//fmt.Printf("%s\n", a)
	fmt.Printf("%d", a)
}
