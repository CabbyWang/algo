# -*- coding: utf-8 -*-
"""
请设计一个函数，用来判断在一个矩阵中是否存在一条包含某字符串所有字符的路径。路径可以从矩阵中的任意一个格子开始，
每一步可以在矩阵中向左，向右，向上，向下移动一个格子。如果一条路径经过了矩阵中的某一个格子，则之后不能再次进入
这个格子。例如 a b c e s f c s a d e e这样的3X4矩阵中包含一条字符串"bcced"的路径，但是矩阵中不包含"abcb"
路径，因为字符串的第一个字符b占据了矩阵中的第一行第二个格子之后，路径不能再次进入该格子。
"""
__author__ = 'cabbyw'

import numpy


def hasPath(matrix, rows, cols, path):

    record = [[0 for i in range(cols)] for j in range(rows)]
    def is_path(i, j, index, record):
        if i < 0 or i >= rows or j < 0 or j >= cols or record[i][j] or matrix[i][j] != path[index]:
            return False
        if index == len(path) - 1:
            return True
        index += 1
        record[i][j] = 1

        flag = any([
            is_path(i + 1, j, index, record),
            is_path(i - 1, j, index, record),
            is_path(i, j + 1, index, record),
            is_path(i, j - 1, index, record)]
        )
        if not flag:
            index -= 1
            record[i][j] = 0
        return flag

    for i in range(rows):
        for j in range(cols):
            index = 0
            if is_path(i, j, index, record):
                return True

    return False


if __name__ == '__main__':
    matrix = numpy.array(['a', 'b', 'c', 'e', 's', 'f', 'c', 's', 'a', 'd', 'e', 'e'])
    matrix.shape = [3, 4]
    # d = hasPath(matrix, 4, 3, 'bcced')
    d = hasPath(matrix, 3, 4, 'bcced')
    print(d)
