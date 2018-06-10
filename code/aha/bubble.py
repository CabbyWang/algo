# coding:utf-8


if __name__ == '__main__':
    numbers = [23, 12, 34, 23, 13]
    n = len(numbers)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    print(numbers)
