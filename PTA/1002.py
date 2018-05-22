#!/usr/bin/env python3
# coding:utf-8


if __name__ == '__main__':
    num_piny = {'1': 'yi', '2': 'er', '3': 'san', '4': 'si', '5': 'wu', '6': 'liu',
                '7': 'qi', '8': 'ba', '9': 'jiu', '0': 'ling'}
    inp = input()
    sum = 0
    for i in inp:
        sum += int(i)
    print(' '.join(num_piny[i] for i in str(sum)))
