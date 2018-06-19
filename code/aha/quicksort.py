# coding:utf-8
import random


def quick_sort(nums):
	if len(nums) <= 1:
		return nums
	less = []
	greater = []
	base = nums.pop(random.randrange(len(nums)))

	for i in nums:
		if i < base:
			less.append(i)
		else:
			greater.append(i)

	return quick_sort(less) + [base] + quick_sort(greater)


def exchange(a, b):
	b, a = a, b


def quick_sort2(nums, start, end):
	if start >= end:
		return
	# 基准数
	mid = nums[start]
	# mid = random.sample(nums, 1)[0]
	low = start
	high = end
	# 开始循环
	while low < high:
		while low < high and nums[high] >= mid:
			high -= 1
		while low < high and nums[low] <= mid:
			low += 1
		# 交换
		if low < high:
			# exchange(nums[low], nums[high])
			nums[low], nums[high] = nums[high], nums[low]
	# 将基准数归位
	nums[low], nums[start] = nums[start], nums[low]
	quick_sort2(nums, start, low - 1)
	quick_sort2(nums, low + 1, end)


if __name__ == '__main__':
	# result = quick_sort([2,3,1,6,4,7,5])
	# print(result)
	alist = [2,3,1,6,4,7,5]
	quick_sort2(alist, 0, len(alist) - 1)
	print(alist)
