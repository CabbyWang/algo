#!/usr/bin/env python3
# coding:utf-8

def old_iter():
    """正整数"""
    n = 0
    while True:
        n += 1
        yield n


if __name__ == '__main__':
    n = int(input())
    step = 0
    while n != 1:
        step += 1
        if n % 2 == 0:
            n = n / 2
        else:
            n = (3 * n + 1) / 2
    print(step)
