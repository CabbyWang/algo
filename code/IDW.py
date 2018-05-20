# coding:utf-8

import math
from functools import reduce
from pathlib import Path
from operator import itemgetter
import numpy as np
from numpy.linalg import inv


def get_coordinates(file_name):
    """获取点的坐标, 返回一个list
    """
    with open(file_name) as fp:
        coordinates = fp.readlines()
        coordinates = list(filter(lambda x: x, [coord.strip('\n') for coord in coordinates]))  # noqa
        coordinates = [eval(c) for c in coordinates]
        return coordinates


def get_distance(x, y, x0, y0):
    """
    计算(x0, y0)到(x, y)之间的距离
    """
    return math.sqrt(pow(x - x0, 2) + pow(y - y0, 2))


def write(out_file, result_coords):
    Path(out_file).parent.mkdir(exist_ok=True)
    with open(out_file, 'w') as f:
        f.writelines((str(i) + '\n' for i in result_coords))


def main(yizhi_file, weizhi_file, out_file):
    """反距离权重插值法"""
    ori_points = get_coordinates(yizhi_file)
    z_points = get_coordinates(weizhi_file)
    result_dict = {}
    for x, y in z_points:
        distances = []
        member = 0         # 分子
        for x0, y0, z0 in ori_points:
            distance = get_distance(x, y, x0, y0)
            distances.append(distance)
            member += z0 / distance

        denominator = reduce(lambda x, y: x + y, (1 / i for i in distances))       # 分母   # noqa
        z = member / denominator
        result_dict[(x, y)] = z         # z坐标
    result_coords = []
    for (x, y), z in result_dict.items():
        result_coords.append((x, y, z))
    write(out_file, result_coords)                 # 写入


def main2(yizhi_file, weizhi_file, out_file):
    """最邻近插值法"""
    ori_points = get_coordinates(yizhi_file)
    z_points = get_coordinates(weizhi_file)
    distances = {}
    result_dict = {}
    for x, y in z_points:
        for x0, y0, z0 in ori_points:
            distance = get_distance(x, y, x0, y0)
            distances[z0] = distance
        z = min(zip(distances.values(), distances.keys()))[1]
        result_dict[(x, y)] = z
    result_coords = []
    for (x, y), z in result_dict.items():
        result_coords.append((x, y, z))
    write(out_file, result_coords)


def main3(yizhi_file, weizhi_file, out_file):
    """线性内插法"""
    ori_points = get_coordinates(yizhi_file)
    z_points = get_coordinates(weizhi_file)
    result_dict = {}
    for x, y in z_points:
        # 取最近三个点
        distance_coord = {get_distance(x, y, x0, y0): (x0, y0, z0) for x0, y0, z0 in ori_points}    # noqa
        # 最近三个点(最近定为(x1, y1))
        [(_, _, z1), (x2, y2, z2), (x3, y3, z3)] = [item[1] for item in sorted(distance_coord.items(), key=itemgetter(0))[:3]]  # noqa
        a = 1 / (x2 * y3 - x3 * y2)
        b1 = x2 * y3 - x3 * y2
        b2 = (y2 - y3) * x
        b3 = (x3 - x2) * y
        c1 = (b1 + b2 + b3) * z1
        c2 = (y3 * x - x3 * y) * z2
        c3 = (x2 * y - y2 * x) * z3
        z = a * (c1 + c2 + c3)
        result_dict[(x, y)] = z
    result_coords = []
    for (x, y), z in result_dict.items():
        result_coords.append((x, y, z))
    write(out_file, result_coords)


def main4(yizhi_file, weizhi_file, out_file, n=6):
    """移动曲面拟合法"""
    ori_points = get_coordinates(yizhi_file)
    z_points = get_coordinates(weizhi_file)
    result_dict = {}
    if n > len(ori_points):
        print('已知点没有{}个!!'.format(n))
        return
    for x, y in z_points:
        # 取最近n个点
        distance_coord = {get_distance(x, y, x0, y0): (x0, y0, z0) for x0, y0, z0 in ori_points}  # noqa
        # 最近n个点的list
        list_n = [item[1] for item in sorted(distance_coord.items(), key=itemgetter(0))[:n]]  # noqa
        # 求权(1/距离的平方)
        list_p = [1 / (pow(x0 - x, 2) + pow(y0 - y, 2)) for x0, y0, _ in list_n]  # noqa
        # 将list转换为对角矩阵
        p = np.diag(np.array(list_p))
        # 已知点构造出的z坐标构造出一个n * 1的矩阵
        z0 = np.array([y0 for _, _, y0 in list_n]).reshape(n, 1)
        # 求M
        list_m = []
        for x0, y0, _ in list_n:
            # d = math.sqrt(pow(x - x0, 2), pow(y - y0, 2))
            d_x = x0 - x
            d_y = y0 - y
            list_m += [pow(d_x, 2), d_x * d_y, pow(d_y, 2), d_x, d_y, 1]
        m = np.array(list_m).reshape(n, 6)

        # 求结果矩阵
        result = inv(m.T.dot(p).dot(m)).dot(m.T).dot(p).dot(z0)
        # 取最后一个
        z = float(list(result)[-1])

        result_dict[(x, y)] = z

    result_coords = []
    for (x, y), z in result_dict.items():
        result_coords.append((x, y, z))
    write(out_file, result_coords)


def main5(yizhi_file, weizhi_file, out_file):
    """双线性多项式内插法"""
    ori_points = get_coordinates(yizhi_file)
    z_points = get_coordinates(weizhi_file)
    result_dict = {}
    if 4 > len(ori_points):
        print('已知点没有{}个!!'.format(4))
        return
    for x, y in z_points:
        # 取最近n个点
        distance_coord = {get_distance(x, y, x0, y0): (x0, y0, z0) for x0, y0, z0 in ori_points}  # noqa
        # 最近n个点的list
        list_n = [item[1] for item in sorted(distance_coord.items(), key=itemgetter(0))[:4]]  # noqa
        [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4)] = list_n
        # 已知点的x坐标矩阵
        z0 = np.array([z1, z2, z3, z4]).reshape(4, 1)

        list_xy = []
        for x0, y0, _ in list_n:
            list_xy += [1, x0, y0, x0 * y0]
        matrix_tem = np.array(list_xy).reshape(4, 4)
        # 求a的矩阵
        matrix_a = np.dot(inv(matrix_tem), z0)
        # 求a0, a1, a2, a3
        a0, a1, a2, a3 = [float(i) for i in list(matrix_a)]

        # 求z
        z = a0 + a1 * x + a2 * y + a3 * x * y
        result_dict[(x, y)] = z

    result_coords = []
    for (x, y), z in result_dict.items():
        result_coords.append((x, y, z))
    write(out_file, result_coords)


if __name__ == '__main__':
    main(r'D:\test\已知点.txt', r'D:\test\未知点.txt', r'D:\test\result1.txt')
    main2(r'D:\test\已知点.txt', r'D:\test\未知点.txt', r'D:\test\result2.txt')
    main3(r'D:\test\已知点.txt', r'D:\test\未知点.txt', r'D:\test\result3.txt')
    main4(r'D:\test\已知点.txt', r'D:\test\未知点.txt', r'D:\test\result4.txt')
    main5(r'D:\test\已知点.txt', r'D:\test\未知点.txt', r'D:\test\result5.txt')
